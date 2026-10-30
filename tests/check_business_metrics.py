
from sqlalchemy import text

from app.database.connection import get_engine


QUERY = """
SELECT
    (SELECT COUNT(*) FROM public.customer) AS total_customers,
    (SELECT COUNT(*) FROM public.film) AS total_films,
    (SELECT COUNT(*) FROM public.inventory) AS inventory_copies,
    (SELECT COUNT(*) FROM public.rental) AS total_rentals,
    (SELECT COUNT(*) FROM public.payment) AS total_payments,
    (SELECT COALESCE(SUM(amount), 0) FROM public.payment)
        AS total_payment_amount,
    (SELECT COUNT(*) FROM public.rental WHERE return_date IS NULL)
        AS unreturned_rentals,
    (SELECT COUNT(*) FROM public.payment WHERE rental_id IS NULL)
        AS payments_without_rental,
    (
        SELECT COUNT(*)
        FROM (
            SELECT rental_id
            FROM public.payment
            WHERE rental_id IS NOT NULL
            GROUP BY rental_id
            HAVING COUNT(*) > 1
        ) AS repeated
    ) AS rentals_with_multiple_payments
"""


def main() -> None:
    with get_engine().connect() as connection:
        result = connection.execute(text(QUERY)).mappings().one()

    print("MOVIE RENTAL BUSINESS METRICS")
    print("-" * 40)

    for metric, value in result.items():
        print(f"{metric}: {value}")


if __name__ == "__main__":
    main()
