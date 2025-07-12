import pytest
from unittest.mock import patch, MagicMock
from src.main import create_app

@pytest.fixture
def client():
    app = create_app({"TESTING": True})
    with app.test_client() as client:
        yield client

def test_hello_world(client):
    with patch.object(client.application, "init_db") as mock_init_db, \
         patch("src.main.psycopg2.connect") as mock_connect:
        
        mock_conn = MagicMock()
        mock_cur = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cur
        
        response = client.get("/")
        assert response.status_code == 200
        assert b"API de Tarefas com PostgreSQL" in response.data
        mock_init_db.assert_not_called()

def test_listar_tarefas_vazio(client):
    with patch.object(client.application, "init_db") as mock_init_db, \
         patch("src.main.psycopg2.connect") as mock_connect:

        mock_conn = MagicMock()
        mock_cur = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cur
        mock_cur.fetchall.return_value = []

        response = client.get("/tarefas")
        assert response.status_code == 200
        assert response.json == []
        mock_init_db.assert_not_called()
