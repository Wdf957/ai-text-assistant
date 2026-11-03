from deepseek_chat import ask_deepseek
import json
import requests

text = input("请输入文本:")

if not text.strip():
    print("文本不能为空，请输入有效文本")
    raise SystemExit

question = f"""
请分析下面这段文本，概括主要内容并提取三个关键词。
只返回合法 JSON,不要添加 Markdown 代码围栏。
必须包含 summary 字段，值为字符串。
必须包含 keywords 字段，值为包含三个关键词的列表。
分析下面提供的文本内容。
文本：
{text}
"""
try:
    result = ask_deepseek(question)
except requests.exceptions.RequestException:
    print("API 调用失败，请检查网络、API Key 或服务状态。")
    raise SystemExit

try:
    data = json.loads(result)
except json.JSONDecodeError:
    print("解析失败:模型返回的内容不是合法JSON格式")
    print("模型返回原始内容如下：")
    print(result)
else:
    if not isinstance(data,dict):
        print("校验失败，返回的JSON不是字典格式")
        print(result)
    elif "summary" not in data or "keywords" not in data:
        print("返回结果缺少summary或keywords字段")
        print(result)
    elif not isinstance(data["summary"],str) or not isinstance(data["keywords"],list):
        print("校验失败，字段类型错误")
        print(result)
    else:
        print(data["summary"])
        print(data["keywords"])