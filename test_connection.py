#!/usr/bin/env python3
"""
Supabase接続テストスクリプト
"""
import os
import requests
from dotenv import load_dotenv

# 環境変数読み込み
load_dotenv()

def test_connection():
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    
    print(f"🔗 SUPABASE_URL: {url}")
    print(f"🔑 SUPABASE_KEY: {key[:20]}..." if key else "❌ Key not found")
    print()
    
    if not url or not key:
        print("❌ 環境変数が設定されていません")
        return
    
    # 1. DNS解決テスト
    print("1️⃣ DNS解決テスト:")
    import socket
    try:
        hostname = url.replace("https://", "").replace("http://", "")
        ip = socket.gethostbyname(hostname)
        print(f"  ✅ DNS解決成功: {hostname} -> {ip}")
    except Exception as e:
        print(f"  ❌ DNS解決失敗: {e}")
        return
    
    # 2. HTTP接続テスト
    print("\n2️⃣ HTTP接続テスト:")
    try:
        response = requests.get(f"{url}/rest/v1/", 
                              headers={"apikey": key},
                              timeout=10)
        print(f"  ✅ HTTP接続成功: {response.status_code}")
    except Exception as e:
        print(f"  ❌ HTTP接続失敗: {e}")
        return
    
    # 3. Supabaseクライアント接続テスト
    print("\n3️⃣ Supabaseクライアント接続テスト:")
    try:
        from supabase import create_client
        client = create_client(url, key)
        print("  ✅ クライアント作成成功")
        
        # テーブル一覧取得テスト
        response = client.table("users").select("count", count="exact").execute()
        print(f"  ✅ テーブルアクセス成功: users table ({response.count} records)")
        
    except Exception as e:
        print(f"  ❌ Supabaseクライアント失敗: {e}")
        print(f"  エラータイプ: {type(e).__name__}")
        
        # より詳細なエラー情報
        import traceback
        print(f"  詳細: {traceback.format_exc()}")

if __name__ == "__main__":
    test_connection()
