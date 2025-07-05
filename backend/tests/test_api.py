import pytest
from src.main import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_hello_world(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"API de Gerenciamento de Tarefas funcionando!" in response.data

def test_listar_tarefas_vazio(client):
    response = client.get("/tarefas")
    assert response.status_code == 200
    assert b"[]" in response.data