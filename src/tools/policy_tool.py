
from langchain_core.tools import tool

from src.retrieval.rag_engine import search_policies


@tool
def search_hr_policies(question: str) -> str:
    """
    Search company HR policy documents to answer questions
    about annual leave, leave requests, and end-of-service policy.

    Use this tool whenever an employee asks about HR policies.
    """

    if not question or not question.strip():
        return "Please provide a valid HR policy question."

    try:
        results = search_policies(question, k=3)

        if not results:
            return "No relevant HR policy information was found."

        formatted_results = []

        for document, score in results:
            source = document.metadata.get("source", "Unknown")
            article = document.metadata.get("article", "Unknown")
            title = document.metadata.get("article_title", "Unknown")

            formatted_results.append(
                f"Source: {source}\n"
                f"Article: {article}\n"
                f"Title: {title}\n"
                f"Content: {document.page_content}\n"
                f"Distance: {score:.4f}"
            )

        return "\n\n---\n\n".join(formatted_results)

    except Exception as error:
        return f"Policy search failed: {str(error)}"


if __name__ == "__main__":

    question = "How many annual leave days do employees receive?"

    result = search_hr_policies.invoke(
        {"question": question}
    )

    print("POLICY TOOL TEST")
    print("================")
    print(result)
