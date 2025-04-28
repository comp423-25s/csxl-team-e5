from typing import Any, Dict, List, Type, Union
import json
import re

from sqlalchemy.orm import Session
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.prompt_template import PromptTemplateConfig, InputVariable
from semantic_kernel.functions import kernel_function, KernelArguments
from semantic_kernel.processes import ProcessBuilder
from semantic_kernel.processes.kernel_process import (
    KernelProcessStep,
    KernelProcessStepContext,
    KernelProcessStepState,
)
from semantic_kernel.processes.kernel_process.kernel_process_event import (
    KernelProcessEvent,
)
from semantic_kernel.processes.local_runtime.local_kernel_process import start

from backend.models.courseseek_course import CourseSeekCourse
from backend.services.academics.courseseek.conversation_context import (
    AIResponse,
    ConversationContext,
)
from backend.services.academics.courseseek.course_prompt import (
    COURSE_REC_PROMPT,
    RESPONSE_PROMPT,
)
from backend.services.chat_history_service import get_chat_history


class ConversationStateManager:
    def __init__(
        self,
        azure_openai_deployment: str,
        azure_openai_endpoint: str,
        azure_openai_api_key: str,
    ):
        self.chat_service = AzureChatCompletion(
            deployment_name=azure_openai_deployment,
            endpoint=azure_openai_endpoint,
            api_key=azure_openai_api_key,
        )
        self.kernel = Kernel()
        self.kernel.add_service(self.chat_service)

    def _build_process(self, shared_context: ConversationContext) -> ProcessBuilder:
        process = ProcessBuilder(name="ConversationStateManager")

        def make_step(step_cls: Type[Any]) -> Any:
            step = step_cls()
            step.kernel = self.kernel
            step.state = shared_context
            return step

        rec = process.add_step(
            ConversationStateManager.CourseRecommendationStep,
            factory_function=lambda: make_step(
                ConversationStateManager.CourseRecommendationStep
            ),
        )
        gen = process.add_step(
            ConversationStateManager.ResponseGenerationStep,
            factory_function=lambda: make_step(
                ConversationStateManager.ResponseGenerationStep
            ),
        )

        # always invoke the generation step with a dict payload
        process.on_input_event("UserInput").send_event_to(rec)
        process.on_input_event("UserInput").send_event_to(gen, parameter_name="data")
        rec.on_event("CourseRecommend").send_event_to(gen, parameter_name="data")

        return process

    async def process_message(
        self, db: Session, session_id: str, user_input: str
    ) -> AIResponse:
        db_history = get_chat_history(db, session_id)
        ctx = ConversationContext(session_id=session_id)
        for entry in db_history:
            ctx.add_message(entry.role, entry.message)

        builder = self._build_process(ctx)
        proc = builder.build()

        async with await start(
            process=proc,
            kernel=self.kernel,
            initial_event=KernelProcessEvent(id="UserInput", data=user_input),
        ):
            pass

        assistants = [m for m in ctx.messages if m.role == "assistant"]
        if assistants:
            newest = assistants[-1]
            return AIResponse(message=newest.message, courses=ctx.sections)
        return AIResponse(message="", courses=[])

    class CourseRecommendationStep(KernelProcessStep):
        kernel: Kernel | None = None
        state: ConversationContext | None = None

        async def activate(self, state: KernelProcessStepState) -> None:
            prompt = PromptTemplateConfig(
                template=COURSE_REC_PROMPT,
                name="course_recommendation",
                template_format="semantic-kernel",
                input_variables=[
                    InputVariable(name="user_input", is_required=True),
                    InputVariable(name="chat_history", is_required=True),
                ],
            )
            self.kernel.add_function(
                plugin_name="CourseRecommendation",
                function_name="course_recommend",
                prompt_template_config=prompt,
            )

        @kernel_function(name="recommend_courses")
        async def recommend_courses(
            self, context: KernelProcessStepContext, user_input: str
        ) -> Dict[str, Any]:
            result = await self.kernel.invoke(
                plugin_name="CourseRecommendation",
                function_name="course_recommend",
                arguments=KernelArguments(
                    user_input=user_input,
                    chat_history=self.state.to_chat_history().messages,
                ),
            )
            raw = getattr(result, "content", str(result)).strip()
            if raw.startswith("```"):
                raw = re.sub(r"^```(?:json)?\s*", "", raw)
                raw = re.sub(r"\s*```$", "", raw)

            try:
                parsed = json.loads(raw)
            except json.JSONDecodeError:
                parsed = []

            if isinstance(parsed, dict):
                parsed = [parsed]

            self.state.sections = []
            for item in parsed:
                c = CourseSeekCourse(
                    course_number=item.get("course_number", ""),
                    course_title=item.get("course_title", ""),
                    credits=item.get("credits", ""),
                    description=item.get("description", ""),
                    requirements=item.get("requirements", ""),
                )
                self.state.add_section(c)

            data: Dict[str, Any] = {
                "user_input": user_input,
                "chat_history": self.state.to_chat_history().messages,
                "courses": self.state.sections,
            }
            await context.emit_event(process_event="CourseRecommend", data=data)
            return data

    class ResponseGenerationStep(KernelProcessStep):
        kernel: Kernel | None = None
        state: ConversationContext | None = None

        async def activate(self, state: KernelProcessStepState) -> None:
            prompt = PromptTemplateConfig(
                template=RESPONSE_PROMPT,
                name="response_generator",
                template_format="semantic-kernel",
                input_variables=[
                    InputVariable(name="user_input", is_required=True),
                    InputVariable(name="chat_history", is_required=True),
                    InputVariable(name="courses", is_required=False),
                ],
            )
            self.kernel.add_function(
                plugin_name="ResponseGenerator",
                function_name="generate_response",
                prompt_template_config=prompt,
            )

        @kernel_function(name="generate_response")
        async def generate_response(
            self,
            context: KernelProcessStepContext,
            data: Union[str, Dict[str, Any]],
        ) -> str:
            if isinstance(data, str):
                data = {
                    "user_input": data,
                    "chat_history": self.state.to_chat_history().messages,
                    "courses": [],
                }

            user_input = data.get("user_input", "")
            chat_history = data.get("chat_history", [])
            courses: List[CourseSeekCourse] = data.get("courses", [])

            result = await self.kernel.invoke(
                plugin_name="ResponseGenerator",
                function_name="generate_response",
                arguments=KernelArguments(
                    user_input=user_input,
                    chat_history=chat_history,
                    courses=courses,
                ),
            )
            response = str(getattr(result, "content", result)).strip()

            self.state.add_user_message(user_input)
            self.state.add_assistant_message(response)
            return response
