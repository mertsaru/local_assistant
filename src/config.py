# Paths


PARAM_PATH = "src/parameters.yaml"

## Main Chatbot
SYS_PROMPT_PATH = "src/chatbot/sys_prompt.txt"

## Web Search
SUMMARY_LLM_SYS_PROMPT_PATH = "src\chatbot\summary_bot\summary_llm_sys_prompt.txt"

## Question Gen
QUESTION_GEN_SYS_PROMPT_PATH = (
    "src/chatbot/question_generator/question_gen_sys_prompt.txt"
)
CROSS_ENCODER_PATH = "src/models/cross_encoder"

## RAG
EMBEDDING_MODEL_PATH = "src/models/embedding_model"
RAG_DATA_TOPICS_PATH = "src/chatbot/RAG/rag_data_topics.json"
RAG_DB_PATH = "src\chatbot\doc_searchers\RAG\RAG_DB"

### RAG FILES
OCR_FILES_PATH = "data\img_to_text_files"
OCR_FOLDER_LANG_PATH = "data\img_to_text_files\folder_languages.json"
INTERPRETATION_FILES_PATH = "data\interpretation_imgs"
TEXT_FILES_PATH = "data/texts"


## DECIDER LLM
DECIDER_LLM_SYS_PROMPT = "src\chatbot\decider_llm\decide_llm_sys_prompt.txt"
