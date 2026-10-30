
"""
Test the end-to-end AI analytics service.
"""

from app.services.analytics import analyze_question


def main() -> None:
    question = "Show the top 5 movies by total revenue."

    print("QUESTION:")
    print(question)

    response = analyze_question(question)

    print("\nGENERATED SQL:")
    print(response["sql"])

    print("\nQUERY RESULTS:")
    for row in response["results"]:
        print(row)

    print("\nTOTAL ROWS:", response["row_count"])

    assert response["row_count"] == 5, (
        "Expected exactly 5 movie records."
    )

    print("\nEnd-to-end analytics test: PASS")


if __name__ == "__main__":
    main()
