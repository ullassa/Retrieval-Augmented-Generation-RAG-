from qdrant_client import QdrantClient
from embeddings import get_embedding  # Your embedding function

QDRANT_URL = "https://a93ea185-7cc0-46db-a70b-e3e78c578ae5.eu-west-2-0.aws.cloud.qdrant.io"
QDRANT_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.-39LTbKRBl0omIWtPUPNXc8yvD3N_KBGe43Dxt__7bM"

client = QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY,
)

collection_name = "kb_collection"

def create_collection():
    collections = client.get_collections().collections
    collection_names = [col.name for col in collections]
    if collection_name not in collection_names:
        client.create_collection(
            collection_name=collection_name,
            vectors_config={"size": 1536, "distance": "Cosine"}
        )


def upload_documents(documents):
    create_collection()
    points = []
    for idx, doc in enumerate(documents):
        embedding = get_embedding(doc)
        points.append({
            "id": idx,
            "vector": embedding,
            "payload": {"text": doc}
        })
    client.upsert(collection_name=collection_name, points=points)
    print(f"Uploaded {len(documents)} documents to Qdrant.")

    # Fetch some points back to verify
result, _ = client.scroll(collection_name=collection_name, limit=10)
print("Documents in collection now:")
for record in result:
    print(record.payload['text'])
