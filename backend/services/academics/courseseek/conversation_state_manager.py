from typing import Type, TypeVar
from semantic_kernel import Kernel
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.processes import ProcessBuilder
from backend.models.academics.course import Course
from backend.services.academics.courseseek.conversation_context import AIResponse, ChatHistoryResponse, ConversationContext
from backend.services.academics.courseseek.course_recommendation_step import CourseRecommendationStep
from backend.services.academics.courseseek.response_step import ResponseGenerationStep

class ConversationStateManager:
    def __init__(self, azure_openai_deployment: str, azure_openai_endpoint: str, azure_openai_api_key: str):
        self.chat_service = AzureChatCompletion(
            deployment_name=azure_openai_deployment,
            endpoint=azure_openai_endpoint,
            api_key=azure_openai_api_key
        )
        self.kernel = Kernel()
        self.kernel.add_service(self.chat_service)
        self.context = ConversationContext()
        self.process_builder = self._build_process()
        self.process = self.process_builder.build()

    def _build_process(self) -> ProcessBuilder:
        process = ProcessBuilder(name="ConversationStateManager")

        shared_context = self.context

        # Add plugins for semantic functions

        T = TypeVar("T")

        def create_step(step_class: Type[T]):
            step = step_class()
            step.kernel = self.kernel
            step.state = shared_context
            return step
        
        # Adding steps
        course_recommendation_step = process.add_step(
            CourseRecommendationStep,
            factory_function=lambda: create_step(CourseRecommendationStep)
        )

        response_generation_step = process.add_step(
            ResponseGenerationStep,
            factory_function=lambda: create_step(ResponseGenerationStep)
        )

        #Define process flow
        process.on_input_event(event_id="UserInput").send_event_to(
            course_recommendation_step,
            parameter_name="user_input"
        )

        course_recommendation_step.on_event(event_id="CourseRecommend").send_event_to(
            response_generation_step,
            parameter_name="data"
        )
        
        return process
        
    async def process_message(self, user_input: str) -> AIResponse:
        from semantic_kernel.processes.local_runtime.local_kernel_process import start
        from semantic_kernel.processes.kernel_process.kernel_process_event import KernelProcessEvent

        previous_assistant_messages = [msg for msg in self.context.messages if msg.role == "assistant"]

        async with await start(
                process=self.process,
                kernel=self.kernel,
                initial_event=KernelProcessEvent(id="UserInput", data=user_input)
        ) as running_process:
            # The context is properly awaited here
            pass

        current_assistant_messages = [msg for msg in self.context.messages if msg.role == "assistant"]

        if len(current_assistant_messages) > len(previous_assistant_messages):
            newest_message = current_assistant_messages[-1]
            courses = self.context.sections if len(self.context.sections) > 0 else []

            return AIResponse(message=newest_message.message, courses=courses)