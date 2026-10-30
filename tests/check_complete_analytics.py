
"""
Test the complete AI analytics pipeline.

Question -> SQL -> Database -> Natural-language answer
"""

from app.services.analytics import analyze_question


def main() -> None:
    question = "Show the top 5 movies by total revenue."

    print("QUESTION:")
    print(question)

    response = analyze_question(question)

    print("\nAI ANSWER:")
    print(response["answer"])

    print("\nDATABASE RESULTS:")
    for row in response["results"]:
        print(row)

    print("\nTOTAL ROWS:", response["row_count"])

    assert response["answer"].strip(), "AI answer is empty."
    assert response["row_count"] == 5, "Expected 5 movies."

    expected_titles = [
        "TELEGRAPH VOYAGE",
        "WIFE TURN",
        "ZORRO ARK",
        "GOODFELLAS SALUTE",
        "SATURDAY LAMBS",
    ]

    actual_titles = [
        row["title"] for row in response["results"]
    ]

    assert actual_titles == expected_titles, (
        "Movie rankings do not match verified results."
    )

    assert response["sql"].strip(), "Generated SQL is empty."

    print("\nComplete analytics pipeline: PASS")


if __name__ == "__main__":
    main()
