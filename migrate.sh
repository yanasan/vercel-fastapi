#!/bin/bash

# Supabaseマイグレーション実行スクリプト

set -e

echo "🚀 Supabase マイグレーションを開始します..."

# プロジェクトディレクトリに移動
cd "$(dirname "$0")"

echo "📁 現在のディレクトリ: $(pwd)"

# .envファイルから環境変数を読み込み
if [ -f ".env" ]; then
    echo "📄 .envファイルを読み込んでいます..."
    # #を含むパスワードに対応した読み込み
    while IFS='=' read -r key value; do
        # コメント行や空行をスキップ
        if [[ $key =~ ^[[:space:]]*# ]] || [[ -z $key ]]; then
            continue
        fi
        # クォートを除去して環境変数としてエクスポート
        key=$(echo $key | xargs)
        value=$(echo $value | sed 's/^["\x27]\|["\x27]$//g')
        export "$key=$value"
    done < .env
else
    echo "⚠️ .envファイルが見つかりません"
fi

# 環境変数チェック
if [ -z "$SUPABASE_PROJECT_REF" ]; then
    echo "❌ SUPABASE_PROJECT_REF が設定されていません"
    echo "   .envファイルに追加してください: SUPABASE_PROJECT_REF=your-project-ref"
    exit 1
fi

if [ -z "$SUPABASE_DB_PASSWORD" ]; then
    echo "❌ SUPABASE_DB_PASSWORD が設定されていません"
    echo "   .envファイルに追加してください: SUPABASE_DB_PASSWORD=your-db-password"
    exit 1
fi

if [ "$SUPABASE_DB_PASSWORD" = "your-database-password" ]; then
    echo "❌ SUPABASE_DB_PASSWORD を実際のパスワードに変更してください"
    exit 1
fi

# Supabase CLIがインストールされているかチェック
if ! command -v supabase &> /dev/null; then
    echo "❌ Supabase CLI がインストールされていません"
    echo "   インストール: brew install supabase/tap/supabase"
    exit 1
fi

echo "🔗 Supabaseプロジェクトにリンクしています..."
echo "   Project REF: $SUPABASE_PROJECT_REF"

# Supabase プロジェクトにリンク
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
echo "   - APIテスト: python test_connection.py"
