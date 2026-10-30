"""
Shared state for the LangGraph analytics workflow.
"""

from typing import Any, Annotated, TypedDict

from langgraph.graph.message import add_messages


class AnalyticsState(TypedDict, total=False):
    """
    Data passed between the analytics workflow nodes.
    """

    question: str
    sql: str
    results: list[dict[str, Any]]
    row_count: int
    answer: str
    error: str | None

    # Conversation messages accumulated across turns.
    messages: Annotated[list, add_messages]