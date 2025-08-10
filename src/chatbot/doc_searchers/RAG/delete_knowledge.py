import chromadb
from chromadb.config import Settings

from src import config

client = chromadb.PersistentClient(
    path=config.RAG_DB_PATH, settings=Settings(anonymized_telemetry=False)
)

collection_chunk = client.get_or_create_collection(name="chunk")


collection_main = client.get_or_create_collection(name="main")


def _delete(collection, file_path):
    ids_to_delete = collection.get(where={"file_path": file_path})["ids"]
    if ids_to_delete:
        collection.delete(ids=ids_to_delete)
        config.logger.info(f"Deleted from main collection: {file_path}")
    else:
        config.logger.info(
            f"No documents found in main collection for file: {file_path}"
        )


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Delete knowledge from RAG database")
    parser.add_argument("file_path", type=str, help="Path to the file to delete", required=True)
    args = parser.parse_args()

    # Delete from chunk collection
    _delete(collection_chunk, args.file_path)

    # Delete from main collection
    _delete(collection_main, args.file_path)
