import os
import requests

class DeepSeekConfigError(Exception):
    """DeepSeek 相关配置缺失或错误"""

def ask_deepseek(question):
    api_key = os.environ.get("DEEPSEEK_API_KEY")

    if not api_key:
        raise DeepSeekConfigError("缺少 DEEPSEEK_API_KEY 环境变量")
    print("API key is available")

    url = "https://api.deepseek.com/chat/completions"

    headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json",
    }

    body = {
        "model": "deepseek-flash",
        "messages": [
            {"role":"user","content":question}        
        ]
    }

    res = requests.post(
        url,
        headers=headers,
        json=body,
        timeout=30,
    )

    print(res.status_code)
    res.raise_for_status()

    data = res.json()
    answer = data["choices"][0]["message"]["content"]

    return answer

if __name__ == "__main__":
    answer = ask_deepseek("用一句话解释什么是Java")
    print(answer)

