# FastAPI Vercel Project

.PHONY: help install dev deploy

help:
	@echo "利用可能なコマンド:"
	@echo "  make install  - 依存関係をインストール"
	@echo "  make dev      - ローカル開発サーバー起動"
	@echo "  make deploy   - Vercelにデプロイ"

install:
	pip install -r requirements.txt
	pip install uvicorn

dev:
	uvicorn main:app --reload --host 0.0.0.0 --port 8000

deploy:
	vercel --prod
