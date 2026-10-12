import pytest
from fastapi.testclient import TestClient

import app_final


@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.setattr(app_final, "NOTE_FILE", tmp_path / "note.txt")
    with TestClient(app_final.app) as test_client:
        yield test_client


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_save_and_read(client):
    response = client.post("/save", json={"text": "Моя заметка"})
    assert response.status_code == 200
    assert client.get("/note").json() == {"text": "Моя заметка"}


def test_clear(client):
    client.post("/save", json={"text": "Удали меня"})
    response = client.post("/clear")
    assert response.status_code == 200
    assert client.get("/note").json() == {"text": ""}


def test_save_without_text(client):
    response = client.post("/save", json={})
    assert response.status_code == 422