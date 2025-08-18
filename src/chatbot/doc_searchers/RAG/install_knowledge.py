r"""installs files in data to RAG. If the file is already installed to RAG, then the system finds it has already been installed by the hashing of the text and does not import again.

The data searched in Llama-index DB since Llama-index DB built with smaller chunk texts, then the source document retrieved from data folder. Then the model summarizes the document to feed to the model.
"""

import os
from typing import Literal, LiteralString
import uuid
import json


import chromadb
from chromadb.config import Settings
from langchain.text_splitter import NLTKTextSplitter
from llama_index.core import Document
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

from src import config
from src.config import logger
from .knowledge_extractors import interpreter, ocr, readers
from . import extract_rag_topics


RAG_DB_PATH = config.RAG_DB_PATH

bare_splitter = NLTKTextSplitter(chunk_size=1024, chunk_overlap=128, separator=" ")

# KNOWLEDGE PATHS
OCR_FILES_PATH = config.OCR_FILES_PATH
INTERPRETATION_FILES_PATH = config.INTERPRETATION_FILES_PATH
TEXT_FILES_PATH = config.TEXT_FILES_PATH

client = chromadb.PersistentClient(
    path=RAG_DB_PATH, settings=Settings(anonymized_telemetry=False)
)

collection_chunk = client.get_or_create_collection(name="chunk")
vector_store = ChromaVectorStore(
    collection=collection_chunk,
    embedding_function=HuggingFaceEmbedding(model_name=config.EMBEDDING_MODEL_PATH),
)

collection_main = client.get_or_create_collection(
    name="main"
)  # TODO change main collection to just document store without embedding db for efficiency

with open(config.FOLDER_LANGUAGE_PATH, "r", encoding="utf-8") as f:
    folder_languages = json.load(f)


def _add_to_chunk_collection(
    content_piece: str, doc_id: str, metadata: dict, language: str
) -> None:
    bare_splitter._chunk_size = 256
    bare_splitter._chunk_overlap = 32
    cont_pieces = bare_splitter.split_text(content_piece)
    for cont_piece in cont_pieces:
        document = Document(
            id_=doc_id,
            text_resource=cont_piece,
            metadata={
                "doc_id": doc_id,
            }
            | metadata,  # Merge with additional metadata
        )

        # Add the document to the collection
        vector_store.add([document])


def _add_to_main_collection(content_piece: str, doc_id: str, metadata: dict):
    collection_main.add(ids=[doc_id], documents=[content_piece], metadatas=[metadata])


def _install_file(
    file_path: str,
    file_type: Literal["ocr", "interpretation", "text"],
    title: LiteralString,
    content: LiteralString,
    language: LiteralString,
) -> None:

    if not content:
        return

    language = folder_languages.get(language, "unknown")
    bare_splitter._language = language
    content_splits = bare_splitter.split_text(content)

    content_uuids = [
        str(uuid.uuid3(uuid.NAMESPACE_DNS, content_piece))
        for content_piece in content_splits
    ]
    split_package = zip(content_splits, content_uuids)
    metadata = {
        "source": file_path,
        "title": title,
        "type": file_type,
        "language": language if language else "unknown",
    }
    for content_piece, doc_id in split_package:

        _add_to_main_collection(content_piece, doc_id, metadata)

        _add_to_chunk_collection(content_piece, doc_id, metadata, language=language)

        extract_rag_topics.add_to_topics(content_piece)


def _check_language_folder(folder_name: str, base_folder) -> bool:
    if folder_name == base_folder:
        return True
    elif folder_name not in folder_languages.keys():
        logger.warning(
            f'Skipping folder "{folder_name}" due to unsupported language {folder_name}'
        )
        return True
    else:
        return False


def install_knowledge() -> None:
    """Installs all knowledge files to RAG DB."""

    # Install OCR files
    for folder_path, _, files in os.walk(OCR_FILES_PATH):
        language = os.path.basename(folder_path)

        if _check_language_folder(language, os.path.basename(OCR_FILES_PATH)):
            continue
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
    for folder_path, _, files in os.walk(INTERPRETATION_FILES_PATH):
        language = os.path.basename(folder_path)
        if _check_language_folder(
            language, os.path.basename(INTERPRETATION_FILES_PATH)
        ):
            continue
        for file_name in files:
            ext = os.path.splitext(file_name)[1].lower()
            if ext not in [".jpg", ".jpeg", ".png", ".gif"]:
                logger.warning(
                    f"Skipping file {file_name} in {folder_path} due to unsupported extension {ext}"
                )
                continue
            file_path = os.path.join(folder_path, file_name)
            title, content = interpreter.interpret(file_path)
            _install_file(
                file_path, "interpretation", title, content, language=language
            )

    # Install text files
    for folder_path, _, files in os.walk(TEXT_FILES_PATH):
        language = os.path.basename(folder_path)
        if _check_language_folder(language, os.path.basename(TEXT_FILES_PATH)):
            continue
    for file_name in files:
        file_path = os.path.join(folder_path, file_name)
        title, content = readers.text_reader(file_path)
        _install_file(file_path, "text", title, content, language=language)


if __name__ == "__main__":
    install_knowledge()
