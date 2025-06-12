#!/usr/bin/env python3
"""
Vercelデプロイ後のAPIテストスクリプト
"""

import requests
import json
import sys
from datetime import datetime

def test_deployed_api(base_url):
    """デプロイされたAPIをテスト"""
    
    print("=" * 60)
    print(f"Vercel FastAPI デプロイテスト")
    print(f"テスト対象URL: {base_url}")
    print("=" * 60)
    
    tests = [
        ("ルートエンドポイント", "/"),
        ("ヘルスチェック", "/health"),
        ("現在時刻", "/time"),
        ("ユーザー一覧", "/users"),
        ("統計情報", "/stats"),
    ]
    
    success_count = 0
    total_tests = len(tests)
    
    for test_name, endpoint in tests:
        try:
            print(f"🧪 {test_name}をテストしています...")
            response = requests.get(f"{base_url}{endpoint}", timeout=30)
            
            if response.status_code == 200:
                print(f"✅ {test_name}: 成功 (ステータス: {response.status_code})")
                success_count += 1
            else:
                print(f"❌ {test_name}: 失敗 (ステータス: {response.status_code})")
                print(f"   レスポンス: {response.text[:200]}...")
                
        except requests.exceptions.Timeout:
            print(f"⏰ {test_name}: タイムアウト (30秒)")
        except requests.exceptions.ConnectionError:
            print(f"🔌 {test_name}: 接続エラー")
        except Exception as e:
            print(f"❌ {test_name}: エラー - {str(e)}")
        
        print()
    
    # POST テスト
    print("📝 POST テストを実行しています...")
    try:
        new_user = {
            "name": "Vercelテストユーザー",
            "email": "vercel-test@example.com"
        }
        response = requests.post(f"{base_url}/users", json=new_user, timeout=30)
        
        if response.status_code == 200:
            print("✅ ユーザー作成: 成功")
            success_count += 1
        else:
            print(f"❌ ユーザー作成: 失敗 (ステータス: {response.status_code})")
            
    except Exception as e:
        print(f"❌ ユーザー作成: エラー - {str(e)}")
    
    total_tests += 1
    
    print("=" * 60)
    print(f"テスト結果: {success_count}/{total_tests} 成功")
    
    if success_count == total_tests:
        print("🎉 すべてのテストが成功しました！")
        print(f"📖 API ドキュメント: {base_url}/docs")
        print(f"🔧 ReDoc: {base_url}/redoc")
        return True
    else:
        print("⚠️  一部のテストが失敗しました。")
        return False

def main():
    if len(sys.argv) != 2:
        print("使用方法: python test_vercel_api.py <deployed-url>")
        print("例: python test_vercel_api.py https://your-app.vercel.app")
        sys.exit(1)
    
    base_url = sys.argv[1].rstrip('/')
    
    # URLの検証
    if not base_url.startswith(('http://', 'https://')):
        print("❌ 無効なURL形式です。http://またはhttps://で始まる必要があります。")
        sys.exit(1)
    
    success = test_deployed_api(base_url)
    
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()
