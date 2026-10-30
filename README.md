# CineScope Analytics

### AI-Powered Movie Rental Business Intelligence Assistant

CineScope Analytics is a full-stack, AI-powered analytics application that allows users to explore a PostgreSQL movie rental database using natural-language questions.

Instead of writing SQL manually, users can ask business questions about revenue, customers, films, and rental activity. The application generates PostgreSQL queries, validates and executes them, and presents the results as natural-language explanations, interactive charts, and downloadable tables.

The application combines **LangGraph, LangChain, OpenAI, FastAPI, PostgreSQL, and Streamlit**.

> **Project status:** Completed local-development portfolio project. The application runs locally and requires PostgreSQL and an OpenAI API key.

## Key Features

- **Natural-language analytics:** Ask business questions without writing SQL.

- **AI-generated SQL:** Convert questions into PostgreSQL SELECT queries using an OpenAI language model.

- **LangGraph workflow:** Coordinate SQL generation, execution, and answer generation through a three-node graph.

- **SQL safety controls:** Validate queries using SQLGlot, restrict SQL operations, and execute within read-only PostgreSQL transactions.

- **Persistent conversation memory:** Store conversation checkpoints in a separate PostgreSQL database.

- **Context-aware follow-ups:** Ask questions that reference previous conversation turns.

- **Saved conversations:** Resume previously saved conversations from the Streamlit sidebar.

- **Business KPI dashboard:** Display revenue, rentals, customers, and films using live PostgreSQL data.

- **Interactive visualizations:** Automatically generate suitable Plotly bar and line charts.

- **Transparent results:** Inspect generated SQL, view detailed tables, and export results as CSV.

- **REST API:** Access analytics and conversation history through FastAPI.

## Dataset Overview

The project uses a PostgreSQL implementation of the Sakila movie rental dataset.

| Metric | Value |

|---|---:|

| Customers | 599 |

| Films | 1,000 |

| Rentals | 16,044 |

| Payments | 16,044 |

| Total payment revenue | 67,406.56 |

| Database tables | 16 |

Revenue is calculated from `payment.amount`, not from film rental rates. The dataset does not establish a currency, so revenue is displayed without a currency symbol.

The database contains information about films, actors, categories, inventory, rentals, customers, payments, stores, and staff.

## Technology Stack

| Layer | Technology |

|---|---|

| Frontend | Streamlit |

| Visualizations | Plotly, Pandas |

| Backend API | FastAPI, Uvicorn |

| AI model | OpenAI GPT-4.1-mini |

| LLM integration | LangChain |

| Agent workflow | LangGraph |

| SQL generation | LangChain + OpenAI |

| SQL validation | SQLGlot |

| Analytics database | PostgreSQL |

| Database access | SQLAlchemy, Psycopg2 |

| Conversation memory | LangGraph PostgreSQL Checkpointer, Psycopg |

| Configuration | Pydantic Settings, python-dotenv |

| Development and diagnostics | Python test scripts, LangGraph Studio, LangSmith |

## System Architecture

```text

                  User

                   |

                   v

          Streamlit Frontend

          - KPI dashboard

          - Analytics questions

          - Saved conversations

          - Charts and CSV export

                   |

                   v

              FastAPI

                   |

                   v

           LangGraph Workflow

                   |

                   v

            Generate SQL

          - Database schema

          - Business rules

          - Conversation context

          - OpenAI language model

                   |

                   v

         Validate and Execute

          - SQLGlot validation

          - SELECT-only queries

          - Table restrictions

          - Read-only transaction

          - Query timeout

          - Result row limit

                   |

                   v

         PostgreSQL Analytics DB

                   |

                   v

           Generate AI Answer

                   |

                   v

             API Response

                   |

                   v

          Streamlit Results

          - Explanation

          - SQL query

          - Data table

          - Interactive chart

          - CSV download

      Separate PostgreSQL Database

          LangGraph Checkpoints

          - Conversation history

          - Thread persistence

          - Follow-up context

```

## How the AI Workflow Works

The LangGraph workflow contains three sequential nodes:

1. **Generate SQL:** The application provides the language model with PostgreSQL schema metadata, business rules, the current question, and recent conversation context. The model generates a SQL query.

2. **Execute SQL:** The generated query is validated using SQLGlot and executed against the PostgreSQL analytics database with read-only transaction protections.

3. **Generate Answer:** The language model receives the original question, SQL query, and database results, then produces a natural-language explanation.

The workflow uses LangGraph's shared state to pass data between nodes.

For conversations, a `thread_id` identifies the active thread. PostgreSQL checkpoints allow the application to recover saved messages and continue follow-up questions after a restart.

## SQL Validation and Data Safety

AI-generated SQL is treated as untrusted input.

The application implements several safeguards:

- Accepts a single SELECT statement.

- Rejects database-modifying SQL operations.

- Rejects row-locking clauses.

- Restricts access to permitted tables in the public schema.

- Uses an allowlist of supported SQL functions.

- Applies a maximum result limit of 100 rows.

- Executes queries in PostgreSQL read-only transactions.

