#!/bin/bash
# 実行権限を付与: chmod +x start.sh
# 簡単起動スクリプト

echo "FastAPI アプリケーション起動オプション"
echo "======================================"
echo "1) 開発モード（自動リロード有効）"
echo "2) 本番モード（マルチワーカー）"
echo "3) 直接uvicornコマンド"
echo "4) APIテスト実行"
echo "======================================"
read -p "選択してください (1-4): " choice

case $choice in
    1)
        echo "🚀 開発モードで起動します..."
        python dev_server.py
        ;;
    2)
        echo "🚀 本番モードで起動します..."
        python prod_server.py
        ;;
    3)
        echo "📡 基本uvicornコマンドで起動します..."
        uvicorn main:app --host 0.0.0.0 --port 8000 --reload
        ;;
    4)
        echo "🧪 APIテストを実行します..."
        echo "まずサーバーが起動していることを確認してください..."
        read -p "サーバーは起動していますか？ (y/n): " server_running
        if [ "$server_running" = "y" ] || [ "$server_running" = "Y" ]; then
            python test_api.py
        else
            echo "先にサーバーを起動してください"
        fi
        ;;
    *)
        echo "❌ 無効な選択です"
        exit 1
        ;;
esac
