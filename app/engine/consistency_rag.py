from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import MarkdownTextSplitter
from app.repositories.vector_repo import add_documents, search
from app.infrastructure.config import get_settings
import os

settings = get_settings()

WORLD_FILES = {
    "cyberpunk": "app/worlds/cyberpunk.md",
    "fantasy":   "app/worlds/fantasy.md",
    "noir":      "app/worlds/noir.md",
}


def ingest_world(world: str) -> None:
    path = WORLD_FILES.get(world)
    if not path or not os.path.exists(path):
        raise ValueError(f"世界观文件不存在: {world}")

    loader = TextLoader(path, encoding="utf-8")
    docs = loader.load()

    splitter = MarkdownTextSplitter(chunk_size=500, chunk_overlap=80)
    chunks = splitter.split_documents(docs)

    add_documents(world, chunks)
    print(f"[RAG] {world} 向量化完成，共 {len(chunks)} 个片段")


def get_context(world: str, scene: str) -> str:
    results = search(world, scene, k=3)
    if not results:
        return ""
    return "\n\n".join(r.page_content for r in results)