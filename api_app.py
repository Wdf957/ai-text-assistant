import requests.exceptions
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from deepseek_chat import ask_deepseek,DeepSeekConfigError
from service import analyze_text
import json

app = FastAPI()

class AnalyzeRequest(BaseModel):
    text: str

@app.get("/")
def home():
    return {"message":"Hello FastAPI"}

@app.post("/analyze")
def analyze(data: AnalyzeRequest):
    return analyze_text(data.text)