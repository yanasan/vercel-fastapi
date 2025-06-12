#!/bin/bash
# apiフォルダを削除（参考リポジトリ形式に変更）
echo "🗑️  api フォルダを削除しています..."
rm -rf api/
echo "✅ 削除完了"

echo "📋 現在の構成:"
echo "- main.py: メインアプリケーション"
echo "- vercel.json: main.pyを直接指定"
echo ""
echo "📝 次のステップ:"
echo "git add ."
echo "git commit -m \"Simplify structure: Use main.py directly\""
echo "git push origin main"
