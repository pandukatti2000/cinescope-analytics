"""
CineScope Analytics
Professional Streamlit frontend for the Movie Rental AI Assistant.
"""

import pandas as pd
import requests
import streamlit as st
from frontend.charts import render_chart


API_URL = "http://127.0.0.1:8000/analyze"

OVERVIEW_URL = "http://127.0.0.1:8000/overview"
CONVERSATIONS_URL = "http://127.0.0.1:8000/conversations"


@st.cache_data(ttl=60)
def fetch_dashboard_overview():
    """
    Retrieve live KPI metrics from FastAPI.

    Cache results for 60 seconds to avoid unnecessary
    database queries on every Streamlit interaction.
    """
    response = requests.get(OVERVIEW_URL, timeout=10)
    response.raise_for_status()
    return response.json()

st.set_page_config(
    page_title="CineScope | Movie Rental Analytics",
    page_icon="C",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ---------------------------------------------------------
# PAGE STYLING
# ---------------------------------------------------------

st.markdown(
    """
    <style>
    .stApp {
        background: #0B1020;
        color: #E9EDF7;
    }

    .block-container {
        max-width: 1450px;
        padding-top: 2rem;
        padding-bottom: 4rem;
    }

    section[data-testid="stSidebar"] {
        background: #10182B;
        border-right: 1px solid #253047;
    }

    h1, h2, h3 {
        letter-spacing: -0.035em;
    }

    .sidebar-brand {
        font-size: 1.35rem;
        font-weight: 800;
        color: #F4F6FF;
        padding: 0.7rem 0 0.1rem;
    }

    .sidebar-subtitle {
        font-size: 0.78rem;
        color: #93A4C3;
        margin-bottom: 1.8rem;
    }

    .eyebrow {
        font-size: 0.76rem;
        font-weight: 700;
        letter-spacing: 0.13em;
        color: #A89CFF;
        text-transform: uppercase;
        margin-bottom: 0.6rem;
    }

    .hero {
        background: linear-gradient(
            115deg,
            #252052 0%,
            #192442 52%,
            #102B38 100%
        );
        border: 1px solid #3A426A;
        border-radius: 20px;
        padding: 2.2rem 2.4rem;
        margin-bottom: 1.7rem;
    }

    .hero-title {
        color: #FFFFFF;
        font-weight: 800;
        font-size: clamp(1.8rem, 3vw, 2.8rem);
        letter-spacing: -0.05em;
        line-height: 1.12;
        margin: 0.5rem 0 0.9rem;
    }

    .hero-description {
        color: #C0CBE2;
        font-size: 1rem;
        max-width: 650px;
        line-height: 1.7;
    }

    .metric-card {
        background: #151F34;
        border: 1px solid #2B3853;
        border-radius: 16px;
        padding: 1.3rem 1.4rem;
        min-height: 128px;
        margin-bottom: 1rem;
    }

    .metric-label {
        color: #9CABCA;
        font-size: 0.86rem;
        margin-bottom: 0.75rem;
    }

    .metric-value {
        color: #F6F8FF;
        font-size: clamp(1.4rem, 2vw, 2rem);
        font-weight: 800;
        letter-spacing: -0.04em;
        font-variant-numeric: tabular-nums;
    }

    .section-heading {
        font-size: 1.4rem;
        font-weight: 750;
        color: #F4F6FF;
        margin: 1.8rem 0 0.3rem;
    }

    .section-description {
        color: #9CABCA;
        font-size: 0.9rem;
        margin-bottom: 1.1rem;
    }

    .answer-label {
        color: #A89CFF;
        font-size: 0.8rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-top: 1rem;
    }

    .small-note {
        color: #8292B0;
        font-size: 0.8rem;
        line-height: 1.6;
    }

    div.stButton > button[kind="primary"],
    div.stFormSubmitButton > button[kind="primary"] {
        background: linear-gradient(90deg, #7667E9, #5D80E8);
        color: #FFFFFF;
        border: none;
        border-radius: 10px;
        font-weight: 700;
        min-height: 43px;
    }

    div.stButton > button {
        border-radius: 10px;
    }

    div[data-testid="stForm"] {
        background: #121C30;
        border: 1px solid #2C3B58;
        border-radius: 16px;
        padding: 1.2rem;
    }

    div[data-testid="stExpander"] {
        border: 1px solid #2C3B58;
        border-radius: 12px;
        background: #121C30;
    }

    div[data-testid="stDataFrame"] {
        border-radius: 12px;
        overflow: hidden;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# SESSION STATE
# ---------------------------------------------------------

if "question_input" not in st.session_state:
    st.session_state.question_input = ""

if "last_analysis" not in st.session_state:
    st.session_state.last_analysis = None

if "history" not in st.session_state:
    st.session_state.history = []

if "active_thread_id" not in st.session_state:
    st.session_state.active_thread_id = None

if "conversation_messages" not in st.session_state:
    st.session_state.conversation_messages = []


def select_question(question: str) -> None:
    """Populate the input with a suggested question."""
    st.session_state.question_input = question


def start_new_chat() -> None:
    """Start a fresh conversation without deleting stored checkpoints."""
    st.session_state.active_thread_id = None
    st.session_state.question_input = ""
    st.session_state.last_analysis = None
    st.session_state.conversation_messages = []
    st.session_state.conversation_error = None


def load_saved_conversation(thread_id: str) -> None:
    """Load messages for a persisted thread from FastAPI."""
    try:
        response = requests.get(f"{CONVERSATIONS_URL}/{thread_id}", timeout=15)
        response.raise_for_status()
        payload = response.json()
    except (requests.exceptions.RequestException, ValueError):
        st.session_state.conversation_error = "Unable to load this conversation."
        return

    st.session_state.active_thread_id = payload["thread_id"]
    st.session_state.conversation_messages = payload.get("messages", [])
    st.session_state.last_analysis = None
    st.session_state.question_input = ""
    st.session_state.conversation_error = None


def load_history(item: dict) -> None:
    """Restore a previous analysis without another API call."""
    st.session_state.question_input = item["question"]
    st.session_state.last_analysis = item["response"]
    st.session_state.active_thread_id = item["response"].get("thread_id")
    st.session_state.conversation_messages = []


# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------

with st.sidebar:
    st.markdown(
        '<div class="sidebar-brand">CineScope Analytics</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="sidebar-subtitle">'
        'Movie Rental Intelligence Platform'
        '</div>',
        unsafe_allow_html=True,
    )

    st.button(
        "New Chat",
        key="new_chat",
        use_container_width=True,
        type="primary",
        on_click=start_new_chat,
    )

    st.divider()

    st.markdown("### Saved Conversations")

    try:
        saved_response = requests.get(CONVERSATIONS_URL, timeout=10)
        saved_response.raise_for_status()
        saved_conversations = saved_response.json()
        if not isinstance(saved_conversations, list):
            raise ValueError("Unexpected conversations response")
    except (requests.exceptions.RequestException, ValueError):
        saved_conversations = []
        st.caption("Saved conversations are temporarily unavailable.")

    for saved in saved_conversations:
        saved_id = saved.get("thread_id")
        if not saved_id:
            continue
        title = saved.get("title") or "Untitled conversation"
        is_active = saved_id == st.session_state.active_thread_id
        st.button(
            ("• " if is_active else "") + title,
            key=f"saved_{saved_id}",
            use_container_width=True,
            on_click=load_saved_conversation,
            args=(saved_id,),
        )

    if not saved_conversations:
        st.caption("Your saved chats will appear here.")

    st.divider()

    st.markdown("### Explore your data")

    examples = [
        "Show the top 5 movies by total revenue.",
        "How many customers are registered?",
        "Who are the top 10 customers by total spending?",
        "Show the number of rentals by month.",
    ]

    for index, example in enumerate(examples):
        st.button(
            example,
            key=f"example_{index}",
            use_container_width=True,
            on_click=select_question,
            args=(example,),
        )

    st.divider()

    st.markdown("### Recent analyses")

    if st.session_state.history:
        for index, item in enumerate(
            reversed(st.session_state.history[-8:])
        ):
            st.button(
                item["question"],
                key=f"history_{index}",
                use_container_width=True,
                on_click=load_history,
                args=(item,),
            )
    else:
        st.caption("Your recent questions will appear here.")

    st.divider()

    st.markdown(
        '<div class="small-note">'
        'Powered by OpenAI, LangGraph, FastAPI '
        'and PostgreSQL.<br><br>'
        'Local development edition.'
        '</div>',
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------
# DASHBOARD HEADER
# ---------------------------------------------------------

st.markdown(
    """
    <div class="hero">
        <div class="eyebrow">AI-Powered Business Intelligence</div>
        <div class="hero-title">
            Your movie rental data,<br>explained.
        </div>
        <div class="hero-description">
            Explore customer behavior, movie performance,
            rental activity, and revenue using natural language.
            Ask a question and turn your database into insights.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# DATASET OVERVIEW
# These are verified reference values, not live API metrics.
# ---------------------------------------------------------

st.markdown(
    '<div class="section-heading">Dataset Overview</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="section-description">'
    'Live business metrics retrieved from PostgreSQL.'
    '</div>',
    unsafe_allow_html=True,
)


try:
    overview = fetch_dashboard_overview()
except requests.exceptions.RequestException:
    overview = None
    st.warning(
        "Live dashboard metrics are temporarily unavailable. "
        "Please check the FastAPI server."
    )

if overview is not None:
    metrics = [
        ("Total Revenue", f"{overview['total_revenue']:,.2f}"),
        ("Total Rentals", f"{overview['total_rentals']:,}"),
        ("Customers", f"{overview['total_customers']:,}"),
        ("Films", f"{overview['total_films']:,}"),
    ]
else:
    metrics = [
        ("Total Revenue", "Unavailable"),
        ("Total Rentals", "Unavailable"),
        ("Customers", "Unavailable"),
        ("Films", "Unavailable"),
    ]


metric_columns = st.columns(4, gap="medium")

for column, (label, value) in zip(metric_columns, metrics):
    with column:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">{label}</div>
                <div class="metric-value">{value}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


# ---------------------------------------------------------
# AI QUESTION INTERFACE
# ---------------------------------------------------------

st.markdown(
    '<div class="section-heading">Ask CineScope</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="section-description">'
    'Ask a business question in plain English. '
    'No SQL knowledge required.'
    '</div>',
    unsafe_allow_html=True,
)

with st.form("analytics_form"):
    question = st.text_area(
        "Your business question",
        key="question_input",
        placeholder=(
            "Example: Which 5 movies generated "
            "the highest revenue?"
        ),
        height=95,
    )

    submitted = st.form_submit_button(
        "Analyze Question",
        type="primary",
        use_container_width=True,
    )


# ---------------------------------------------------------
# FASTAPI REQUEST
# ---------------------------------------------------------

if submitted:
    clean_question = question.strip()

    if not clean_question:
        st.warning("Please enter a business question.")

    else:
        with st.spinner("Analyzing your movie rental data..."):
            try:
                response = requests.post(
                    API_URL,
                    json={
                        "question": clean_question,
                        "thread_id": st.session_state.active_thread_id,
                    },
                    timeout=90,
                )

                response.raise_for_status()
                result = response.json()

                st.session_state.active_thread_id = result["thread_id"]
                st.session_state.last_analysis = result
                st.session_state.conversation_messages.extend([
                    {"role": "human", "content": clean_question},
                    {"role": "ai", "content": result["answer"]},
                ])

                st.session_state.history.append(
                    {
                        "question": clean_question,
                        "response": result,
                    }
                )

                # Keep only the most recent 10 analyses.
                st.session_state.history = (
                    st.session_state.history[-10:]
                )

            except requests.exceptions.Timeout:
                st.session_state.last_analysis = None
                st.error(
                    "The analysis took too long. "
                    "Please try a simpler question."
                )

            except requests.exceptions.HTTPError as exc:
                st.session_state.last_analysis = None
                status_code = exc.response.status_code

                if status_code == 422:
                    st.error(
                        "The question could not be analyzed. "
                        "Try rephrasing it."
                    )
                else:
                    st.error(
                        "The backend could not complete "
                        "this analysis."
                    )

            except requests.exceptions.RequestException:
                st.session_state.last_analysis = None
                st.error(
                    "Unable to connect to the backend. "
                    "Check that FastAPI is running "
                    "on port 8000."
                )


# ---------------------------------------------------------
# DISPLAY RESULTS
# ---------------------------------------------------------

if st.session_state.get("conversation_error"):
    st.error(st.session_state.conversation_error)

if st.session_state.conversation_messages:
    st.divider()
    st.markdown(
        '<div class="section-heading">Conversation History</div>',
        unsafe_allow_html=True,
    )
    for message in st.session_state.conversation_messages:
        role = "user" if message.get("role") in ("human", "user") else "assistant"
        with st.chat_message(role):
            st.markdown(message.get("content", ""))

data = st.session_state.last_analysis

if data:
    st.divider()

    st.markdown(
        '<div class="section-heading">Your Analysis</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-description">'
        'AI explanation and supporting database results.'
        '</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="answer-label">AI Answer</div>',
        unsafe_allow_html=True,
    )

    st.markdown(data["answer"])

    # Automatically display an interactive chart
    # when the database results support one.
    if data["results"]:
        render_chart(data["results"])

    st.markdown("### Detailed Results")

    if data["results"]:
        dataframe = pd.DataFrame(data["results"])

        st.dataframe(
            dataframe,
            use_container_width=True,
            hide_index=True,
        )

        csv_data = dataframe.to_csv(index=False)

        st.download_button(
            label="Download Results as CSV",
            data=csv_data,
            file_name="cinescope_analysis.csv",
            mime="text/csv",
        )

    else:
        st.info("No matching records were found.")

    st.caption(
        f"Rows returned: {data['row_count']}"
    )

    # Technical details stay hidden by default.
    with st.expander("Show Analysis", expanded=False):
        st.markdown("**Generated SQL**")

        st.code(
            data["sql"],
            language="sql",
        )

        st.caption(
            "This SQL was generated by the AI and "
            "validated before database execution."
        )


# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------

st.divider()

st.markdown(
    '<div class="small-note">'
    'CineScope Analytics | Movie Rental AI Assistant<br>'
    'AI-generated insights should be reviewed '
    'against the underlying data.'
    '</div>',
    unsafe_allow_html=True,
)
