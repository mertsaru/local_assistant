r"""installs files in data to RAG. If the file is already installed to RAG, then the system finds it has already been installed by the hashing of the text and does not import again.

The data searched in Llama-index DB since Llama-index DB built with smaller chunk texts, then the source document retrieved from data folder. Then the model summarizes the document to feed to the model.
"""

import os
from typing import Literal, LiteralString, Optional
import uuid
import json

import llama_index
import chromadb
from chromadb.config import Settings
from llama_index.core import Document
from llama_index.core.node_parser import SentenceSplitter

from src import config
from src.config import logger
from .knowledge_extractors import interpreter, ocr, readers

EMBEDDING_MODEL_PATH = config.EMBEDDING_MODEL_PATH
RAG_DB_PATH = config.RAG_DB_PATH

# KNOWLEDGE PATHS
OCR_FILES_PATH = config.OCR_FILES_PATH
INTERPRETATION_FILES_PATH = config.INTERPRETATION_FILES_PATH
TEXT_FILES_PATH = config.TEXT_FILES_PATH
OCR_FOLDER_LANG_PATH = config.OCR_FOLDER_LANG_PATH

client = chromadb.PersistentClient(
    path=RAG_DB_PATH, settings=Settings(anonymized_telemetry=False)
)

collection = client.get_or_create_collection(name="main")
collection = llama_index.ChromaVectorStore(
    collection=collection,
    embedding_function=llama_index.HuggingFaceEmbeddingFunction(
        model_name=EMBEDDING_MODEL_PATH
    ),
)

with open(OCR_FOLDER_LANG_PATH, "r", encoding="utf-8") as f:
    folder_languages = json.load(f)


def _split_text(text: str) -> list[str]:
    pass


def _install_file(
    file_path: str,
    file_type: Literal["ocr", "interpretation", "text"],
    title: LiteralString,
    content: LiteralString,
    language = Optional[LiteralString] = None,
) -> None:

    if not content:
        return

    content_splits = _split_text(content)

    content_uuids = [
        str(uuid.uuid4()) for _ in content_splits
    ]  # TODO create from content
    split_package = zip(content_splits, content_uuids)

    for content_piece, doc_id in split_package:
        # Create a Document object
        document = Document(
            id=doc_id,
            text=content_piece,
            metadata={
                "source": file_path,
                "file_name": os.path.basename(file_path),
                "title": title,
                "type": file_type,
                "language": language if language else "unknown",
            },
        )

        # Add the document to the collection
        collection.add_documents([document])


def install_knowledge() -> None:
    """Installs all knowledge files to RAG DB."""


    # Install OCR files
    for folder_path , _, files in os.walk(OCR_FILES_PATH):
        language_folder = folder_path.basename(folder_path)
        if language_folder not in folder_languages.keys() and language_folder != "img_to_text_files":
            logger.warning(
                f"Skipping folder {folder_path} due to unsupported language {language}"
            )
            continue
        if language_folder == "img_to_text_files":
            logger.warning(
                f"Files in {folder_path} will be processed with default language 'english' as it is not specified"
            )
            language = "eng"
        else:
            language = language_folder
        for file_name in files:
            ext = os.path.splitext(file_name)[1].lower()
            if ext not in [".jpg", ".jpeg", ".png"]:
                logger.warning(
                    f"Skipping file {file_name} in {folder_path} due to unsupported extension {ext}"
                )
                continue
            file_path = os.path.join(folder_path, file_name)
            title, content = ocr.transform_to_text(file_path, language=language)
            _install_file(file_path, "ocr", title, content, language)

    # Install interpretation files
    for folder_path , _, files in os.walk(INTERPRETATION_FILES_PATH):
        for file_name in files:
            ext = os.path.splitext(file_name)[1].lower()
            if ext not in [".jpg", ".jpeg", ".png", ".gif"]:
                logger.warning(
                    f"Skipping file {file_name} in {folder_path} due to unsupported extension {ext}"
                )
                continue
            file_path = os.path.join(folder_path, file_name)
            title, content = interpreter.interpret(file_path)
            _install_file(file_path, "interpretation", title, content)

    # Install text files
    for file_name in os.listdir(TEXT_FILES_PATH):
        file_path = os.path.join(TEXT_FILES_PATH, file_name)
        title, content = readers.text_reader(file_path)
        _install_file(file_path, "text", title, content)
