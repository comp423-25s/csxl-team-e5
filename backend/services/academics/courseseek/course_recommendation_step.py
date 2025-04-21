import json
import uuid
from semantic_kernel import Kernel
from semantic_kernel.prompt_template import PromptTemplateConfig, InputVariable
from semantic_kernel.functions import kernel_function, KernelArguments
from semantic_kernel.processes.kernel_process import KernelProcessStep, KernelProcessStepState, KernelProcessStepContext
from backend.models.academics.course import Course
from backend.services.academics.courseseek.conversation_context import ConversationContext
from backend.services.academics.courseseek.course_prompt import COURSE_REC_PROMPT


class CourseRecommendationStep(KernelProcessStep[ConversationContext]):
    kernel: Kernel | None = None
    state: ConversationContext | None = None

    def __init__(self):
        super().__init__()


    async def activate(self, state: KernelProcessStepState[ConversationContext]):
        self._setup_class_recommendation()

    def _setup_class_recommendation(self):
        class_recommendation_prompt = PromptTemplateConfig(
            template=COURSE_REC_PROMPT,
            name="course_recommendation",
            template_format="semantic-kernel",
            input_variables=[
                InputVariable(name="user_input", is_required=True),
                InputVariable(name="chat_history", is_required=True)
            ]
        )
        if self.kernel:
            self.kernel.add_function(
                plugin_name="CourseRecommendation",
                function_name="course_recommend",
                prompt_template_config=class_recommendation_prompt
            )

    @kernel_function(name="recommend_courses")
    async def recommend_courses(self, context: KernelProcessStepContext, user_input: str):
        if not self.kernel:
            raise ValueError("Kernel is not initialized.")
            
        try:
            result = await self.kernel.invoke(
                plugin_name="CourseRecommendation",
                function_name="course_recommend",
                arguments=KernelArguments(
                    user_input=user_input,
                    chat_history=self.state.to_chat_history().messages,
                )
            )
            
            data_result = {
                "user_input": user_input,
            }
            
            result_str = str(result).strip()
            if not result_str or result_str.lower() == "null":
                await context.emit_event(process_event="CourseRecommend", data=data_result)
                return data_result
                
            try:
                courses_dict = json.loads(result_str)

                if courses_dict is None:
                    await context.emit_event(process_event="CourseRecommend", data=data_result)
                    return data_result
                    
                if courses_dict is None or courses_dict == "null":
                    await context.emit_event(process_event="CourseRecommend", data=data_result)
                    return data_result
                    
                if not isinstance(courses_dict, list):
                    if isinstance(courses_dict, dict):
                        courses_dict = [courses_dict]
                    else:
                        await context.emit_event(process_event="CourseRecommend", data=data_result)
                        return data_result
                
                courses = []
                for course_dict in courses_dict:
                    if not isinstance(course_dict, dict):
                        continue
                    
                    course_number_parts = course_dict.get("course_number", "").split()
                    subject_code = course_number_parts[0] if len(course_number_parts) > 0 else ""
                    number = course_number_parts[1] if len(course_number_parts) > 1 else ""
                    
                    try:
                        course = Course(
                            id = "0",
                            subject_code=subject_code,
                            number=number,
                            title=course_dict.get("course_title", ""),
                            description=course_dict.get("description", ""),
                            credit_hours=int(course_dict.get("credits", "0")) if course_dict.get("credits", "").isdigit() else 0,
                        )
                        courses.append(course)
                        self.state.add_sections(course)
                    except Exception:
                        continue
                
                data_result["courses"] = courses
                
                await context.emit_event(process_event="CourseRecommend", data=data_result)
                return data_result
                
            except json.JSONDecodeError as e:
                await context.emit_event(process_event="CourseRecommend", data=data_result)
                return data_result
                
        except Exception:
            data_result = {
                "user_input": user_input,
                "courses": []
            }
            await context.emit_event(process_event="CourseRecommend", data=data_result)
            return data_result
