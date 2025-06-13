# Vercel FastAPI with Supabase

Vercel上で動作するSupabase統合FastAPIサンプルアプリケーションです。

## 機能

- Supabaseデータベース統合
- ユーザー管理API（CRUD操作）
- メッセージ管理API
- ヘルスチェック（DB接続テスト含む）
- 現在時刻取得
- 統計情報取得

## 技術スタック

- **Backend**: FastAPI
- **Database**: Supabase (PostgreSQL)
- **Deployment**: Vercel
- **ORM**: Supabase Python SDK

## セットアップ手順

### 1. Supabaseプロジェクトの設定

1. [Supabase](https://supabase.com)でプロジェクトを作成
2. プロジェクトのSQL Editorで`database_setup.sql`を実行してテーブルを作成
3. Settings > APIからURL、anon key、service_role keyを取得

### 2. 環境変数の設定

`.env`ファイルを作成し、以下の値を設定：

```env
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_KEY=your-anon-key
SUPABASE_SERVICE_KEY=your-service-role-key
ENVIRONMENT=development
```

### 3. 依存関係のインストール

```bash
pip install -r requirements.txt
```

### 4. データベースセットアップ

Supabaseの管理画面のSQL Editorで`database_setup.sql`を実行してください。

## API エンドポイント

### 基本情報
- `GET /` - API情報とエンドポイント一覧
- `GET /health` - ヘルスチェック（DB接続テスト含む）
- `GET /time` - 現在時刻取得
- `GET /stats` - 統計情報
- `GET /test-db` - データベース接続テスト

### ユーザー管理
- `GET /users` - ユーザー一覧取得
- `GET /users/{user_id}` - 特定ユーザー取得
- `POST /users` - ユーザー作成
- `PUT /users/{user_id}` - ユーザー更新
- `DELETE /users/{user_id}` - ユーザー削除

### メッセージ管理
- `GET /messages` - メッセージ一覧取得
- `GET /messages/{message_id}` - 特定メッセージ取得
- `POST /messages` - メッセージ作成
- `DELETE /messages/{message_id}` - メッセージ削除

## デプロイ方法

### Vercel環境変数設定
Vercelの管理画面で以下の環境変数を設定：
- `SUPABASE_URL`
- `SUPABASE_KEY`
- `SUPABASE_SERVICE_KEY`

### Vercel CLI
```bash
npm i -g vercel
vercel
```

### GitHub連携
GitHubにプッシュすると自動デプロイされます。

## ローカル実行

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

アプリケーションは http://localhost:8000 でアクセス可能です。
API ドキュメントは http://localhost:8000/docs でアクセス可能です。

## 使用例

### ユーザー作成
```bash
curl -X POST "https://your-app.vercel.app/users" \
  -H "Content-Type: application/json" \
  -d '{"name": "新しいユーザー", "email": "new@example.com"}'
```

### ユーザー一覧取得
```bash
curl "https://your-app.vercel.app/users"
```

### メッセージ作成
```bash
curl -X POST "https://your-app.vercel.app/messages" \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello, World!", "user_id": 1}'
```

## データベーススキーマ

### users テーブル
```sql
- id: BIGSERIAL PRIMARY KEY
- name: VARCHAR(255) NOT NULL
- email: VARCHAR(255) UNIQUE NOT NULL
- created_at: TIMESTAMP WITH TIME ZONE
- updated_at: TIMESTAMP WITH TIME ZONE
```

### messages テーブル
```sql
- id: BIGSERIAL PRIMARY KEY
- message: TEXT NOT NULL
- user_id: BIGINT (外部キー)
- created_at: TIMESTAMP WITH TIME ZONE
- updated_at: TIMESTAMP WITH TIME ZONE
```

## 注意事項

- 本番環境では適切なRow Level Security (RLS) の設定を推奨
- Supabaseの利用制限に注意してください
- 環境変数は.envファイルにローカル用のみ記載し、本番はVercelの環境変数機能を使用

## トラブルシューティング

### データベース接続エラー
1. 環境変数が正しく設定されているか確認
2. `/test-db` エンドポイントで接続をテスト
3. Supabaseプロジェクトが正常に動作しているか確認

### パッケージインストールエラー
- Python 3.8以上を使用してください
- 仮想環境の使用を推奨します
