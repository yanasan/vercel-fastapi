#!/usr/bin/env python3
"""
本番用uvicornサーバー起動スクリプト
"""

import uvicorn
import os
import sys
from multiprocessing import cpu_count

def main():
    """本番サーバーを起動"""
    
    # 環境変数の設定
    os.environ.setdefault("ENV", "production")
    
    # ワーカー数の決定（CPUコア数に基づく）
    workers = min(cpu_count() * 2 + 1, 8)  # 最大8ワーカー
    
    print("=" * 50)
    print("FastAPI 本番サーバーを起動しています...")
    print("=" * 50)
    print(f"🚀 ワーカー数: {workers}")
    print("📡 サーバーURL: http://localhost:8000")
    print("🔒 自動リロード: 無効")
    print("=" * 50)
    print("終了するには Ctrl+C を押してください")
    print()
    
    try:
        uvicorn.run(
            "main:app",
            host="0.0.0.0",
            port=8000,
            workers=workers,      # マルチプロセス
            reload=False,         # 本番環境では無効
            log_level="warning",  # 本番用ログレベル
            access_log=True,
        )
    except KeyboardInterrupt:
        print("\n👋 サーバーを停止しました")
    except Exception as e:
        print(f"❌ エラーが発生しました: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
