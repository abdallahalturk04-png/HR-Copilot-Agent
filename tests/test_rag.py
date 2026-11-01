
import pytest

from src.retrieval.rag_engine import search_policies


def test_search_retrieves_annual_leave_policy():
    results = search_policies(
        "How many annual leave days do employees receive?",
        k=3
    )

    assert len(results) > 0

    best_document, score = results[0]

    assert best_document.metadata["article"] == "Article 2"
    assert "21 working days" in best_document.page_content


def test_search_rejects_empty_question():
    with pytest.raises(ValueError):
        search_policies("")
