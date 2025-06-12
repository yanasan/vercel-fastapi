#!/bin/bash
# 実行権限を付与: chmod +x deploy.sh

echo "Vercel FastAPI デプロイスクリプト"
echo "=================================="

# デプロイ前チェック実行
echo "🔍 デプロイ前チェックを実行しています..."
python3 pre_deploy_check.py

if [ $? -ne 0 ]; then
    echo "❌ デプロイ前チェックでエラーが発生しました。"
    echo "問題を修正してから再度実行してください。"
    exit 1
fi

echo ""
echo "✅ チェック完了！デプロイを続行します..."
echo ""

# Vercel CLIがインストールされているかチェック
if ! command -v vercel &> /dev/null; then
    echo "Vercel CLIがインストールされていません。"
    echo "以下のコマンドでインストールしてください："
    echo "npm i -g vercel"
    exit 1
fi

echo "🚀 Vercelにデプロイしています..."
vercel --prod

if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 デプロイが完了しました！"
    echo ""
    echo "📝 次のステップ:"
    echo "1. VercelのダッシュボードでURLを確認"
    echo "2. 以下のコマンドでAPIテスト実行:"
    echo "   python3 test_vercel_api.py https://your-domain.vercel.app"
    echo ""
    echo "📚 ドキュメントアクセス:"
    echo "   https://your-domain.vercel.app/docs"
    echo "   https://your-domain.vercel.app/redoc"
else
    echo ""
    echo "❌ デプロイに失敗しました。"
    echo "エラー内容を確認して再度試してください。"
    exit 1
fi
