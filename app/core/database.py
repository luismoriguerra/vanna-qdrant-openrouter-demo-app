from qdrant_client import QdrantClient
from app.core.config import config

def get_qdrant_client() -> QdrantClient:
    return QdrantClient(
        url=config.QDRANT_URL,
        api_key=config.QDRANT_API_KEY,
    )

qdrant_client = get_qdrant_client() 