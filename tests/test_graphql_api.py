import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


# ===========================
# Query テスト
# ===========================
def test_query_users():
    query = """
    {
        users {
            id
            name
            age
        }
    }
    """
    response = client.post("/graphql", json={"query": query})
    data = response.json()["data"]["users"]

    assert response.status_code == 200
    assert isinstance(data, list)
    assert "name" in data[0]


# ===========================
# Mutation: createUser
# ===========================
def test_create_user():
    mutation = """
    mutation {
        createUser(input: {name: "Eve", age: 32}) {
            id
            name
            age
        }
    }
    """
    response = client.post("/graphql", json={"query": mutation})
    result = response.json()["data"]["createUser"]

    assert response.status_code == 200
    assert result["name"] == "Eve"
    assert result["age"] == 32


# ===========================
# Mutation: updateUser
# ===========================
def test_update_user():
    mutation = """
    mutation {
        updateUser(id: 1, name: "AliceUpdated") {
            id
            name
        }
    }
    """
    response = client.post("/graphql", json={"query": mutation})
    result = response.json()["data"]["updateUser"]

    assert result["name"] == "AliceUpdated"


# ===========================
# Mutation: deleteUser
# ===========================
def test_delete_user():
    mutation = """
    mutation {
        deleteUser(id: 2)
    }
    """
    response = client.post("/graphql", json={"query": mutation})
    result = response.json()["data"]["deleteUser"]

    assert result is True
