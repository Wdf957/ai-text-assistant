import unittest
from unittest.mock import patch, Mock
from deepseek_chat import ask_deepseek


class TestAskDeepseek(unittest.TestCase):

    @patch("deepseek_chat.requests.post")
    def test_returns_answer(self, mock_post):
        mock_response = Mock()
        mock_response.json.return_value = {
            "choices": [
                {
                    "message": {
                        "content": "这是测试回答"
                    }
                }
            ]
        }

        mock_post.return_value = mock_response

        answer = ask_deepseek("测试问题")

        self.assertEqual(answer, "这是测试回答")


if __name__ == "__main__":
    unittest.main()