- Applies a 5-second database statement timeout.

- Rolls back the transaction after execution.

- Uses a dedicated read-only analytics database account.

These controls provide multiple layers of protection, but they are not a substitute for database-level permissions and a comprehensive production security review.

## Project Structure

```text

CineScope-Analytics/

|

|-- app/

|   |-- agents/

|   |   |-- graph.py

|   |   |-- nodes.py

|   |   `-- state.py

|   |

|   |-- api/

|   |   `-- main.py

|   |

|   |-- core/

|   |   |-- business_rules.py

|   |   `-- config.py

|   |

|   |-- database/

|   |   |-- connection.py

|   |   |-- executor.py

|   |   |-- memory.py

|   |   |-- metadata.py

|   |   `-- validator.py

|   |

|   |-- llm/

|   |   |-- answer_generator.py

|   |   |-- client.py

|   |   |-- prompts.py

|   |   `-- sql_generator.py

|   |

|   `-- services/

|       |-- analytics.py

|       `-- overview.py

|

|-- frontend/

|   |-- charts.py

|   `-- streamlit_app.py

|

|-- Data/

|   `-- SQL/

|       |-- sakila_schema.sql

|       `-- sakila_data.sql

|

|-- tests/

|   `-- check_*.py

|

|-- setup_memory_db.py

|-- langgraph.json

|-- requirements.txt

|-- .env.example

|-- .gitignore

`-- README.md

```

## Getting Started

### Prerequisites

- Python 3.13

- PostgreSQL (developed using PostgreSQL 18)

- An OpenAI API key

- Git

- Windows Command Prompt or another compatible terminal

### 1. Clone the Repository

```bash

git clone https://github.com/pandukatti2000/cinescope-analytics.git

cd cinescope-analytics

```

### 2. Create a Python Virtual Environment

On Windows:

```cmd

python -m venv .venv

.venv\Scripts\activate

```

Install dependencies:

```cmd

python -m pip install -r requirements.txt

```

### 3. Configure PostgreSQL

The application uses two PostgreSQL databases:

| Database | Purpose |

|---|---|

| `movie_rental_db` | Stores movie rental business data |

| `cinescope_memory_db` | Stores LangGraph conversation checkpoints |

Create both databases using PostgreSQL administration tools or an administrator account.

The analytics database should be accessed through a dedicated read-only role, such as `movie_rental_reader`.

The conversation memory database requires a separate account, such as `cinescope_memory_user`, with permissions to create and maintain LangGraph checkpoint tables.

The repository includes:

```text

Data/SQL/sakila_schema.sql

Data/SQL/sakila_data.sql

```

These contain the database schema and data used by the project.

The SQL files should be reviewed for PostgreSQL compatibility and executed in the correct order: schema first, then data. A clean-database import has not yet been independently verified.

After importing the dataset, grant the analytics account only the database, schema, and table permissions required for read-only access.

### 4. Configure Environment Variables

Copy the example environment file:

```cmd

copy .env.example .env

```

Edit `.env` and provide the credentials for both PostgreSQL databases and your OpenAI API key.

The configuration includes:

```dotenv

DB_HOST=localhost

DB_PORT=5432

DB_NAME=movie_rental_db

DB_USER=movie_rental_reader

DB_PASSWORD=your_analytics_database_password

MEMORY_DB_HOST=localhost

MEMORY_DB_PORT=5432

MEMORY_DB_NAME=cinescope_memory_db

MEMORY_DB_USER=cinescope_memory_user

MEMORY_DB_PASSWORD=your_memory_database_password

OPENAI_API_KEY=your_openai_api_key_here

OPENAI_MODEL=gpt-4.1-mini

APP_NAME="Movie Rental AI Analytics"

APP_ENV=development

```

**Never commit `.env` or real credentials to GitHub.**

### 5. Initialize Conversation Memory

Run this command once after configuring the memory database:

```cmd

python setup_memory_db.py

```

The script initializes the PostgreSQL checkpoint tables required by LangGraph.

Expected success message:

```text

Checkpoint setup: SUCCESS

```

### 6. Start the FastAPI Backend

From the project root, run:

```cmd

python -m uvicorn app.api.main:app --reload --host 127.0.0.1 --port 8000 --env-file .env

```

The API will be available at:

```text

http://127.0.0.1:8000

```

Interactive API documentation:

```text

http://127.0.0.1:8000/docs

```

Health endpoint:

```text

http://127.0.0.1:8000/health

```

### 7. Start the Streamlit Frontend

Open a second terminal, activate the same virtual environment, and run:

```cmd

python -m streamlit run frontend\streamlit_app.py

```

Streamlit will display the local application URL, normally:

```text

http://localhost:8501

```

Open the URL in your browser to use CineScope Analytics.

## Example Business Questions

Try asking CineScope:

- Show the top 5 movies by total revenue.

- How many customers are registered?

- Who are the top 10 customers by total spending?

- Show the number of rentals by month.

- Which movie categories generate the most revenue?

- Which films are rented most frequently?

- How many rentals have not been returned?

- What is the total revenue generated by the rental business?

