"""
シンプルなSupabase設定（デバッグ用）
"""
import os
from supabase import create_client, Client
from dotenv import load_dotenv
import logging

# 環境変数を読み込み
load_dotenv()

# ログ設定
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 環境変数から直接取得
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

logger.info(f"Loading Supabase config...")
logger.info(f"URL present: {bool(SUPABASE_URL)}")
logger.info(f"Key present: {bool(SUPABASE_KEY)}")
logger.info(f"Service key present: {bool(SUPABASE_SERVICE_KEY)}")

# グローバル変数初期化
supabase = None
supabase_admin = None

def init_supabase():
    """Supabaseクライアントを初期化"""
    global supabase, supabase_admin
    
    if not SUPABASE_URL or not SUPABASE_KEY:
        logger.error("Missing SUPABASE_URL or SUPABASE_KEY")
        return False
    
    try:
        logger.info("Creating Supabase client...")
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        logger.info("✅ Supabase client created successfully")
        
        if SUPABASE_SERVICE_KEY:
            logger.info("Creating Supabase admin client...")
            supabase_admin = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
            logger.info("✅ Supabase admin client created successfully")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Failed to initialize Supabase: {e}")
        logger.error(f"Error type: {type(e).__name__}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        return False

def test_connection(client: Client, max_retries: int = 2) -> bool:
    """接続テスト"""
    if not client:
        return False
        
    for attempt in range(max_retries):
        try:
            # 最もシンプルなクエリでテスト
            response = client.table("users").select("id").limit(1).execute()
            logger.info(f"✅ Connection test successful on attempt {attempt + 1}")
            return True
        except Exception as e:
            logger.warning(f"⚠️ Connection test failed on attempt {attempt + 1}: {e}")
            if attempt < max_retries - 1:
                import time
                time.sleep(0.5)
    
    return False

# 初期化実行
logger.info("🚀 Initializing Supabase...")
init_success = init_supabase()
logger.info(f"Initialization result: {init_success}")
