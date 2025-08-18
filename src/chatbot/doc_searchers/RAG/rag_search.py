from typing import List, Optional

import chromadb
from llama_index.core.schema import NodeWithScore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import VectorStoreIndex
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


client = chromadb.PersistentClient(
    path=config.RAG_DB_PATH, settings=Settings(anonymized_telemetry=False)
)
main_collection = client.get_or_create_collection(name="main")
chunk_collection = client.get_or_create_collection(name="chunk")

vector_store = ChromaVectorStore(chroma_collection=chunk_collection)
index = VectorStoreIndex.from_vector_store(
    vector_store=vector_store,
    embed_model=HuggingFaceEmbedding(model_name=config.EMBEDDING_MODEL_PATH),
)
retriever: VectorIndexRetriever = index.as_retriever(
    similarity_top_k=config.PARAMETERS["rag"]["number_of_retrievals"],
    similarity_threshold=config.PARAMETERS["rag"]["retrieval_threshold"],
)


def _search_rag(
    questions: list[str],
    used_ids: Optional[list[int]] = None,
) -> List[NodeWithScore]:

    filters = MetadataFilters(
        filters=[
            MetadataFilter(key="doc_id", value=used_ids, operator=FilterOperator.NIN),
        ]
    )
    retriever._filters = filters if used_ids != [] else None
    for question in questions:
        results = retriever.retrieve(
            query=question,
            n_results=config.PARAMETERS["rag"]["number_of_retrievals"],
            threshold=config.PARAMETERS["rag"]["retrieval_threshold"],
        )

    return results


def _best_doc_ids(question: str, documents: List[NodeWithScore]) -> List[NodeWithScore]:
    doc_texts = [doc.node.text for doc in documents]
    best_indices = agents.cross_encoder.find_best_indices(question, doc_texts)
    return [documents[i].node.metadata["doc_id"] for i in best_indices]


def get_rag_docs(
    question: str,
    used_ids: Optional[List[int]] = None,
):

    generated_questions = agents.question_generator.generate_questions(
        question=question,
        number_of_gen_questions=config.PARAMETERS["rag"]["number_of_gen_questions"],
    )

    question_list = [question] + generated_questions

    documents = _search_rag(question_list=question_list, used_ids=used_ids)

    # cross encoder
    best_doc_ids = _best_doc_ids(
        documents=documents,
        question=question,
    )

    # get from chroma
    best_results = main_collection.get(
        ids=best_doc_ids,
        include=["documents", "metadatas"],
    )

    # summarize each document
    new_used_ids = []
    doc_packages = []
    for i in range(len(best_results["ids"])):
        doc_summary = agents.summary_bot.summarize_page(
            page_text=best_results["documents"][i],
            question=question,
        )
        doc_packages.append(f"""
        file name: {best_results["metadatas"][i]["file_name"]}
        file path: {best_results["metadatas"][i]["file_path"]}
        document: {doc_summary}\n""")

        new_used_ids.append(best_results["ids"][i])

    return doc_packages, new_used_ids
