
"""
Interactive Plotly visualizations for CineScope Analytics.

Automatically chooses charts based on SQL result data.
"""

import pandas as pd
import plotly.express as px
import streamlit as st


CHART_COLORS = [
    "#8B7CF6",
    "#5B9CF6",
    "#37C9B5",
    "#F5B971",
    "#EF7DA8",
]



def prepare_dataframe(results: list[dict]) -> pd.DataFrame:
    """
    Convert database results into a DataFrame.

    Handle numeric strings from JSON, including Pandas StringDtype.
    """
    dataframe = pd.DataFrame(results)

    if dataframe.empty:
        return dataframe

    for column in dataframe.columns:
        # Skip columns that are already numeric.
        if pd.api.types.is_numeric_dtype(dataframe[column]):
            continue

        # Only attempt conversion for text columns.
        if not (
            pd.api.types.is_string_dtype(dataframe[column])
            or dataframe[column].dtype == "object"
        ):
            continue

        converted = pd.to_numeric(
            dataframe[column],
            errors="coerce",
        )

        # Convert only when every non-null value is numeric.
        original_non_null = dataframe[column].notna()
        converted_non_null = converted.notna()

        if (
            original_non_null.any()
            and converted_non_null.sum()
            == original_non_null.sum()
        ):
            dataframe[column] = converted

    return dataframe



def detect_chart_type(
    dataframe: pd.DataFrame,
) -> tuple[str | None, str | None, str | None]:
    """
    Determine chart type, category column, and metric column.

    Returns:
        (chart_type, category_column, metric_column)
    """
    if dataframe.empty:
        return None, None, None

    if len(dataframe) == 1:
        return None, None, None

    numeric_columns = dataframe.select_dtypes(
        include="number"
    ).columns.tolist()

    category_columns = dataframe.select_dtypes(
        exclude="number"
    ).columns.tolist()

    # Prefer business metrics over numeric identifiers.
    metric_keywords = [
        "revenue",
        "spending",
        "amount",
        "count",
        "total",
        "rentals",
        "payments",
        "average",
        "avg",
        "duration",
    ]

    metric_columns = [
        column
        for column in numeric_columns
        if any(
            keyword in column.lower()
            for keyword in metric_keywords
        )
        and not column.lower().endswith("_id")
    ]

    if not metric_columns:
        return None, None, None

    metric_column = metric_columns[0]

    # Prefer readable categories such as title, name, or month.
    category_keywords = [
        "title",
        "name",
        "category",
        "month",
        "year",
        "date",
        "period",
        "label",
    ]

    preferred_categories = [
        column
        for column in category_columns
        if any(
            keyword in column.lower()
            for keyword in category_keywords
        )
    ]

    if preferred_categories:
        category_column = preferred_categories[0]
    elif category_columns:
        category_column = category_columns[0]
    else:
        return None, None, None

    column_name = category_column.lower()

    if any(
        keyword in column_name
        for keyword in ["month", "date", "period", "year"]
    ):
        return "line", category_column, metric_column

    return "bar", category_column, metric_column


def render_chart(results: list[dict]) -> None:
    """
    Render an appropriate interactive Plotly chart.

    Displays nothing if the data is not suitable for a chart.
    """
    dataframe = prepare_dataframe(results)

    chart_type, category_column, metric_column = (
        detect_chart_type(dataframe)
    )

    if chart_type is None:
        return

    st.markdown("### Interactive Visualization")

    chart_data = dataframe.copy()

    if chart_type == "bar":
        # Preserve the original SQL result ordering.
        chart_data[category_column] = (
            chart_data[category_column].astype(str)
        )

        figure = px.bar(
            chart_data,
            x=metric_column,
            y=category_column,
            orientation="h",
            color=metric_column,
            color_continuous_scale=[
                "#5046A0",
                "#8B7CF6",
                "#B9B0FF",
            ],
            labels={
                metric_column: (
                    metric_column.replace("_", " ").title()
                ),
                category_column: "",
            },
        )

        figure.update_layout(
            yaxis={
                "categoryorder": "array",
                "categoryarray": (
                    chart_data[category_column]
                    .tolist()[::-1]
                ),
            },
            coloraxis_showscale=False,
        )

    else:
        figure = px.line(
            chart_data,
            x=category_column,
            y=metric_column,
            markers=True,
            color_discrete_sequence=CHART_COLORS,
            labels={
                metric_column: (
                    metric_column.replace("_", " ").title()
                ),
                category_column: (
                    category_column.replace("_", " ").title()
                ),
            },
        )

    figure.update_layout(
        template="plotly_dark",
        paper_bgcolor="#0B1020",
        plot_bgcolor="#0B1020",
        font=dict(
            family="Arial",
            color="#DCE5F5",
            size=13,
        ),
        title=None,
        height=max(
            380,
            min(650, len(chart_data) * 38 + 160),
        ),
        margin=dict(
            l=30,
            r=30,
            t=25,
            b=35,
        ),
        hovermode="closest",
    )

    figure.update_xaxes(
        showgrid=True,
        gridcolor="#27344C",
        zeroline=False,
    )

    figure.update_yaxes(
        showgrid=False,
        zeroline=False,
    )

    st.plotly_chart(
        figure,
        use_container_width=True,
        config={
            "displaylogo": False,
            "scrollZoom": False,
            "toImageButtonOptions": {
                "format": "png",
                "filename": "cinescope_chart",
                "scale": 2,
            },
        },
    )