You can also ask follow-up questions in the same conversation, such as:

```text

Question: Show the top 5 movies by total revenue.

Follow-up: Which of these movies has the highest rental count?

```

Follow-up questions use saved conversation context to interpret references to earlier questions.

## REST API

The FastAPI backend provides five endpoints.

| Method | Endpoint | Description |

|---|---|---|

| GET | `/health` | Check API health |

| POST | `/analyze` | Analyze a natural-language question |

| GET | `/overview` | Retrieve live dashboard metrics |

| GET | `/conversations` | List saved conversation threads |

| GET | `/conversations/{thread_id}` | Retrieve saved messages for a thread |

### Analyze a Question

**Request**

```http

POST /analyze

Content-Type: application/json

```

```json

{

  "question": "How many customers are registered?",

  "thread_id": null

}

```

**Example response structure**

```json

{

  "question": "How many customers are registered?",

  "answer": "There are 599 registered customers.",

  "results": [

    {

      "total_customers": 599

    }

  ],

  "row_count": 1,

  "sql": "SELECT COUNT(*) AS total_customers FROM public.customer LIMIT 100",

  "thread_id": "<generated-conversation-uuid>"

}

```

The exact generated SQL and answer may vary between model calls.

To continue an existing conversation, send the returned `thread_id` in the next `/analyze` request.

### Dashboard Overview

```http

GET /overview

```

Returns the total revenue, rentals, customers, and films calculated directly from PostgreSQL.

### Saved Conversations

```http

GET /conversations

```

Returns saved conversation identifiers and titles.

```http

GET /conversations/{thread_id}

```

Returns the saved human and AI messages for the requested conversation.

## Visualizations and Reporting

CineScope uses Pandas and Plotly to visualize suitable query results.

The visualization component:

- Converts SQL result records into a DataFrame.

- Identifies numeric business metrics.

- Selects a category or time-based dimension.

- Displays horizontal bar charts for comparisons.

- Displays line charts for time-based trends.

- Preserves SQL result ordering for ranked comparisons.

Users can also inspect the underlying results in a table, download CSV files, and expand the generated SQL for transparency.

Not every query result requires a chart. Single-value metrics and unsuitable result structures are displayed without one.

## Testing and Validation

The `tests/` directory contains executable Python diagnostic scripts covering:

- OpenAI connectivity

- SQL generation

- SQL validation

- SQL function restrictions

- Table and schema restrictions

- Query result limits

- SQL execution

- Read-only PostgreSQL transactions

- Business metric calculations

- Revenue queries

- AI answer generation

- End-to-end analytics

- LangGraph workflow execution

For example, from the project root:

```cmd

python -m tests.check_sql_validator

```

```cmd

python -m tests.check_sql_limits

```

```cmd

python -m tests.check_langgraph_workflow

```

Some tests require a running PostgreSQL database, and AI integration tests require a valid OpenAI API key.

These are primarily standalone diagnostic scripts rather than a fully automated pytest test suite.

## LangGraph Development Tools

The repository includes `langgraph.json`, which defines the analytics graph for LangGraph development tooling.

With a compatible LangGraph CLI installed, the graph can be inspected using the local development server:

```cmd

langgraph dev --port 2024

```

This is an optional development workflow and is not required to run the FastAPI and Streamlit application.

LangSmith can also be configured separately for tracing LangChain and LangGraph model interactions.

## Business Logic and Analytical Definitions

The application includes explicit business rules to improve SQL generation accuracy.

Examples include:

- **Revenue:** Sum of `payment.amount`.

- **Rental count:** Count of `rental.rental_id`.

- **Customer spending:** Sum of payment amounts grouped by customer.

- **Film revenue:** Sum of payments linked through rental, inventory, and film.

- **Film popularity:** Number of rentals associated with each film.

- **Unreturned rentals:** Rentals with a NULL `return_date`.

- **Rental trends:** Based on `rental.rental_date`.

- **Revenue trends:** Based on `payment.payment_date`.

These rules help the language model generate queries that align with the dataset's business meaning.

## Limitations

- The application is designed for local development, not public production deployment.

- An OpenAI API key is required for AI-powered questions.

- Generated answers depend on the quality of the model-generated SQL and underlying data.

- SQL validation is a defense-in-depth measure, not a complete security boundary.

- Results are limited to 100 rows per query.

- PostgreSQL must be configured and available locally.

- Saved conversations persist in the configured memory database.

- The bundled SQL import process has not yet been independently verified on a clean PostgreSQL installation.

## Project Purpose

CineScope Analytics was developed as a portfolio project to demonstrate practical skills in:

- Python backend development

- REST API design

- PostgreSQL and SQL analytics

- LLM application development

- LangChain and LangGraph workflows

- Natural-language-to-SQL systems

- Database query validation

- Stateful AI conversations

- Interactive data visualization

- End-to-end application integration

The project demonstrates how AI can provide a natural-language interface to structured business data while retaining visibility into the generated SQL and supporting results.

---

**CineScope Analytics — Ask questions. Explore data. Understand your business.**
