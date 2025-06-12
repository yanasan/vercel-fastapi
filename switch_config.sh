#!/bin/bash
# Vercel用の設定を切り替えるスクリプト

echo "Vercel設定切り替えツール"
echo "======================="
echo "1) 基本設定（main.pyからインポート）"
echo "2) 自己完結型設定（standalone.py使用）"
read -p "選択してください (1-2): " choice

case $choice in
    1)
        echo "🔄 基本設定に切り替えています..."
        # vercel.jsonでapi/index.pyを使用
        sed -i 's/api\/standalone.py/api\/index.py/g' vercel.json
        echo "✅ 基本設定に切り替えました"
        ;;
    2)
        echo "🔄 自己完結型設定に切り替えています..."
        # vercel.jsonでapi/standalone.pyを使用
        sed -i 's/api\/index.py/api\/standalone.py/g' vercel.json
        echo "✅ 自己完結型設定に切り替えました"
        ;;
    *)
        echo "❌ 無効な選択です"
        exit 1
        ;;
esac

echo ""
echo "📝 次のステップ:"
echo "git add ."
echo "git commit -m \"Switch Vercel configuration\""
echo "git push origin main"
