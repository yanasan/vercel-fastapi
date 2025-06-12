# uvicorn コマンドオプション詳細

## 基本的な使用方法

```bash
uvicorn main:app
```

## よく使用するオプション

### ホストとポート設定
```bash
# すべてのIPアドレスでリッスン
uvicorn main:app --host 0.0.0.0

# ポート指定
uvicorn main:app --port 8000

# ホストとポート両方指定
uvicorn main:app --host 0.0.0.0 --port 8000
```

### 開発用オプション
```bash
# 自動リロード（ファイル変更時に自動再起動）
uvicorn main:app --reload

# 監視するディレクトリ指定
uvicorn main:app --reload --reload-dir ./src

# 特定の拡張子のみ監視
uvicorn main:app --reload --reload-include "*.py"

# 特定のファイルを監視対象から除外
uvicorn main:app --reload --reload-exclude "*.log"
```

### 本番用オプション
```bash
# マルチワーカー（CPUコア数に応じて調整）
uvicorn main:app --workers 4

# ワーカープロセスクラス指定
uvicorn main:app --worker-class uvicorn.workers.UvicornWorker
```

### ログ設定
```bash
# ログレベル設定
uvicorn main:app --log-level debug    # debug, info, warning, error, critical
uvicorn main:app --log-level info
uvicorn main:app --log-level warning

# アクセスログ無効化
uvicorn main:app --no-access-log

# ログ設定ファイル使用
uvicorn main:app --log-config logging.conf
```

### SSL/TLS設定
```bash
# SSL証明書使用
uvicorn main:app --ssl-keyfile ./key.pem --ssl-certfile ./cert.pem

# 自己署名証明書でHTTPS
uvicorn main:app --ssl-keyfile ./key.pem --ssl-certfile ./cert.pem --port 443
```

### パフォーマンス設定
```bash
# 接続制限
uvicorn main:app --limit-concurrency 1000

# 最大リクエストサイズ
uvicorn main:app --limit-max-requests 1000

# ワーカー毎の最大リクエスト数（メモリリーク防止）
uvicorn main:app --max-requests 1000

# リクエスト間のジッター追加
uvicorn main:app --max-requests-jitter 100
```

### その他便利なオプション
```bash
# 設定ファイルから読み込み
uvicorn main:app --config ./uvicorn.conf

# デーモン化（バックグラウンド実行）
uvicorn main:app --daemon

# プロセスファイル作成
uvicorn main:app --pid-file ./uvicorn.pid

# 詳細ヘルプ表示
uvicorn --help
```

## 設定ファイル例（uvicorn.conf）

```ini
# uvicorn.conf
host = 0.0.0.0
port = 8000
workers = 4
log_level = info
access_log = true
reload = false
```

## 環境変数での設定

```bash
# 環境変数で設定も可能
export UVICORN_HOST=0.0.0.0
export UVICORN_PORT=8000
export UVICORN_LOG_LEVEL=info

uvicorn main:app
```

## 開発・本番での推奨設定

### 開発環境
```bash
uvicorn main:app \
  --host 0.0.0.0 \
  --port 8000 \
  --reload \
  --log-level debug \
  --access-log
```

### 本番環境
```bash
uvicorn main:app \
  --host 0.0.0.0 \
  --port 8000 \
  --workers 4 \
  --log-level warning \
  --no-access-log \
  --limit-concurrency 1000
```
