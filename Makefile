# FastAPI 開発用Makefile

.PHONY: help install dev prod test clean docs setup-github

# デフォルトターゲット
help:
	@echo "利用可能なコマンド:"
	@echo "  make install      - 依存関係をインストール"
	@echo "  make dev          - 開発サーバーを起動"
	@echo "  make prod         - 本番サーバーを起動"
	@echo "  make test         - APIテストを実行"
	@echo "  make docs         - ドキュメントを開く"
	@echo "  make clean        - キャッシュファイルを削除"
	@echo "  make deploy       - Vercelにデプロイ"
	@echo "  make setup-github - GitHub Actions設定ガイドを表示"
	@echo "  make git-push     - GitHubにプッシュ（自動デプロイ実行）"

# 依存関係のインストール
install:
	@echo "📦 依存関係をインストールしています..."
	pip install -r requirements-dev.txt
	@echo "✅ インストール完了!"

# Vercel用の軽量インストール
install-prod:
	@echo "📦 Vercel用依存関係をインストールしています..."
	pip install -r requirements.txt
	@echo "✅ インストール完了!"

# 開発サーバー起動
dev:
	@echo "🚀 開発サーバーを起動します..."
	python dev_server.py

# 本番サーバー起動
prod:
	@echo "🚀 本番サーバーを起動します..."
	python prod_server.py

# APIテスト実行
test:
	@echo "🧪 APIテストを実行します..."
	python test_api.py

# ドキュメントを開く
docs:
	@echo "📖 ブラウザでAPIドキュメントを開きます..."
	@open http://localhost:8000/docs 2>/dev/null || echo "http://localhost:8000/docs をブラウザで開いてください"

# キャッシュ削除
clean:
	@echo "🧹 キャッシュファイルを削除しています..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.pyc" -delete 2>/dev/null || true
	@echo "✅ 削除完了!"

# Vercelデプロイ
deploy:
	@echo "🚀 Vercelにデプロイします..."
	chmod +x deploy.sh
	./deploy.sh

# GitHub Actions設定ガイド表示
setup-github:
	@echo "🔧 GitHub Actions設定ガイド:"
	@cat GITHUB_ACTIONS_SETUP.md

# GitHubにプッシュ（自動デプロイ実行）
git-push:
	@echo "💾 GitHubにプッシュして自動デプロイを実行します..."
	git add .
	@read -p "コミットメッセージを入力: " msg; git commit -m "$msg"
	git push origin main
	@echo "✅ プッシュ完了！GitHub Actionsが自動でデプロイを実行します。"
