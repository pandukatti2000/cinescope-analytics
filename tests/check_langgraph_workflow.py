
"""
Test the complete LangGraph analytics workflow.
"""

from app.agents.graph import analytics_graph


def main() -> None:
    question = (
        "How many customers are registered "
        "in the movie rental database?"
    )

    print("QUESTION:")
    print(question)

    # Execute the complete LangGraph workflow.
    response = analytics_graph.invoke({
        "question": question
    })

    print("\nAI ANSWER:")
    print(response["answer"])

    print("\nDATABASE RESULTS:")
    for row in response["results"]:
        print(row)

    print("\nTOTAL ROWS:", response["row_count"])

    # Verify the database calculation.
    assert response["row_count"] == 1, (
        "Expected one aggregation result."
    )

    result = response["results"][0]

    assert len(result) == 1, (
        "Expected one customer-count column."
    )

    customer_count = next(iter(result.values()))

    assert customer_count == 599, (
        f"Expected 599 customers, got {customer_count}."
    )

    assert response["answer"].strip(), (
        "AI answer cannot be empty."
    )

    print("\nLangGraph workflow test: PASS")


if __name__ == "__main__":
    main()
