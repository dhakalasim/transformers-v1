import json

import pytest
from fastapi.testclient import TestClient

from transformers_v1.api import app

client = TestClient(app)


def test_list_bots():
    response = client.get("/api/bots")
    assert response.status_code == 200
    names = [bot["name"] for bot in response.json()]
    assert {"Bumblebee", "Ironhide", "Ratchet", "Jazz"}.issubset(set(names))


def test_transform_success():
    response = client.post(
        "/api/transform",
        json={"content": json.dumps({"a": 1}), "from_format": "json", "to_format": "yaml"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["bot_name"] == "Bumblebee"
    assert "a: 1" in body["result"]


def test_transform_no_bot_available():
    response = client.post(
        "/api/transform",
        json={"content": "# hi", "from_format": "html", "to_format": "csv"},
    )
    assert response.status_code == 422
    assert "No Autobot" in response.json()["detail"]


def test_transform_bad_content():
    response = client.post(
        "/api/transform",
        json={"content": "not json", "from_format": "json", "to_format": "yaml"},
    )
    assert response.status_code == 400
