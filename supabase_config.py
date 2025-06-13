"""
Supabase設定とクライアント初期化
"""
import os
from supabase import create_client, Client
from dotenv import load_dotenv

# 環境変数を読み込み
load_dotenv()

# Supabase設定
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

# Supabaseクライアントの初期化
def get_supabase_client() -> Client:
    """
    Supabaseクライアントを取得
    一般的な操作用（アノニマスキー使用）
    """
    if not SUPABASE_URL or not SUPABASE_KEY:
        raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set")
    
    return create_client(SUPABASE_URL, SUPABASE_KEY)

def get_supabase_admin_client() -> Client:
    """
    Supabase管理者クライアントを取得
    管理者権限が必要な操作用（サービスロールキー使用）
    """
    if not SUPABASE_URL or not SUPABASE_SERVICE_KEY:
        raise ValueError("SUPABASE_URL and SUPABASE_SERVICE_KEY must be set")
    
    return create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

# グローバルクライアントインスタンス
# 環境変数が設定されている場合のみ初期化
try:
    supabase: Client = get_supabase_client()
    supabase_admin: Client = get_supabase_admin_client()
except ValueError as e:
    print(f"Warning: Supabase configuration error: {e}")
    supabase = None
    supabase_admin = None
