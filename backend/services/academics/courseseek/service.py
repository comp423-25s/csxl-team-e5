from typing import Type, TypeVar, Any, Dict
import json
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.prompt_template import PromptTemplateConfig, InputVariable
from semantic_kernel.functions import kernel_function, KernelArguments
from semantic_kernel.processes import ProcessBuilder
from semantic_kernel.processes.kernel_process import (
    KernelProcessStep,
    KernelProcessStepState,
    KernelProcessStepContext,
)
from semantic_kernel.processes.local_runtime.local_kernel_process import start
from semantic_kernel.processes.kernel_process.kernel_process_event import (
    KernelProcessEvent,
)
from backend.models.academics.course import Course
from backend.models.courseseek_course import CourseSeekCourse
from backend.services.academics.courseseek.conversation_context import (
    AIResponse,
    ConversationContext,
)
from backend.services.academics.courseseek.course_prompt import (
    COURSE_REC_PROMPT,
    RESPONSE_PROMPT,
)
import re


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
        self.context = ConversationContext()
        self.process_builder = self._build_process()
        self.process = self.process_builder.build()

    def _build_process(self) -> ProcessBuilder:
        process = ProcessBuilder(name="ConversationStateManager")
        shared_context = self.context

        T = TypeVar("T")

        def create_step(step_class: Type[T]) -> T:
            step = step_class()
            step.kernel = self.kernel
            step.state = shared_context
            return step

        course_recommendation = process.add_step(
            ConversationStateManager.CourseRecommendationStep,
            factory_function=lambda: create_step(
                ConversationStateManager.CourseRecommendationStep
            ),
        )
        response_generation = process.add_step(
            ConversationStateManager.ResponseGenerationStep,
            factory_function=lambda: create_step(
                ConversationStateManager.ResponseGenerationStep
            ),
        )

        process.on_input_event(event_id="UserInput").send_event_to(
            course_recommendation, parameter_name="user_input"
        )
        course_recommendation.on_event(event_id="CourseRecommend").send_event_to(
            response_generation, parameter_name="data"
        )

        return process

    async def process_message(self, user_input: str) -> AIResponse:
        previous = [msg for msg in self.context.messages if msg.role == "assistant"]

        async with await start(
            process=self.process,
            kernel=self.kernel,
            initial_event=KernelProcessEvent(id="UserInput", data=user_input),
        ) as running:
            pass

        current = [msg for msg in self.context.messages if msg.role == "assistant"]
        if len(current) > len(previous):
            newest = current[-1]
            courses = self.context.sections if self.context.sections else []
            return AIResponse(message=newest.message, courses=courses)
        return AIResponse(message="", courses=[])

    class CourseRecommendationStep(KernelProcessStep[ConversationContext]):
        kernel: Kernel | None = None
        state: ConversationContext | None = None

        def __init__(self):
            super().__init__()

        async def activate(self, state: KernelProcessStepState[ConversationContext]):
            self._setup_class_recommendation()

        def _setup_class_recommendation(self):
            prompt = PromptTemplateConfig(
                template=COURSE_REC_PROMPT,
                name="course_recommendation",
                template_format="semantic-kernel",
                input_variables=[
                    InputVariable(name="user_input", is_required=True),
                    InputVariable(name="chat_history", is_required=True),
                ],
            )
            if self.kernel:
                self.kernel.add_function(
                    plugin_name="CourseRecommendation",
                    function_name="course_recommend",
                    prompt_template_config=prompt,
                )

        @kernel_function(name="recommend_courses")
        async def recommend_courses(
            self, context: KernelProcessStepContext, user_input: str
        ):
            if not self.kernel:
                raise ValueError("Kernel is not initialized.")

            data = {"user_input": user_input}

            try:
                result = await self.kernel.invoke(
                    plugin_name="CourseRecommendation",
                    function_name="course_recommend",
                    arguments=KernelArguments(
                        user_input=user_input,
                        chat_history=self.state.to_chat_history().messages,
                    ),
                )

                raw = getattr(result, "content", None) or str(result)
                text = raw.strip()
                print("Raw AI output repr:", repr(text))

                if text.startswith("```"):
                    text = re.sub(r"^```(?:json)?\s*", "", text)
                    text = re.sub(r"\s*```$", "", text)
                    print("🔍 Stripped fences repr:", repr(text))

                try:
                    parsed = json.loads(text)
                    print("JSON parsed successfully:", parsed)
                except json.JSONDecodeError as je:
                    print("‼ JSON decode error:", je)
                    parsed = []

                if isinstance(parsed, dict):
                    parsed = [parsed]

                courses = []
                for item in parsed:
                    course = CourseSeekCourse(
                        course_number=item.get("course_number", ""),
                        course_title=item.get("course_title", ""),
                        credits=item.get("credits", ""),
                        description=item.get("description", ""),
                        requirements=item.get("requirements", ""),
                    )
                    courses.append(course)
                    self.state.add_section(course)

                if courses:
                    data["courses"] = courses

            except Exception as e:
                print("‼ recommend_courses turned into voodoo:", e)

            await context.emit_event(process_event="CourseRecommend", data=data)
            print("Emitted data:", data)
            return data

    class ResponseGenerationStep(KernelProcessStep[ConversationContext]):
        kernel: Kernel | None = None
        state: ConversationContext | None = None

        def __init__(self):
            super().__init__()

        async def activate(self, state: KernelProcessStepState[ConversationContext]):
            self._setup_response_generation()

        def _setup_response_generation(self):
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
            if self.kernel:
                self.kernel.add_function(
                    plugin_name="ResponseGenerator",
                    function_name="generate_response",
                    prompt_template_config=prompt,
                )

        @kernel_function(name="generate_response")
        async def generate_response(self, data: Dict[str, Any]):
            if not self.kernel:
                raise ValueError("Kernel is not initialized.")
            user_input = data.get("user_input", "")
            try:
                result = await self.kernel.invoke(
                    plugin_name="ResponseGenerator",
                    function_name="generate_response",
                    arguments=KernelArguments(
                        user_input=user_input,
                        chat_history=self.state.to_chat_history().messages,
                        courses=data.get("courses", []),
                    ),
                )
                response = str(result)
            except Exception:
                response = (
                    "I'm sorry, but I encountered an error processing your request."
                )
            self.state.add_user_message(user_input)
            self.state.add_assistant_message(response)
            return response
