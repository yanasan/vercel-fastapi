from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import json
from datetime import datetime
from supabase_config import supabase, supabase_admin, test_connection
import logging

# ログ設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPIアプリケーション作成
app = FastAPI(title="Vercel FastAPI with Supabase", version="1.0.0")

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
    id: Optional[int] = None
    name: str
    email: str
    created_at: Optional[str] = None

class UserCreate(BaseModel):
    name: str
    email: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None

class Message(BaseModel):
    id: Optional[int] = None
    message: str
    user_id: Optional[int] = None
    created_at: Optional[str] = None

class MessageCreate(BaseModel):
    message: str
    user_id: Optional[int] = None

@app.get("/")
async def root():
    return {
        "message": "Vercel FastAPI with Supabase",
        "version": "1.0.0",
        "database": "Supabase",
        "endpoints": {
            "users": "/users",
            "messages": "/messages",
            "health": "/health",
            "time": "/time"
        }
    }

@app.get("/health")
async def health_check():
    """ヘルスチェック（Supabase接続テスト含む）"""
    if supabase is None:
        return {
            "status": "warning",
            "timestamp": datetime.now().isoformat(),
            "service": "fastapi-vercel-supabase",
            "database": "not configured",
            "message": "Supabase environment variables not set"
        }
    
    # 接続テスト実行
    connection_ok = test_connection(supabase, max_retries=2)
    
    if connection_ok:
        try:
            # ユーザー数を取得
            response = supabase.table("users").select("count", count="exact").execute()
            user_count = response.count if response.count is not None else 0
            db_status = "connected"
        except Exception as e:
            logger.error(f"Error fetching user count: {e}")
            db_status = "connected_but_query_failed"
            user_count = 0
    else:
        db_status = "connection_failed"
        user_count = 0
    
    return {
        "status": "healthy" if connection_ok else "degraded",
        "timestamp": datetime.now().isoformat(),
        "service": "fastapi-vercel-supabase",
        "database": db_status,
        "user_count": user_count
    }

@app.get("/time")
async def get_current_time():
    return {
        "current_time": datetime.now().isoformat(),
        "timezone": "UTC"
    }

# ユーザー関連エンドポイント
@app.get("/users", response_model=List[User])
async def get_users():
    """全ユーザー取得"""
    if supabase is None:
        raise HTTPException(status_code=503, detail="Database not configured")
    
    try:
        logger.info("Fetching users from database")
        response = supabase.table("users").select("*").execute()
        logger.info(f"Successfully fetched {len(response.data)} users")
        return response.data
    except Exception as e:
        logger.error(f"Failed to fetch users: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch users: {str(e)}")

@app.get("/users/{user_id}", response_model=User)
async def get_user(user_id: int):
    """特定ユーザー取得"""
    try:
        response = supabase.table("users").select("*").eq("id", user_id).execute()
        if not response.data:
            raise HTTPException(status_code=404, detail="User not found")
        return response.data[0]
    except Exception as e:
        if "User not found" in str(e):
            raise e
        raise HTTPException(status_code=500, detail=f"Failed to fetch user: {str(e)}")

@app.post("/users", response_model=User)
async def create_user(user: UserCreate):
    """ユーザー作成"""
    try:
        response = supabase.table("users").insert({
            "name": user.name,
            "email": user.email,
            "created_at": datetime.now().isoformat()
        }).execute()
        
        if not response.data:
            raise HTTPException(status_code=400, detail="Failed to create user")
        
        return response.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create user: {str(e)}")

@app.put("/users/{user_id}", response_model=User)
async def update_user(user_id: int, user: UserUpdate):
    """ユーザー更新"""
    try:
        # 更新データを準備
        update_data = {}
        if user.name is not None:
            update_data["name"] = user.name
        if user.email is not None:
            update_data["email"] = user.email
        
        if not update_data:
            raise HTTPException(status_code=400, detail="No update data provided")
        
        response = supabase.table("users").update(update_data).eq("id", user_id).execute()
        
        if not response.data:
            raise HTTPException(status_code=404, detail="User not found")
        
        return response.data[0]
    except Exception as e:
        if "User not found" in str(e):
            raise e
        raise HTTPException(status_code=500, detail=f"Failed to update user: {str(e)}")

