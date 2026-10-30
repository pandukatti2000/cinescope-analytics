
"""
Retrieve live overview metrics for the CineScope dashboard.
"""

from decimal import Decimal

from app.database.executor import execute_query


def get_dashboard_overview() -> dict:
    """
    Return the main movie rental business metrics.

    Each metric uses a predefined, validated SELECT query.
    """
    revenue = execute_query(
        "SELECT SUM(amount) AS total_revenue FROM public.payment"
    )

    rentals = execute_query(
        "SELECT COUNT(*) AS total_rentals FROM public.rental"
    )

    customers = execute_query(
        "SELECT COUNT(*) AS total_customers FROM public.customer"
    )

    films = execute_query(
        "SELECT COUNT(*) AS total_films FROM public.film"
    )

    return {
        "total_revenue": float(
            revenue[0]["total_revenue"] or Decimal("0")
        ),
        "total_rentals": rentals[0]["total_rentals"],
        "total_customers": customers[0]["total_customers"],
        "total_films": films[0]["total_films"],
    }
