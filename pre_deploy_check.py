#!/usr/bin/env python3
"""
Vercelデプロイ前のチェックスクリプト
"""

import os
import sys
import json

def check_file_exists(file_path, description):
    """ファイルの存在確認"""
    if os.path.exists(file_path):
        print(f"✅ {description}: {file_path}")
        return True
    else:
        print(f"❌ {description}が見つかりません: {file_path}")
        return False

def check_vercel_json():
    """vercel.jsonの内容確認"""
    try:
        with open("vercel.json", "r") as f:
            config = json.load(f)
        
        print("✅ vercel.json: 有効なJSON")
        
        # 必要なキーの確認
        required_keys = ["version", "builds", "routes"]
        for key in required_keys:
            if key in config:
                print(f"✅ vercel.json: {key} ✓")
            else:
                print(f"❌ vercel.json: {key}が不足")
                return False
        
        return True
    except json.JSONDecodeError:
        print("❌ vercel.json: 無効なJSON形式")
        return False
    except FileNotFoundError:
        print("❌ vercel.jsonが見つかりません")
        return False

def check_main_py():
    """main.pyの内容確認"""
    try:
        with open("main.py", "r") as f:
            content = f.read()
        
        # 重要なチェック項目
        checks = [
            ("FastAPIインポート", "from fastapi import FastAPI"),
            ("appインスタンス", "app = FastAPI"),
            ("ルートエンドポイント", "@app.get(\"/\")"),
        ]
        
        for check_name, check_string in checks:
            if check_string in content:
                print(f"✅ main.py: {check_name} ✓")
            else:
                print(f"❌ main.py: {check_name}が見つかりません")
                return False
        
        # uvicorn.runがないことを確認（Vercel用）
        if "uvicorn.run" in content and not content.count("# ") > content.count("uvicorn.run"):
            print("⚠️  main.py: uvicorn.runが有効になっています。Vercelでは不要です。")
        else:
            print("✅ main.py: uvicorn.runが適切にコメントアウトされています")
        
        return True
    except FileNotFoundError:
        print("❌ main.pyが見つかりません")
        return False

def main():
    """デプロイ前チェックを実行"""
    print("🔍 Vercelデプロイ前チェックを開始します...")
    print("=" * 50)
    
    checks = []
    
    # ファイル存在確認
    checks.append(check_file_exists("main.py", "メインアプリケーション"))
    checks.append(check_file_exists("api/index.py", "Vercelエントリーポイント"))
    checks.append(check_file_exists("requirements.txt", "依存関係ファイル"))
    checks.append(check_file_exists("vercel.json", "Vercel設定ファイル"))
    
    # 設定ファイルの内容確認
    checks.append(check_vercel_json())
    checks.append(check_main_py())
    
    print("=" * 50)
    
    success_count = sum(checks)
    total_checks = len(checks)
    
    if success_count == total_checks:
        print(f"🎉 チェック完了: {success_count}/{total_checks} すべて成功!")
        print("\n次のステップ:")
        print("1. vercel コマンドを実行してデプロイ")
        print("2. デプロイ完了後、test_vercel_api.py でテスト実行")
        return True
    else:
        print(f"⚠️  チェック結果: {success_count}/{total_checks} 問題があります")
        print("\n修正が必要な項目を確認してください。")
        return False

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)
