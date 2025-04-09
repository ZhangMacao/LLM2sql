from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import ollama
import psycopg2
from datetime import datetime

# 初始化 FastAPI
app = FastAPI()

# 连接数据库
conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="123456",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

# 请求结构
class ChatRequest(BaseModel):
    prompt: str
    model: str = "deepseek-r1:1.5b"  

# 调用 Ollama 模型
def call_llm(prompt: str, model: str = "deepseek-r1:1.5b"):
    response = ollama.chat(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )
    return response["message"]["content"]

# API 端点
@app.post("/chat/")
def chat(request: ChatRequest):
    try:
        response_text = call_llm(request.prompt, request.model)
        
        # 记录数据到数据库
        cur.execute(
            "INSERT INTO chat_history (prompt, response, model_name, timestamp) VALUES (%s, %s, %s, %s)",
            (request.prompt, response_text, request.model, datetime.now())
        )
        conn.commit()
        
        return {"prompt": request.prompt, "response": response_text, "model": request.model}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