@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    """ユーザー削除"""
    try:
        response = supabase.table("users").delete().eq("id", user_id).execute()
        
        if not response.data:
            raise HTTPException(status_code=404, detail="User not found")
        
        return {"message": f"User {user_id} deleted successfully"}
    except Exception as e:
        if "User not found" in str(e):
            raise e
        raise HTTPException(status_code=500, detail=f"Failed to delete user: {str(e)}")

# メッセージ関連エンドポイント
@app.get("/messages", response_model=List[Message])
async def get_messages():
    """全メッセージ取得"""
    try:
        response = supabase.table("messages").select("*").execute()
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch messages: {str(e)}")

@app.get("/messages/{message_id}", response_model=Message)
async def get_message(message_id: int):
    """特定メッセージ取得"""
    try:
        response = supabase.table("messages").select("*").eq("id", message_id).execute()
        if not response.data:
            raise HTTPException(status_code=404, detail="Message not found")
        return response.data[0]
    except Exception as e:
        if "Message not found" in str(e):
            raise e
        raise HTTPException(status_code=500, detail=f"Failed to fetch message: {str(e)}")

@app.post("/messages", response_model=Message)
async def create_message(message: MessageCreate):
    """メッセージ作成"""
    try:
        response = supabase.table("messages").insert({
            "message": message.message,
            "user_id": message.user_id,
            "created_at": datetime.now().isoformat()
        }).execute()
        
        if not response.data:
            raise HTTPException(status_code=400, detail="Failed to create message")
        
        return response.data[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create message: {str(e)}")

@app.delete("/messages/{message_id}")
async def delete_message(message_id: int):
    """メッセージ削除"""
    try:
        response = supabase.table("messages").delete().eq("id", message_id).execute()
        
        if not response.data:
            raise HTTPException(status_code=404, detail="Message not found")
        
        return {"message": f"Message {message_id} deleted successfully"}
    except Exception as e:
        if "Message not found" in str(e):
            raise e
        raise HTTPException(status_code=500, detail=f"Failed to delete message: {str(e)}")

@app.get("/stats")
async def get_stats():
    """統計情報取得"""
    try:
        users_response = supabase.table("users").select("count", count="exact").execute()
        messages_response = supabase.table("messages").select("count", count="exact").execute()
        
        return {
            "total_users": users_response.count or 0,
            "total_messages": messages_response.count or 0,
            "server_time": datetime.now().isoformat(),
            "api_version": "1.0.0",
            "database": "Supabase"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch stats: {str(e)}")

@app.get("/debug-env")
async def debug_environment():
    """環境変数のデバッグ情報（本番環境では削除すること）"""
    import os
    
    return {
        "supabase_url_set": bool(os.getenv("SUPABASE_URL")),
        "supabase_key_set": bool(os.getenv("SUPABASE_KEY")),
        "supabase_service_key_set": bool(os.getenv("SUPABASE_SERVICE_KEY")),
        "supabase_url_prefix": os.getenv("SUPABASE_URL", "")[:20] + "..." if os.getenv("SUPABASE_URL") else "Not set",
        "environment": os.getenv("VERCEL_ENV", "unknown"),
        "all_env_keys": [key for key in os.environ.keys() if "SUPABASE" in key],
        "timestamp": datetime.now().isoformat(),
    }

# テスト用エンドポイント
@app.get("/test-db")
async def test_database_connection():
    """データベース接続テスト"""
    if supabase is None:
        return {
            "status": "error",
            "message": "Supabase client not initialized",
            "timestamp": datetime.now().isoformat()
        }
    
    try:
        logger.info("Testing database connection...")
        
        # シンプルなクエリでテスト
        response = supabase.from_("users").select("id").limit(1).execute()
        
        return {
            "status": "success",
            "message": "Database connection successful",
            "timestamp": datetime.now().isoformat(),
            "test_query_result": "OK"
        }
    except Exception as e:
        logger.error(f"Database connection test failed: {e}")
        return {
            "status": "error",
            "message": f"Database connection failed: {str(e)}",
            "timestamp": datetime.now().isoformat(),
            "error_type": type(e).__name__
        }
