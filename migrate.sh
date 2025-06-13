#!/bin/bash

# Supabaseマイグレーション実行スクリプト

set -e

echo "🚀 Supabase マイグレーションを開始します..."

# 環境変数チェック
if [ -z "$SUPABASE_PROJECT_REF" ]; then
    echo "❌ SUPABASE_PROJECT_REF が設定されていません"
    echo "   例: export SUPABASE_PROJECT_REF=your-project-ref"
    exit 1
fi

if [ -z "$SUPABASE_DB_PASSWORD" ]; then
    echo "❌ SUPABASE_DB_PASSWORD が設定されていません"
    echo "   例: export SUPABASE_DB_PASSWORD=your-db-password"
    exit 1
fi

# Supabase CLIがインストールされているかチェック
if ! command -v supabase &> /dev/null; then
    echo "❌ Supabase CLI がインストールされていません"
    echo "   インストール: brew install supabase/tap/supabase"
    exit 1
fi

# プロジェクトディレクトリに移動
cd "$(dirname "$0")"

echo "📁 現在のディレクトリ: $(pwd)"

# Supabase プロジェクトにリンク
echo "🔗 Supabaseプロジェクトにリンクしています..."
supabase link --project-ref $SUPABASE_PROJECT_REF --password $SUPABASE_DB_PASSWORD

# マイグレーション実行
echo "📊 マイグレーションを実行しています..."
supabase db push

# シードデータ実行
echo "🌱 シードデータを実行しています..."
supabase db seed

echo "✅ マイグレーション完了！"
echo "🔍 確認方法:"
echo "   - Supabase Dashboard: https://supabase.com/dashboard"
echo "   - ローカル確認: python check_tables.py"
