# Vercel FastAPI Sample

Vercel上で動作するFastAPIサンプルアプリケーションです。

## 機能

- ユーザー管理API（CRUD操作）
- メッセージ管理API
- ヘルスチェック
- 現在時刻取得
- 統計情報取得

## API エンドポイント

- `GET /` - API情報とエンドポイント一覧
- `GET /health` - ヘルスチェック
- `GET /time` - 現在時刻取得
- `GET /users` - ユーザー一覧取得
- `GET /users/{user_id}` - 特定ユーザー取得
- `POST /users` - ユーザー作成
- `DELETE /users/{user_id}` - ユーザー削除
- `GET /messages` - メッセージ一覧取得
- `POST /messages` - メッセージ作成
- `GET /stats` - 統計情報

## デプロイ方法

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
pip install uvicorn
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
