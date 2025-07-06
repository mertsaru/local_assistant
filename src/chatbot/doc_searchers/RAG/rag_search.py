from typing import Optional

import chromadb
from llama_index import HuggingFaceEmbeddingFunction, ChromaVectorStore
from chromadb.config import Settings

import agents
import config


def _connect_to_chroma():
    """
    Connect to the ChromaDB instance.
    """
    client = chromadb.PersistentClient(
        path=config.RAG_DB_PATH, settings=Settings(anonymized_telemetry=False)
    )
    return client.get_or_create_collection(name="main")


def connect_to_rag_db():
    """
    Connect to the RAG database and return the collection.
    """
    collection = _connect_to_chroma()
    vector_store = ChromaVectorStore(
        collection=collection,
        embedding_function=HuggingFaceEmbeddingFunction(
            model_name=config.EMBEDDING_MODEL_PATH
        ),
    )
    return vector_store


def _search_rag(
    questions: list[str], vector_store, used_ids: Optional[list[int]] = None
):
    pass


def find_docs(
    question,
    vector_store,
    used_ids,
    generator_model,
):

    generated_questions = agents.question_generator.generate_questions(
        model=generator_model,
        question=question,
        number_of_gen_questions=config.PARAMETERS["rag"]["number_of_gen_questions"],
    )

    question_list = [question] + generated_questions

    # search rag discluding used ids


    # cross encoder


    # return docs with ids and metadata
