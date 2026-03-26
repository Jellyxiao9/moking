from app.engine.consistency_rag import ingest_world, WORLD_FILES


def get_available_worlds() -> list[str]:
    return list(WORLD_FILES.keys())


def load_world(world: str) -> None:
    ingest_world(world)