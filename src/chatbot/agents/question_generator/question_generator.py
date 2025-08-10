from typing_extensions import Annotated, TypedDict

from langchain_core.messages import SystemMessage, HumanMessage
from langchain_ollama import OllamaLLM

from src import config


with open(config.QUESTION_GEN_SYS_PROMPT_PATH, "r") as f:
    question_gen_sys_prompt = f.read()


class GenQuestion(TypedDict):

    generated_questions: Annotated[list[str], "List of generated questions"]

question_gen_llm = OllamaLLM(
    model=config.PARAMETERS["agents"]["question_gen_llm"],
).with_structured_output(GenQuestion())


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

    return response["generated_questions"]