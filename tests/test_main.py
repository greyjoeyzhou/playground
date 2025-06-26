import pytest
from httpx import AsyncClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app, get_db
from app.models import Base


DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


import pytest_asyncio

app.dependency_overrides[get_db] = override_get_db


from httpx import ASGITransport

@pytest_asyncio.fixture(scope="module")
async def client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac


@pytest.mark.asyncio
async def test_create_todo(client: AsyncClient):
    response = await client.post("/todos/", json={"title": "Test Todo", "description": "Test Description"})
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Todo"
    assert data["description"] == "Test Description"
    assert "id" in data
    assert "completed" in data
    assert data["completed"] is False


@pytest.mark.asyncio
async def test_read_todos(client: AsyncClient):
    response = await client.post("/todos/", json={"title": "Test Todo 2", "description": "Test Description 2"})
    assert response.status_code == 200
    todo_id = response.json()["id"]

    response = await client.get("/todos/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert any(item["id"] == todo_id for item in data)


@pytest.mark.asyncio
async def test_read_todo(client: AsyncClient):
    response = await client.post("/todos/", json={"title": "Test Todo 3", "description": "Test Description 3"})
    assert response.status_code == 200
    todo_id = response.json()["id"]

    response = await client.get(f"/todos/{todo_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Todo 3"
    assert data["description"] == "Test Description 3"
    assert data["id"] == todo_id


@pytest.mark.asyncio
async def test_read_todo_not_found(client: AsyncClient):
    response = await client.get("/todos/999")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_todo(client: AsyncClient):
    response = await client.post("/todos/", json={"title": "Test Todo 4", "description": "Test Description 4"})
    assert response.status_code == 200
    todo_id = response.json()["id"]

    response = await client.put(f"/todos/{todo_id}", json={"title": "Updated Todo 4", "description": "Updated Description 4"})
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Todo 4"
    assert data["description"] == "Updated Description 4"
    assert data["id"] == todo_id


@pytest.mark.asyncio
async def test_update_todo_not_found(client: AsyncClient):
    response = await client.put("/todos/999", json={"title": "Updated Todo", "description": "Updated Description"})
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_todo(client: AsyncClient):
    response = await client.post("/todos/", json={"title": "Test Todo 5", "description": "Test Description 5"})
    assert response.status_code == 200
    todo_id = response.json()["id"]

    response = await client.delete(f"/todos/{todo_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == todo_id

    response = await client.get(f"/todos/{todo_id}")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_todo_not_found(client: AsyncClient):
    response = await client.delete("/todos/999")
    assert response.status_code == 404
