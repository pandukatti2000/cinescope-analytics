
"""
Test natural-language answer generation using verified results.
"""

from decimal import Decimal

from app.llm.answer_generator import generate_answer


def main() -> None:
    question = "Show the top 5 movies by total revenue."

    sql_query = """
    SELECT
        f.title,
        SUM(p.amount) AS total_revenue
    FROM public.film AS f
    JOIN public.inventory AS i
        ON f.film_id = i.film_id
    JOIN public.rental AS r
        ON i.inventory_id = r.inventory_id
    JOIN public.payment AS p
        ON r.rental_id = p.rental_id
    GROUP BY f.film_id, f.title
    ORDER BY total_revenue DESC
    LIMIT 5
    """

    results = [
        {
            "title": "TELEGRAPH VOYAGE",
            "total_revenue": Decimal("231.73"),
        },
        {
            "title": "WIFE TURN",
            "total_revenue": Decimal("223.69"),
        },
        {
            "title": "ZORRO ARK",
            "total_revenue": Decimal("214.69"),
        },
        {
            "title": "GOODFELLAS SALUTE",
            "total_revenue": Decimal("209.69"),
        },
        {
            "title": "SATURDAY LAMBS",
            "total_revenue": Decimal("204.72"),
        },
    ]

    print("QUESTION:")
    print(question)

    answer = generate_answer(question, sql_query, results)

    print("\nAI-GENERATED ANSWER:")
    print(answer)

    assert answer.strip(), "AI returned an empty answer."

    print("\nAnswer generator test: PASS")


if __name__ == "__main__":
    main()
