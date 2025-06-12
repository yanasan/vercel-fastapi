from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import json
from datetime import datetime

# FastAPIアプリケーション作成
app = FastAPI(title="Vercel FastAPI Sample", version="1.0.0")

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# データモデル
class User(BaseModel):
    id: int
    name: str
    email: str
    created_at: Optional[str] = None

class UserCreate(BaseModel):
    name: str
    email: str

class Message(BaseModel):
    message: str
    timestamp: str

# インメモリデータストレージ
users_db = [
    User(id=1, name="太郎", email="taro@example.com", created_at="2025-01-01T00:00:00"),
    User(id=2, name="花子", email="hanako@example.com", created_at="2025-01-01T00:00:00"),
]

messages_db = []

@app.get("/")
async def root():
    return {
        "message": "Vercel FastAPI Sample API",
        "version": "1.0.0",
        "endpoints": {
            "users": "/users",
            "health": "/health",
            "time": "/time",
            "messages": "/messages"
        }
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "fastapi-vercel"
    }

@app.get("/time")
async def get_current_time():
    return {
        "current_time": datetime.now().isoformat(),
        "timezone": "UTC"
    }

@app.get("/users", response_model=List[User])
async def get_users():
    return users_db

@app.get("/users/{user_id}", response_model=User)
async def get_user(user_id: int):
    user = next((user for user in users_db if user.id == user_id), None)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.post("/users", response_model=User)
async def create_user(user: UserCreate):
    new_id = max([u.id for u in users_db], default=0) + 1
    new_user = User(
        id=new_id,
        name=user.name,
        email=user.email,
        created_at=datetime.now().isoformat()
    )
    users_db.append(new_user)
    return new_user

@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    global users_db
    user = next((user for user in users_db if user.id == user_id), None)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    users_db = [u for u in users_db if u.id != user_id]
    return {"message": f"User {user_id} deleted successfully"}

@app.get("/messages", response_model=List[Message])
async def get_messages():
    return messages_db

@app.post("/messages", response_model=Message)
async def create_message(message: str):
    new_message = Message(
        message=message,
        timestamp=datetime.now().isoformat()
    )
    messages_db.append(new_message)
    return new_message

@app.get("/stats")
async def get_stats():
    return {
        "total_users": len(users_db),
        "total_messages": len(messages_db),
        "server_time": datetime.now().isoformat(),
        "api_version": "1.0.0"
    }

# エラーハンドリング用のエンドポイント
@app.get("/error")
async def trigger_error():
    raise HTTPException(status_code=500, detail="This is a test error")

# Vercel用: この部分は不要（削除）
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)
