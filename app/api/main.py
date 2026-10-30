"""FastAPI backend for the Movie Rental AI Analytics Assistant."""

import logging
from contextlib import asynccontextmanager
from typing import Any
from uuid import uuid4

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from app.agents.graph import build_analytics_graph
from app.database.memory import create_memory_checkpointer
from app.database.validator import SQLValidationError
from app.services.overview import get_dashboard_overview

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage persistent LangGraph checkpoint storage."""
    pool, checkpointer = create_memory_checkpointer()
    pool.open(wait=True)
    try:
        app.state.checkpointer = checkpointer
        app.state.analytics_graph = build_analytics_graph(checkpointer=checkpointer)
        logger.info("PostgreSQL conversation memory initialized")
        yield
    finally:
        pool.close()
        logger.info("PostgreSQL conversation memory connection closed")


app = FastAPI(
    title="Movie Rental AI Analytics API",
    description="AI-powered analytics for the movie rental database.",
    version="0.1.0",
    lifespan=lifespan,
)


class AnalyzeRequest(BaseModel):
    question: str = Field(min_length=3, max_length=500, description="Natural-language business question")
    thread_id: str | None = Field(
        default=None, min_length=1, max_length=100,
        description="Conversation ID for follow-up questions",
    )


class AnalyzeResponse(BaseModel):
    question: str
    answer: str
    results: list[dict[str, Any]]
    row_count: int
    sql: str
    thread_id: str


@app.get("/health")
def health_check() -> dict[str, str]:
    """Check whether the API is running."""
    return {"status": "healthy", "service": "movie-rental-analytics"}


@app.post("/analyze", response_model=AnalyzeResponse)
def analyze(request: AnalyzeRequest) -> AnalyzeResponse:
    """Run the LangGraph analytics workflow."""
    question = request.question.strip()
    if not question:
        raise HTTPException(status_code=422, detail="Question cannot be empty.")

    thread_id = request.thread_id or str(uuid4())
    config = {"configurable": {"thread_id": thread_id}}

    try:
        response = app.state.analytics_graph.invoke({"question": question}, config=config)
        return AnalyzeResponse(
            question=question,
            answer=response["answer"],
            results=response["results"],
            row_count=response["row_count"],
            sql=response["sql"],
            thread_id=thread_id,
        )
    except SQLValidationError:
        raise HTTPException(status_code=422, detail="The generated query could not be validated.")
    except Exception:
        logger.exception("Analytics workflow failed")
        raise HTTPException(status_code=500, detail="Unable to complete the analysis.")


def _messages_from_checkpoint(checkpoint: dict) -> list[dict[str, str]]:
    """Extract human/AI messages from a LangGraph checkpoint."""
    messages = checkpoint.get("channel_values", {}).get("messages", [])
    return [
        {"role": message.type, "content": str(message.content)}
        for message in messages
        if message.type in ("human", "ai")
    ]


@app.get("/conversations")
def list_conversations() -> list[dict[str, str]]:
    """List saved threads, newest first, using the first question as the title."""
    try:
        # Each execution produces several checkpoints. Keep only the latest
        # checkpoint for each thread, while preserving newest-first order.
        seen = set()
        conversations = []
        for item in app.state.checkpointer.list(None):
            thread_id = item.config["configurable"]["thread_id"]
            if thread_id in seen:
                continue
            seen.add(thread_id)
            messages = _messages_from_checkpoint(item.checkpoint)
            first_question = next(
                (m["content"] for m in messages if m["role"] == "human"),
                None,
            )
            if first_question:
                conversations.append({
                    "thread_id": thread_id,
                    "title": first_question[:80],
                })
        return conversations
    except Exception:
        logger.exception("Could not list conversations")
        raise HTTPException(status_code=500, detail="Unable to load conversations.")


@app.get("/conversations/{thread_id}")
def get_conversation(thread_id: str) -> dict[str, Any]:
    """Retrieve a conversation's saved human and AI messages."""
    if not thread_id or len(thread_id) > 100:
        raise HTTPException(status_code=422, detail="Invalid conversation ID.")
    try:
        checkpoint = app.state.checkpointer.get_tuple(
            {"configurable": {"thread_id": thread_id}}
        )
        if checkpoint is None:
            raise HTTPException(status_code=404, detail="Conversation not found.")
        return {
            "thread_id": thread_id,
            "messages": _messages_from_checkpoint(checkpoint.checkpoint),
        }
    except HTTPException:
        raise
    except Exception:
        logger.exception("Could not retrieve conversation")
        raise HTTPException(status_code=500, detail="Unable to load conversation.")


@app.get("/overview")
def dashboard_overview():
    """Return live dashboard metrics from PostgreSQL without calling OpenAI."""
    return get_dashboard_overview()
