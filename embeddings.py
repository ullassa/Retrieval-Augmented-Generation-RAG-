import openai
import os
import random

# Set the API key securely
openai.api_key = os.getenv("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")  # or directly use the string if needed
# Qdrant client setup
def get_embedding(text: str) -> list[float]:
    import random
    return [random.uniform(-1, 1) for _ in range(1536)]

