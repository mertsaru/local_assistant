import yaml
import logging
import logging.config
import json

# Parameters
PARAM_PATH = "src/parameters.yaml"
with open(PARAM_PATH, "r") as f:
    PARAMETERS = yaml.safe_load(f)

# Logger
LOG_CONFIG_PATH = "src/custom_logger/logs_config.json"
logger = logging.getLogger("assistant_logger")
with open(LOG_CONFIG_PATH, "r") as f:
    log_config = json.load(f)
logging.config.dictConfig(config=log_config)


# Paths
## Prompts
SYS_PROMPT_PATH = "src/chatbot/sys_prompt.txt"
SUMMARY_LLM_SYS_PROMPT_PATH = "src\chatbot\summary_bot\summary_llm_sys_prompt.txt"
QUESTION_GEN_SYS_PROMPT_PATH = (
    "src/chatbot/question_generator/question_gen_sys_prompt.txt"
)
DECIDER_LLM_SYS_PROMPT = "src\chatbot\decider_llm\decide_llm_sys_prompt.txt"


## Models
CROSS_ENCODER_PATH = "models/cross_encoder"
INTERPRETER_MODEL_PATH = "models/interpreter_model"
EMBEDDING_MODEL_PATH = "models/embedding_model"


### RAG FILES
RAG_DATA_TOPICS_PATH = "src/chatbot/RAG/rag_data_topics.json"
RAG_DB_PATH = "src/chatbot/doc_searchers/RAG/RAG_DB"
OCR_FILES_PATH = "data/img_to_text_files"

INTERPRETATION_FILES_PATH = "data/interpretation_imgs"
TEXT_FILES_PATH = "data/texts"

# Metadatas
CONTACT_JSON_PATH = "metadata/contact.json"
