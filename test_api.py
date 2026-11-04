from fastapi.testclient import TestClient
from unittest.mock import patch

import requests

from api_app import app

client = TestClient(app)


def test_hello():
    assert 1 + 1 == 2


def test_home():
    resp = client.get("/")
    assert resp.status_code == 200


def test_timeout_returns_504():
    with patch("api_app.ask_deepseek") as mock_ask:
        mock_ask.side_effect = requests.exceptions.Timeout()
        resp = client.post("/analyze", json={"text": "测试文本"})
        assert resp.status_code == 504


def test_normal_returns_200():
    with patch("api_app.ask_deepseek") as mock_ask:
        mock_ask.return_value = '{"summary": "这是测试摘要", "keywords": ["a", "b", "c"]}'
        resp = client.post("/analyze", json={"text": "测试文本"})
        assert resp.status_code == 200
        assert resp.json()["summary"] == "这是测试摘要"