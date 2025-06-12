# Vercel FastAPI Sample

Vercel上で動作するFastAPIサンプルアプリケーションです。

## 機能

- ユーザー管理API（CRUD操作）
- メッセージ管理API
- ヘルスチェック
- 現在時刻取得
- 統計情報取得

## API エンドポイント

### 基本
- `GET /` - API情報とエンドポイント一覧
- `GET /health` - ヘルスチェック
- `GET /time` - 現在時刻取得
- `GET /stats` - 統計情報

### ユーザー管理
- `GET /users` - ユーザー一覧取得
- `GET /users/{user_id}` - 特定ユーザー取得
- `POST /users` - ユーザー作成
- `DELETE /users/{user_id}` - ユーザー削除

### メッセージ
- `GET /messages` - メッセージ一覧取得
- `POST /messages` - メッセージ作成

## デプロイ方法

1. Vercel CLIをインストール:
```bash
npm i -g vercel
```

2. プロジェクトディレクトリに移動:
```bash
cd vercel_fastapi
```

3. Vercelにデプロイ:
```bash
vercel
```

## ローカル実行

### 方法1: 開発用スクリプト（推奨）
```bash
# 依存関係インストール
pip install -r requirements.txt

# 開発サーバー起動（自動リロード有効）
python dev_server.py
```

### 方法2: Makefileを使用
```bash
make install  # 依存関係インストール
make dev      # 開発サーバー起動
make prod     # 本番サーバー起動
make test     # APIテスト実行
```

### 方法3: 直接uvicornコマンド
```bash
# 開発モード（自動リロード有効）
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# 本番モード（マルチワーカー）
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4

# デバッグモード
uvicorn main:app --host 0.0.0.0 --port 8000 --reload --log-level debug
```

### 方法4: 対話式起動スクリプト
```bash
chmod +x start.sh
./start.sh
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
curl -X POST "https://your-app.vercel.app/messages?message=Hello World"
```

## 注意点

- このサンプルではインメモリデータストレージを使用しているため、デプロイごとにデータはリセットされます
- 本番環境では適切なデータベースを使用してください
- CORS設定は開発用のため、本番環境では適切に制限してください
# vercel-fastapi
