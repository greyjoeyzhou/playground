# TODO List FastAPI App

This is a sample TODO list application built with FastAPI, SQLAlchemy, and Alembic.

## Project Structure

- `app/`: Contains the main application code.
  - `main.py`: FastAPI application and API endpoints.
  - `models.py`: SQLAlchemy database models.
  - `schemas.py`: Pydantic schemas for request/response validation.
  - `crud.py`: CRUD operations for interacting with the database.
  - `database.py`: Database connection and session management.
  - `__init__.py`: Makes the `app` directory a Python package.
- `alembic/`: Contains Alembic migration scripts and configuration.
  - `versions/`: Directory for individual migration scripts.
  - `env.py`: Alembic environment configuration.
- `tests/`: Contains test files.
  - `test_main.py`: Pytest tests for the API endpoints.
  - `__init__.py`: Makes the `tests` directory a Python package.
- `alembic.ini`: Alembic configuration file.
- `requirements.txt`: Project dependencies.
- `README.md`: This file.

## Setup and Installation

1.  **Clone the repository (if applicable).**
2.  **Create and activate a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Apply database migrations:**
    The application uses a SQLite database (`test.db`) by default. Alembic will create this file and the necessary tables.
    ```bash
    alembic upgrade head
    ```

## Running the Application

To run the FastAPI application locally, use Uvicorn:

```bash
uvicorn app.main:app --reload
```

The application will be available at `http://127.0.0.1:8000`. You can access the API documentation (Swagger UI) at `http://127.0.0.1:8000/docs`.

## Running Tests

To run the tests, use Pytest:

```bash
pytest
```

This will discover and run all tests in the `tests/` directory.
The tests use an in-memory SQLite database, so they won't affect your `test.db` file.

## Alembic Migrations

When you make changes to the SQLAlchemy models in `app/models.py`, you'll need to create a new database migration:

1.  **Generate a new revision:**
    ```bash
    alembic revision -m "your_migration_message"
    ```
    This will create a new migration script in `alembic/versions/`.
2.  **Edit the migration script:**
    Open the newly generated script and implement the `upgrade()` and `downgrade()` functions to reflect your model changes (Alembic often autogenerates most of this for you if `target_metadata` is set up correctly in `alembic/env.py`).
3.  **Apply the migration:**
    ```bash
    alembic upgrade head
    ```

To downgrade (revert) a migration:

```bash
alembic downgrade -1  # Downgrade by one revision
alembic downgrade base # Downgrade to the initial empty state
```
