
"""
Business definitions for the Movie Rental AI Analytics Assistant.

These rules guide SQL generation and analytical interpretation.
"""

BUSINESS_RULES = {
    "revenue": (
        "Revenue means the sum of payment.amount from public.payment. "
        "Do not calculate revenue using film.rental_rate. "
        "The database does not establish a currency."
    ),
    "rental_count": (
        "Rental count means COUNT(rental.rental_id). "
        "Each rental represents one rental transaction."
    ),
    "customer_spending": (
        "Customer spending means SUM(payment.amount), grouped by "
        "customer.customer_id. Join customer to payment using customer_id."
    ),
    "film_revenue": (
        "Film revenue means SUM(payment.amount), grouped by film.film_id. "
        "Use the join path: payment -> rental -> inventory -> film."
    ),
    "film_popularity": (
        "Film popularity by rentals means COUNT(rental.rental_id), "
        "grouped by film.film_id. "
        "Use the join path: rental -> inventory -> film."
    ),
    "unreturned_rentals": (
        "An unreturned rental is a rental where return_date IS NULL. "
        "Do not automatically describe these historical records as "
        "currently overdue."
    ),
    "date_filtering": (
        "Use rental.rental_date for rental activity trends. "
        "Use payment.payment_date for revenue trends. "
        "Do not use film.release_year to determine rental dates."
    ),
    "payment_relationship": (
        "In the current dataset, every rental has exactly one payment. "
        "This was verified against the database."
    ),
}


def get_business_rules() -> str:
    """Return business rules formatted for an LLM prompt."""
    lines = ["BUSINESS DEFINITIONS:"]

    for name, definition in BUSINESS_RULES.items():
        readable_name = name.replace("_", " ").title()
        lines.append(f"- {readable_name}: {definition}")

    return "\n".join(lines)
