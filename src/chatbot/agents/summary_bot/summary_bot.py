from langchain_core.messages import HumanMessage, SystemMessage
from langchain.chat_models import init_chat_model

from src import config


with open(config.SUMMARY_LLM_SYS_PROMPT_PATH, "r") as f:
    summary_llm_sys_prompt = f.read()

summary_llm = init_chat_model(
    model=config.PARAMETERS["agents"]["summary_llm"], model_provider="ollama",
)


def summarize_page(page_text: str, source_text) -> str:
    summary_hist = [
        SystemMessage(summary_llm_sys_prompt.format(source_text)),
        HumanMessage(page_text),
    ]
    summary = summary_llm.invoke(summary_hist)
    return summary.content
