
"""
Nodes for the LangGraph movie rental analytics workflow.
"""
from langchain_core.messages import AIMessage, HumanMessage
from app.agents.state import AnalyticsState
from app.database.executor import execute_query
from app.llm.answer_generator import generate_answer
from app.llm.sql_generator import generate_sql


def generate_sql_node(state: AnalyticsState) -> dict:
    """
    Generate SQL using the current question and previous
    conversation messages.
    """
    question = state["question"]

    messages = state.get("messages", [])

    # Keep the most recent five conversation turns.
    recent_messages = messages[-10:]

    history_lines = []

    for message in recent_messages:
        if message.type == "human":
            role = "Human"
        elif message.type == "ai":
            role = "AI"
        else:
            continue

        history_lines.append(f"{role}: {str(message.content)[:1000]}")

    conversation_history = "\n".join(history_lines)

    sql = generate_sql(
        question,
        conversation_history=conversation_history,
    )

    return {"sql": sql}


def execute_sql_node(state: AnalyticsState) -> dict:
    """Validate and execute the generated SQL."""
    sql = state["sql"]

    results = execute_query(sql)

    return {
        "results": results,
        "row_count": len(results),
    }



def generate_answer_node(state: AnalyticsState) -> dict:
    """
    Generate an explanation and record the conversation turn.
    """
    answer = generate_answer(
        question=state["question"],
        sql_query=state["sql"],
        results=state["results"],
    )

    return {
        "answer": answer,
        "messages": [
            HumanMessage(content=state["question"]),
            AIMessage(content=answer),
        ],
    }
