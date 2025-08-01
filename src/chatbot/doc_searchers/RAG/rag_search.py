from typing import List, Optional
from operator import itemgetter

import chromadb
from llama_index.core.schema import NodeWithScore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import VectorStoreIndex, StorageContext
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import VectorStoreIndex
from llama_index.core.vector_stores import (
    MetadataFilter,
    MetadataFilters,
    FilterOperator,
)
from chromadb.config import Settings
from llama_index.core.indices.vector_store.retrievers import (
    VectorIndexRetriever,
)

from src.chatbot import agents
from src import config


def _connect_to_chroma_collection():
    """
    Connect to the ChromaDB instance.
    """
    client = chromadb.PersistentClient(
        path=config.RAG_DB_PATH, settings=Settings(anonymized_telemetry=False)
    )
    return client.get_or_create_collection(name="main")


def create_retriever():
    """
    Connect to the RAG database and return the collection.
    """
    collection = _connect_to_chroma_collection()
    vector_store = ChromaVectorStore(chroma_collection=collection)
    index = VectorStoreIndex.from_vector_store(
        vector_store=vector_store,
        embed_model=HuggingFaceEmbedding(model_name=config.EMBEDDING_MODEL_PATH),
    )

    retriever = index.as_retriever(
        similarity_top_k=config.PARAMETERS["rag"]["number_of_retrievals"],
        similarity_threshold=config.PARAMETERS["rag"]["retrieval_threshold"],
    )
    return retriever


def _search_rag(
    questions: list[str],
    retriever: VectorIndexRetriever,
    used_ids: Optional[list[int]] = None,
) -> List[NodeWithScore]:

    filters = MetadataFilters(
        filters=[
            MetadataFilter(key="doc_id", value=used_ids, operator=FilterOperator.NIN),
        ]
    )
    retriever._filters = filters if used_ids else None
    for question in questions:
        results = retriever.retrieve(
            query=question,
            n_results=config.PARAMETERS["rag"]["number_of_retrievals"],
            threshold=config.PARAMETERS["rag"]["retrieval_threshold"],
        )

    return results


def _cross_encoder_selection(
    prompt, documents: List[NodeWithScore]
) -> List[NodeWithScore]:
    doc_texts = [doc.node.text for doc in documents]
    best_indices = agents.cross_encoder.find_best_indices(prompt, doc_texts)
    if len(best_indices) == 0:
        return []
    elif len(best_indices) == 1:
        return [documents[best_indices[0]]]
    else:
        return itemgetter(*best_indices)(documents)


def get_rag_docs(
    retriever: VectorIndexRetriever,
    question: str,
    used_ids: Optional[List[int]] = None,
    generator_model: Optional[str] = None,
):

    generated_questions = agents.question_generator.generate_questions(
        model=generator_model,
        question=question,
        number_of_gen_questions=config.PARAMETERS["rag"]["number_of_gen_questions"],
    )

    question_list = [question] + generated_questions

    documents = _search_rag(
        question_list=question_list, retriever=retriever, used_ids=used_ids
    )

    # cross encoder
    best_docs = _cross_encoder_selection(
        documents=documents,
        question=question,
    )

    # summarize each document
    new_used_ids = list()
    search_result_package = "\n"
    for doc in best_docs:
        doc_summary = agents.summary_bot.summarize_page(
            page_text=doc.node.text,
            model=generator_model,
            question=question,
        )
        search_result_package += f"""
        file name: {doc.node.metadata.get('file_name', 'Unknown')}
        file path: {doc.node.metadata.get('file_path', 'Unknown')}
        document: {doc_summary}\n"""

        new_used_ids.append(doc.node.metadata["doc_id"])

    return search_result_package, new_used_ids
