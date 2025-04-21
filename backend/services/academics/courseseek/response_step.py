from typing import Any, Dict
from semantic_kernel import Kernel
from semantic_kernel.prompt_template import PromptTemplateConfig, InputVariable
from semantic_kernel.functions import kernel_function, KernelArguments
from semantic_kernel.processes.kernel_process import KernelProcessStep, KernelProcessStepState, KernelProcessStepContext

from backend.services.academics.courseseek.conversation_context import ConversationContext
from backend.services.academics.courseseek.course_prompt import RESPONSE_PROMPT


class ResponseGenerationStep(KernelProcessStep[ConversationContext]):
    kernel: Kernel | None = None
    state: ConversationContext | None = None

    def __init__(self):
        super().__init__()

    async def activate(self, state: KernelProcessStepState[ConversationContext]):
        self._setup_response_generation()

    def _setup_response_generation(self):
        response_generation_prompt = PromptTemplateConfig(
            template=RESPONSE_PROMPT,
            name="response_generator",
            template_format="semantic-kernel",
            input_variables=[
                InputVariable(name="user_input", is_required=True),
                InputVariable(name="chat_history", is_required=True),
                InputVariable(name="courses", is_required=False)
            ]
        )
        if self.kernel:
            self.kernel.add_function(
                plugin_name="ResponseGenerator",
                function_name="generate_response",
                prompt_template_config=response_generation_prompt
            )

    @kernel_function(name="generate_response")
    async def generate_response(self, data: Dict[str, Any]):
        if not self.kernel:
            raise ValueError("Kernel is not initialized.")
            
        try:
            user_input = data.get("user_input", "")

            courses = data.get("courses", [])
            
            result = await self.kernel.invoke(
                plugin_name="ResponseGenerator",
                function_name="generate_response",
                arguments=KernelArguments(
                    user_input=user_input,
                    chat_history=self.state.to_chat_history().messages,
                    courses=courses
                )
            )
            
            response_text = str(result)
            
            
            self.state.add_user_message(user_input)
            self.state.add_assistant_message(response_text)
            
            return response_text
                
        except Exception as e:
            import traceback
            
            error_msg = "I'm sorry, but I encountered an error processing your request."
            
            self.state.add_user_message(user_input)
            self.state.add_assistant_message(error_msg)
            
            return error_msg