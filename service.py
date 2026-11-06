import json
import requests.exceptions
from fastapi import HTTPException
from deepseek_chat import ask_deepseek,DeepSeekConfigError



def analyze_text(text: str):
    if len(text) > 500:
        raise HTTPException(
            status_code=400,
            detail=f"请求文本过长，最大长度为500字符，输入长度为{len(text)}"
        )

    if len(text) == 0:
        raise HTTPException(
            status_code=400,
            detail="请求文本为空"
        )
    
    prompt = f"""
请分析下面这段文本，概括主要内容并提取三个关键词。
只返回合法 JSON,不要添加 Markdown 代码围栏。
必须包含 summary 字段，值为字符串。
必须包含 keywords 字段，值为包含三个关键词的列表。
分析下面提供的文本内容。
文本：
{text}
"""
    
    try:
        result = ask_deepseek(prompt)
        
    except requests.exceptions.Timeout:
        raise HTTPException(
            status_code=504,
            detail="上游超时：DeepSeek服务未在30秒内返回响应"
        )

    except DeepSeekConfigError:
        raise HTTPException(
            status_code=500,
            detail="服务端配置缺失：未设置DEEPSEEK_API_KEY"
        )
    
    print("模型原始返回内容：",repr(result))
    try:
        analysis_data = json.loads(result)

    except json.JSONDecodeError:
        raise HTTPException(
           status_code=502,
           detail="模型返回的内容不是合法JSON"
        )

    if not isinstance(analysis_data,dict):
            raise HTTPException(
                status_code=502,
                detail="校验失败，模型返回的数据不是JSON对象"
        )

    if "summary" not in analysis_data or "keywords" not in analysis_data:
        raise HTTPException(
            status_code=502,
            detail="模型返回的JSON缺少必要字段"
        )

    if not isinstance(analysis_data["summary"],str) or not isinstance (analysis_data["keywords"],list):
        raise HTTPException(
            status_code=502,
            detail="校验失败，字段类型错误"
        )

    keywords = analysis_data["keywords"]

    if len(keywords) != 3 or not all(isinstance(word,str) for word in keywords):
        raise HTTPException(
            status_code=502,
            detail="校验失败，keywords元素错误"
        )

    return analysis_data
