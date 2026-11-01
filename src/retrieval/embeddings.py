
from langchain_ollama import OllamaEmbeddings

from config import OLLAMA_EMBEDDING_MODEL, OLLAMA_BASE_URL


def get_embedding_model():
    """
    Initialize the Ollama embedding model.
    """
    return OllamaEmbeddings(
        model=OLLAMA_EMBEDDING_MODEL,
        base_url=OLLAMA_BASE_URL
    )


def generate_embeddings(texts):
    """
    Convert a list of texts into numerical vectors.
    """
    if not texts:
        return []

    embedding_model = get_embedding_model()
    return embedding_model.embed_documents(texts)


def generate_query_embedding(text):
    """
    Convert a user question into a numerical vector.
    """
    if not text or not text.strip():
        raise ValueError("Query cannot be empty.")

    embedding_model = get_embedding_model()
    return embedding_model.embed_query(text)


if __name__ == "__main__":
    sample_texts = [
        "Employees receive 21 working days of annual leave.",
        "Employees can request leave through the HR system."
    ]

    vectors = generate_embeddings(sample_texts)

    print("EMBEDDINGS TEST SUCCESSFUL!")
    print("Number of texts:", len(vectors))
    print("Vector dimensions:", len(vectors[0]))
    print("First 5 values:", vectors[0][:5])

    query_vector = generate_query_embedding(
        "How many annual leave days do employees receive?"
    )

    print("\nQuery embedding dimensions:", len(query_vector))
