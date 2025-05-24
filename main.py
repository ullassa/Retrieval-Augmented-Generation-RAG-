import os
import openai
from qdrant_utils import client, upload_documents, collection_name


openai.api_key = os.getenv("OPENAI_API_KEY")

documents = [
    "To reset your router, press and hold the reset button for 10 seconds.",
    "Restarting your computer can fix many issues.",
    "You can change your Wi-Fi password from the router settings page.",
]

def get_embedding(text):
    response = openai.Embedding.create(
        input=text,
        model="text-embedding-3-small"
    )
    return response['data'][0]['embedding']

def query_rag(user_query, top_k=2):
    query_embedding = get_embedding(user_query)

    results = client.search(
        collection_name=collection_name,
        query_vector=query_embedding,
        limit=top_k
    )

    context = "\n".join(hit.payload['text'] for hit in results)

    prompt = f"Use the context below to answer the question:\n\n{context}\n\nQuestion: {user_query}\nAnswer:"

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )

    return response.choices[0].message.content

if __name__ == "__main__":
    upload_documents(documents)
    while True:
        query = input("Ask something (or 'exit' to quit): ")
        if query.lower() == "exit":
            break
        answer = query_rag(query)
        print("Answer:", answer)
