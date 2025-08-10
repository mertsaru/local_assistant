import os

import json

from src.chatbot.agents.topic_finder import topic_finder
import config


def _get_current_topics() -> list[str]:
    if not os.path.exists(config.RAG_DATA_TOPICS_PATH):
        current_topics = []
    else:
        with open(config.RAG_DATA_TOPICS_PATH, "r", encoding="utf-8") as f:
            current_topics = json.load(f)
    return current_topics


def _find_topic(
    text: str,
) -> str | None:
    current_topics = _get_current_topics()
    new_topic = topic_finder.get_topic(text, current_topics)
    if new_topic in current_topics:
        return None
    else:
        return new_topic


def add_to_topics(text: str) -> None:
    new_topic = _find_topic(text)

    if new_topic is not None:
        current_topics = _get_current_topics()
        current_topics.append(new_topic)
        with open(config.RAG_DATA_TOPICS_PATH, "w", encoding="utf-8") as f:
            json.dump(current_topics, f, ensure_ascii=False, indent=4)
    return None
