from fastapi.testclient import TestClient
from unittest.mock import patch

import pytest
import requests
import deepseek_chat
from deepseek_chat import DeepSeekConfigError

from api_app import app

client = TestClient(app)


def test_home():
    resp = client.get("/")
    assert resp.status_code == 200


def test_timeout_returns_504():
    with patch("service.ask_deepseek") as mock_ask:
        mock_ask.side_effect = requests.exceptions.Timeout()
        resp = client.post("/analyze", json={"text": "测试文本"})
        assert resp.status_code == 504


def test_normal_returns_200():
    with patch("service.ask_deepseek") as mock_ask:
        mock_ask.return_value = '{"summary": "这是测试摘要", "keywords": ["a", "b", "c"]}'
        resp = client.post("/analyze", json={"text": "测试文本"})
        assert resp.status_code == 200
        assert resp.json()["summary"] == "这是测试摘要"


def test_no_key_raise_config_error(monkeypatch):
    monkeypatch.delenv("DEEPSEEK_API_KEY", raising=False)
    with pytest.raises(DeepSeekConfigError):
        deepseek_chat.ask_deepseek("测试问题")


def test_text_too_long_returns_400():
    with patch("service.ask_deepseek") as mock_ask:
        resp = client.post("/analyze", json={"text": "文" * 501})
        assert resp.status_code == 400
        mock_ask.assert_not_called()
