
import re


def split_policy_documents(
    documents,
    chunk_size=900,
    chunk_overlap=150
):
    """
    Split policy documents while preserving article sections.
    """

    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")

    if chunk_overlap < 0 or chunk_overlap >= chunk_size:
        raise ValueError(
            "chunk_overlap must be between 0 and chunk_size"
        )

    chunks = []

    for document in documents:

        content = document["content"]
        source = document["source"]

        # Split by article headings
        sections = re.split(
            r"(?=ARTICLE\s+\d+\s*:)",
            content,
            flags=re.IGNORECASE
        )

        for section in sections:

            section = section.strip()

            if not section:
                continue

            match = re.search(
                r"ARTICLE\s+(\d+)\s*:\s*([^\n]+)",
                section,
                flags=re.IGNORECASE
            )

            if match:
                article = f"Article {match.group(1)}"
                article_title = match.group(2).strip()
            else:
                article = "General Information"
                article_title = "Policy Introduction"

            # Preserve article metadata in every chunk
            words = section.split()

            start = 0

            while start < len(words):

                end = start + chunk_size

                chunk_text = " ".join(words[start:end])

                chunks.append({
                    "content": chunk_text,
                    "source": source,
                    "article": article,
                    "article_title": article_title
                })

                if end >= len(words):
                    break

                start = end - chunk_overlap

    return chunks


if __name__ == "__main__":

    from src.retrieval.document_loader import (
        load_policy_documents
    )

    documents = load_policy_documents()

    chunks = split_policy_documents(documents)

    print("\nPOLICY CHUNKING RESULTS")
    print("=======================")

    for index, chunk in enumerate(chunks, start=1):

        print(f"\nChunk {index}")
        print("Source:", chunk["source"])
        print("Article:", chunk["article"])
        print("Title:", chunk["article_title"])
        print("Preview:", chunk["content"][:150])

    print("\nTotal documents:", len(documents))
    print("Total chunks:", len(chunks))
