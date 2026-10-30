
"""
Test movie revenue analysis using the SQL executor.
"""

from app.database.executor import execute_query


def main() -> None:
    query = """
    SELECT
        f.film_id,
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
    ORDER BY total_revenue DESC, f.film_id
    LIMIT 5
    """

    print("TOP 5 MOVIES BY REVENUE")
    print("-" * 50)

    results = execute_query(query)

    for index, row in enumerate(results, start=1):
        print(
            f"{index}. {row['title']} "
            f"- Revenue: {row['total_revenue']}"
        )

    print("-" * 50)
    print("Total movies returned:", len(results))

    assert len(results) == 5, "Expected exactly 5 movies."

    print("Revenue query test: PASS")


if __name__ == "__main__":
    main()
