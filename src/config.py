import logging
import yaml
import logging.config
import json
import os

from dotenv import load_dotenv

load_dotenv()

# Parameters
PARAM_PATH = "src/parameters.yaml"
with open(PARAM_PATH, "r") as f:
    PARAMETERS = yaml.safe_load(f)

# Logger
LOG_CONFIG_PATH = "src/logs_config.json"
logger = logging.getLogger("assistant_logger")
with open(LOG_CONFIG_PATH, "r") as f:
    log_config = json.load(f)
logging.config.dictConfig(config=log_config)


# Paths
## Prompts
SYS_PROMPT_PATH = "src/chatbot/sys_prompt.txt"
SUMMARY_LLM_SYS_PROMPT_PATH = "src/chatbot/agents/summary_bot/summary_llm_sys_prompt.txt"
QUESTION_GEN_SYS_PROMPT_PATH = (
    "src/chatbot/agents/question_generator/question_gen_sys_prompt.txt"
)
DECIDER_LLM_SYS_PROMPT = "src/chatbot/agents/decider_llm/decide_llm_sys_prompt.txt"
TOPIC_FINDER_LLM_SYS_PROMPT_PATH = (
    "src/chatbot/agents/topic_finder/topic_finder_sys_prompt.txt"
)

## Models
CROSS_ENCODER_PATH = "models/cross_encoder"
INTERPRETER_MODEL_PATH = "models/interpreter_model"
EMBEDDING_MODEL_PATH = "models/embedding_model"
NLTK_DATA_PATH = "models/sentence_splitter"

### RAG FILES # TODO make postgres tables with pgvector and document table
RAG_DB_PATH = "src/chatbot/doc_searchers/RAG/RAG_DB"

RAG_DATA_TOPICS_PATH = (
    "src/chatbot/RAG/rag_data_topics.json"  # TODO make postgres table
)
FOLDER_LANGUAGE_PATH = "data/folder_languages.json"

OCR_FILES_PATH = "data/img_to_text_files"
INTERPRETATION_FILES_PATH = "data/interpretation_imgs"
TEXT_FILES_PATH = "data/texts"

# List Data # TODO make postgres tables
CONTACT_JSON_PATH = "metadata/contact.json"
SHOPPING_LIST_PATH = "metadata/shopping_list.json"

# Sound
ALARM_SOUND_PATH = "sounds/alarm.wav"
terminal = os.getenv("TERMINAL", "PowerShell")

# API
PORT = int(os.getenv("PORT", "11987"))
HOST = os.getenv("HOST", "0.0.0.0")
WORKERS = int(os.getenv("WORKERS", "1"))


# Email
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

# Telegram
TELEGRAM_API_KEY = os.getenv("TELEGRAM_API_KEY")