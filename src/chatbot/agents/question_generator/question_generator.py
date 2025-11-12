from pydantic import BaseModel, Field
import os

from langchain_core.messages import SystemMessage, HumanMessage
from langchain.chat_models import init_chat_model

from src import config


with open(config.QUESTION_GEN_SYS_PROMPT_PATH, "r") as f:
    question_gen_sys_prompt = f.read()


class GenQuestion(BaseModel):
    generated_questions: list[str] = Field(
        default=[], description="list of similar generated questions"
    )


question_gen_llm = init_chat_model(
    model=os.getenv("QUESTION_GEN_LLM"),
    model_provider="ollama",
).with_structured_output(GenQuestion)


def generate_questions(question: str, number_of_gen_questions: int) -> list[str]:
    """Uses Ollama model to generate similar questions to a given text. So the model would have a general context of the text.

    Args:

        question (str): the prompt of the user
        number_of_gen_questions (int): number of generated questions

    Returns:
        list[str]: list of generated questions
    """

    history = [
        SystemMessage(question_gen_sys_prompt.format(number_of_gen_questions)),
        HumanMessage(question),
    ]

    response: GenQuestion = question_gen_llm.invoke(history)

    return response.generated_questions
