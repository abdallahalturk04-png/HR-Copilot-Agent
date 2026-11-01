
from pathlib import Path


# Project root directory
PROJECT_ROOT = Path(__file__).resolve().parents[2]

POLICIES_DIR = PROJECT_ROOT / "data" / "policies"


def load_policy_documents():
    """
    Load all TXT policy documents.

    Returns:
        A list of dictionaries containing:
        - content
        - source
    """

    documents = []

    if not POLICIES_DIR.exists():
        raise FileNotFoundError(
            f"Policies directory not found: {POLICIES_DIR}"
        )

    policy_files = sorted(POLICIES_DIR.glob("*.txt"))

    if not policy_files:
        raise ValueError(
            "No policy TXT files were found."
        )

    for file_path in policy_files:

        content = file_path.read_text(
            encoding="utf-8"
        ).strip()

        if not content:
            print(f"Skipping empty policy: {file_path.name}")
            continue

        documents.append({
            "content": content,
            "source": file_path.name
        })

    if not documents:
        raise ValueError(
            "All policy documents are empty."
        )

    return documents


if __name__ == "__main__":

    docs = load_policy_documents()

    print("POLICY DOCUMENTS LOADED")
    print("=======================")

    for doc in docs:

        print(f"\nSource: {doc['source']}")
        print(f"Characters: {len(doc['content'])}")

        print("\nPreview:")
        print(doc["content"][:300])

    print("\nTotal documents:", len(docs))
