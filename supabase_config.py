"""
Supabase設定とクライアント初期化
"""
import os
from supabase import create_client, Client
from dotenv import load_dotenv
import time
import logging

# 環境変数を読み込み
load_dotenv()

# ログ設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Supabase設定
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

def get_supabase_client() -> Client:
    """
    Supabaseクライアントを取得
    一般的な操作用（アノニマスキー使用）
    """
    if not SUPABASE_URL or not SUPABASE_KEY:
        raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set")
    
    # タイムアウト設定を含むオプション
    options = {
        "schema": "public",
        "headers": {"apikey": SUPABASE_KEY},
        "auto_refresh_token": True,
        "persist_session": False,  # Vercelでのセッション永続化を無効化
    }
    
    try:
        client = create_client(SUPABASE_URL, SUPABASE_KEY, options)
        logger.info("Supabase client created successfully")
        return client
    except Exception as e:
        logger.error(f"Failed to create Supabase client: {e}")
        raise

def get_supabase_admin_client() -> Client:
    """
    Supabase管理者クライアントを取得
    管理者権限が必要な操作用（サービスロールキー使用）
    """
    if not SUPABASE_URL or not SUPABASE_SERVICE_KEY:
        raise ValueError("SUPABASE_URL and SUPABASE_SERVICE_KEY must be set")
    
    # タイムアウト設定を含むオプション
    options = {
        "schema": "public",
        "headers": {"apikey": SUPABASE_SERVICE_KEY},
        "auto_refresh_token": True,
        "persist_session": False,  # Vercelでのセッション永続化を無効化
    }
    
    try:
        client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY, options)
        logger.info("Supabase admin client created successfully")
        return client
    except Exception as e:
        logger.error(f"Failed to create Supabase admin client: {e}")
        raise

def test_connection(client: Client, max_retries: int = 3) -> bool:
    """
    接続テスト（リトライ機能付き）
    """
    for attempt in range(max_retries):
        try:
            # シンプルなクエリで接続テスト
            response = client.from_("users").select("count", count="exact").limit(1).execute()
            logger.info(f"Connection test successful on attempt {attempt + 1}")
            return True
        except Exception as e:
            logger.warning(f"Connection test failed on attempt {attempt + 1}: {e}")
            if attempt < max_retries - 1:
                time.sleep(1)  # 1秒待機してリトライ
            else:
                logger.error(f"All connection attempts failed: {e}")
                return False
    return False

# グローバルクライアントインスタンス
# 環境変数が設定されている場合のみ初期化
supabase = None
supabase_admin = None

try:
    supabase = get_supabase_client()
    supabase_admin = get_supabase_admin_client()
    logger.info("Supabase clients initialized successfully")
except ValueError as e:
    logger.warning(f"Supabase configuration error: {e}")
except Exception as e:
    logger.error(f"Unexpected error initializing Supabase clients: {e}")
