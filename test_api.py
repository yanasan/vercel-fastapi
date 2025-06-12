#!/usr/bin/env python3
"""
Vercel FastAPI APIテストスクリプト
"""

import requests
import json
from datetime import datetime

# APIのベースURL（デプロイ後は実際のURLに変更してください）
BASE_URL = "http://localhost:8000"  # ローカルテスト用
# BASE_URL = "https://your-app.vercel.app"  # デプロイ後はこちらを使用

def test_api():
    print("FastAPI テスト開始")
    print("=" * 50)
    
    # 1. ルートエンドポイントテスト
    print("1. ルートエンドポイントテスト")
    response = requests.get(f"{BASE_URL}/")
    print(f"ステータス: {response.status_code}")
    print(f"レスポンス: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    print()
    
    # 2. ヘルスチェック
    print("2. ヘルスチェック")
    response = requests.get(f"{BASE_URL}/health")
    print(f"ステータス: {response.status_code}")
    print(f"レスポンス: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    print()
    
    # 3. 現在時刻取得
    print("3. 現在時刻取得")
    response = requests.get(f"{BASE_URL}/time")
    print(f"ステータス: {response.status_code}")
    print(f"レスポンス: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    print()
    
    # 4. ユーザー一覧取得
    print("4. ユーザー一覧取得")
    response = requests.get(f"{BASE_URL}/users")
    print(f"ステータス: {response.status_code}")
    print(f"レスポンス: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    print()
    
    # 5. ユーザー作成
    print("5. ユーザー作成")
    new_user = {
        "name": "テストユーザー",
        "email": "test@example.com"
    }
    response = requests.post(f"{BASE_URL}/users", json=new_user)
    print(f"ステータス: {response.status_code}")
    created_user = response.json()
    print(f"レスポンス: {json.dumps(created_user, indent=2, ensure_ascii=False)}")
    print()
    
    # 6. 特定ユーザー取得
    print("6. 特定ユーザー取得")
    user_id = created_user["id"]
    response = requests.get(f"{BASE_URL}/users/{user_id}")
    print(f"ステータス: {response.status_code}")
    print(f"レスポンス: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    print()
    
    # 7. メッセージ作成
    print("7. メッセージ作成")
    response = requests.post(f"{BASE_URL}/messages?message=テストメッセージです")
    print(f"ステータス: {response.status_code}")
    print(f"レスポンス: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    print()
    
    # 8. メッセージ一覧取得
    print("8. メッセージ一覧取得")
    response = requests.get(f"{BASE_URL}/messages")
    print(f"ステータス: {response.status_code}")
    print(f"レスポンス: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    print()
    
    # 9. 統計情報取得
    print("9. 統計情報取得")
    response = requests.get(f"{BASE_URL}/stats")
    print(f"ステータス: {response.status_code}")
    print(f"レスポンス: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    print()
    
    print("テスト完了!")

if __name__ == "__main__":
    try:
        test_api()
    except requests.exceptions.ConnectionError:
        print("エラー: APIサーバーに接続できません。")
        print("ローカルでテストする場合は、先にサーバーを起動してください:")
        print("python main.py")
    except Exception as e:
        print(f"エラーが発生しました: {e}")
