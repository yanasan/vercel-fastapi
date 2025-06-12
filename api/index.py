"""
Vercel用のFastAPIエントリーポイント
"""

# main.pyからFastAPIアプリケーションをインポート
try:
    from main import app
except ImportError as e:
    print(f"Error importing main: {e}")
    # フォールバック用の基本的なFastAPIアプリ
    from fastapi import FastAPI
    app = FastAPI(title="FastAPI on Vercel", version="1.0.0")
    
    @app.get("/")
    async def root():
        return {"message": "FastAPI is running on Vercel!", "status": "ok"}

# Vercel Serverless Functions用のハンドラー
def handler(event, context):
    """
    AWS Lambda/Vercel Serverless Functions用のハンドラー
    """
    return app

# 直接エクスポート（Vercelが自動認識）
# これが最も重要な部分
app = app
