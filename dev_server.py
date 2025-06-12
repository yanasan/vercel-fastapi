#!/usr/bin/env python3
"""
開発用uvicornサーバー起動スクリプト
"""

import uvicorn
import os
import sys

def main():
    """開発サーバーを起動"""
    
    # 環境変数の設定
    os.environ.setdefault("ENV", "development")
    
    print("=" * 50)
    print("FastAPI 開発サーバーを起動しています...")
    print("=" * 50)
    print("📡 サーバーURL: http://localhost:8000")
    print("📖 API ドキュメント: http://localhost:8000/docs")
    print("🔧 ReDoc ドキュメント: http://localhost:8000/redoc")
    print("🔄 自動リロード: 有効")
    print("=" * 50)
    print("終了するには Ctrl+C を押してください")
    print()
    
    try:
        uvicorn.run(
            "main:app",           # アプリケーションモジュール
            host="0.0.0.0",       # すべてのIPアドレスでリッスン
            port=8000,            # ポート番号
            reload=True,          # ファイル変更時の自動リロード
            reload_dirs=["./"],   # 監視するディレクトリ
            log_level="info",     # ログレベル
            access_log=True,      # アクセスログ有効
        )
    except KeyboardInterrupt:
        print("\n👋 サーバーを停止しました")
    except Exception as e:
        print(f"❌ エラーが発生しました: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
