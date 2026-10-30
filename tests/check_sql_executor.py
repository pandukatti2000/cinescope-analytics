
"""
Test the SQL executor using a read-only query.
"""

from app.database.executor import execute_query


def main() -> None:
    query = """
    SELECT
        film_id,
        title,
        rental_rate
    FROM public.film
    ORDER BY film_id
    LIMIT 5
    """

    print("EXECUTING SQL:")
    print(query.strip())

    results = execute_query(query)

    print("\nQUERY RESULTS:")
    for row in results:
        print(row)

    print("\nTotal rows returned:", len(results))


if __name__ == "__main__":
    main()
