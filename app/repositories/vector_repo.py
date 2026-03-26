from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from app.infrastructure.config import get_settings

settings = get_settings()


def get_embeddings():
    return HuggingFaceEmbeddings(
        model_name="BAAI/bge-small-zh-v1.5",
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )


def get_vectorstore(world: str) -> Chroma:
    return Chroma(
        collection_name=f"world_{world}",
        embedding_function=get_embeddings(),
        persist_directory=settings.chroma_persist_dir,
    )


def add_documents(world: str, docs: list) -> None:
    vectorstore = get_vectorstore(world)
    vectorstore.add_documents(docs)


def search(world: str, query: str, k: int = 3) -> list:
    vectorstore = get_vectorstore(world)
    return vectorstore.similarity_search(query, k=k)