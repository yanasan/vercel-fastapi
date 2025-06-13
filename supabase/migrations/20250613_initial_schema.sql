-- 初期スキーマ作成
-- vercel-fastapi用の基本テーブル

-- ユーザーテーブル作成
CREATE TABLE IF NOT EXISTS public.users (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- メッセージテーブル作成
CREATE TABLE IF NOT EXISTS public.messages (
    id BIGSERIAL PRIMARY KEY,
    message TEXT NOT NULL,
    user_id BIGINT REFERENCES public.users(id) ON DELETE SET NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- インデックス作成
CREATE INDEX IF NOT EXISTS idx_users_email ON public.users(email);
CREATE INDEX IF NOT EXISTS idx_messages_user_id ON public.messages(user_id);
CREATE INDEX IF NOT EXISTS idx_messages_created_at ON public.messages(created_at DESC);

-- updated_at自動更新用のトリガー関数
CREATE OR REPLACE FUNCTION public.update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- トリガー作成（IF NOT EXISTSは使用できないため、DROP IF EXISTSを使用）
DROP TRIGGER IF EXISTS update_users_updated_at ON public.users;
CREATE TRIGGER update_users_updated_at 
    BEFORE UPDATE ON public.users
    FOR EACH ROW 
    EXECUTE FUNCTION public.update_updated_at_column();

DROP TRIGGER IF EXISTS update_messages_updated_at ON public.messages;
CREATE TRIGGER update_messages_updated_at 
    BEFORE UPDATE ON public.messages
    FOR EACH ROW 
    EXECUTE FUNCTION public.update_updated_at_column();

-- RLS（Row Level Security）を無効化（開発環境用）
ALTER TABLE public.users DISABLE ROW LEVEL SECURITY;
ALTER TABLE public.messages DISABLE ROW LEVEL SECURITY;

-- コメント追加
COMMENT ON TABLE public.users IS 'ユーザー情報テーブル';
COMMENT ON TABLE public.messages IS 'メッセージテーブル';

COMMENT ON COLUMN public.users.id IS 'ユーザーID';
COMMENT ON COLUMN public.users.name IS 'ユーザー名';
COMMENT ON COLUMN public.users.email IS 'メールアドレス';
COMMENT ON COLUMN public.users.created_at IS '作成日時';
COMMENT ON COLUMN public.users.updated_at IS '更新日時';

COMMENT ON COLUMN public.messages.id IS 'メッセージID';
COMMENT ON COLUMN public.messages.message IS 'メッセージ内容';
COMMENT ON COLUMN public.messages.user_id IS 'ユーザーID（外部キー）';
COMMENT ON COLUMN public.messages.created_at IS '作成日時';
COMMENT ON COLUMN public.messages.updated_at IS '更新日時';
