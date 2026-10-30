
"""
LangGraph workflow for movie rental analytics.
"""

from langgraph.graph import END, START, StateGraph

from app.agents.state import AnalyticsState
from app.agents.nodes import (
    generate_sql_node,
    execute_sql_node,
    generate_answer_node,
)


def build_analytics_graph(checkpointer=None):
    """
    Build and compile the analytics workflow.
    """
    workflow = StateGraph(AnalyticsState)

    # Register workflow nodes.
    workflow.add_node("generate_sql", generate_sql_node)
    workflow.add_node("execute_sql", execute_sql_node)
    workflow.add_node("generate_answer", generate_answer_node)

    # Define execution order.
    workflow.add_edge(START, "generate_sql")
    workflow.add_edge("generate_sql", "execute_sql")
    workflow.add_edge("execute_sql", "generate_answer")
    workflow.add_edge("generate_answer", END)

    return workflow.compile(checkpointer=checkpointer)


# Reusable compiled graph.
analytics_graph = build_analytics_graph()
