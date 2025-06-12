# GitHub Actions 設定ガイド

## 🔐 必要なシークレット設定

GitHub Actions を動作させるために、以下のシークレットをGitHubリポジトリに設定してください。

### 1. VERCEL_TOKEN の取得

1. **Vercel Dashboard** にログイン
2. **Settings** → **Tokens** に移動
3. **Create Token** をクリック
4. トークン名を入力（例: `github-actions`）
5. **Create** をクリック
6. 生成されたトークンをコピー

### 2. VERCEL_ORG_ID の取得

1. **Vercel Dashboard** でプロジェクトを選択
2. **Settings** → **General** に移動
3. **Project Settings** セクション内の **Team ID** をコピー
   （個人アカウントの場合は **User ID**）

### 3. VERCEL_PROJECT_ID の取得

1. 同じ **Settings** → **General** ページで
2. **Project ID** をコピー

## 🛠️ GitHub でのシークレット設定

1. GitHubリポジトリページに移動
2. **Settings** タブをクリック
3. 左サイドバーの **Secrets and variables** → **Actions** をクリック
4. **New repository secret** をクリック
5. 以下の3つのシークレットを作成：

| Name | Value |
|------|-------|
| `VERCEL_TOKEN` | Vercelで生成したトークン |
| `VERCEL_ORG_ID` | VercelのTeam/User ID |
| `VERCEL_PROJECT_ID` | VercelのProject ID |

## 🚀 ワークフロー説明

### deploy.yml（フル機能版）
- **テスト実行**: プッシュ/PR時に自動テスト
- **本番デプロイ**: mainブランチへのプッシュ時
- **プレビューデプロイ**: PR作成時

### simple-deploy.yml（シンプル版）
- **本番デプロイのみ**: mainブランチへのプッシュ時
- **手動実行可能**: GitHub Actionsタブから手動で実行

## 📋 使用方法

### 自動デプロイ
```bash
git add .
git commit -m "Update API"
git push origin main
# → 自動でVercelにデプロイされます
```

### 手動デプロイ
1. GitHubリポジトリの **Actions** タブに移動
2. **Simple Deploy** ワークフローを選択
3. **Run workflow** ボタンをクリック

## 🔍 トラブルシューティング

### よくあるエラー:

**`Error: Vercel token is required`**
→ VERCEL_TOKEN シークレットが設定されていません

**`Error: Project not found`**
→ VERCEL_PROJECT_ID が間違っています

**`Error: Unauthorized`**
→ VERCEL_TOKEN の権限が不足しています

### デバッグ方法:
1. GitHub Actions の **Actions** タブでログを確認
2. Vercel Dashboard でデプロイ状況を確認
3. シークレットの値を再確認

## 🎯 推奨設定

初回は **simple-deploy.yml** を使用して、
慣れてきたら **deploy.yml** に切り替えることをお勧めします。
