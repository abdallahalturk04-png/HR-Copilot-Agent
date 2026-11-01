
from langchain_chroma import Chroma

from config import (
    CHROMA_DIR,
    CHROMA_COLLECTION_NAME
)

from src.retrieval.document_loader import load_policy_documents
from src.retrieval.text_splitter import split_policy_documents
from src.retrieval.embeddings import get_embedding_model


def build_vector_store():
    """
    Load policies, split them into chunks,
    generate embeddings, and store them in ChromaDB.
    """

    print("Loading HR policies...")

    documents = load_policy_documents()

    print("Splitting policies into chunks...")

    chunks = split_policy_documents(documents)

    if not chunks:
        raise ValueError("No policy chunks were generated.")

    print(f"Generated {len(chunks)} chunks.")

    print("Initializing embedding model...")

    embedding_model = get_embedding_model()

    print("Building ChromaDB vector store...")

    vector_store = Chroma.from_documents(
        documents=[
            __import__("langchain_core.documents", fromlist=["Document"]).Document(
                page_content=chunk["content"],
                metadata={
                    "source": chunk["source"],
                    "article": chunk["article"],
                    "article_title": chunk["article_title"]
                }
            )
            for chunk in chunks
        ],
        embedding=embedding_model,
        collection_name=CHROMA_COLLECTION_NAME,
        persist_directory=str(CHROMA_DIR)
    )

    print("Vector store created successfully!")

    return vector_store


def search_policies(question, k=3):
    """
    Search for the most relevant HR policy chunks.
    """

    if not question or not question.strip():
        raise ValueError("Question cannot be empty.")

    vector_store = Chroma(
        collection_name=CHROMA_COLLECTION_NAME,
        embedding_function=get_embedding_model(),
        persist_directory=str(CHROMA_DIR)
    )

    results = vector_store.similarity_search_with_score(
        question,
        k=k
    )

    return results


if __name__ == "__main__":

    vector_store = build_vector_store()

    question = "How many annual leave days do employees receive?"

    print("\nSearching HR policies...")
    results = search_policies(question)

    for index, (document, score) in enumerate(results, start=1):
        print(f"\nResult {index}")
        print("Source:", document.metadata.get("source"))
        print("Article:", document.metadata.get("article"))
        print("Title:", document.metadata.get("article_title"))
        print("Distance:", score)
        print("Content:", document.page_content[:400])
