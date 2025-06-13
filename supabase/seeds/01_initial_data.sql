-- 初期ユーザーデータ
INSERT INTO public.users (name, email, created_at) VALUES 
    ('太郎', 'taro@example.com', NOW()),
    ('花子', 'hanako@example.com', NOW()),
    ('次郎', 'jiro@example.com', NOW()),
    ('三郎', 'saburo@example.com', NOW())
ON CONFLICT (email) DO NOTHING;

-- 初期メッセージデータ
INSERT INTO public.messages (message, user_id, created_at) VALUES 
    ('こんにちは！', 1, NOW()),
    ('はじめまして', 2, NOW()),
    ('よろしくお願いします', 1, NOW()),
    ('FastAPI + Supabaseのテストです', 3, NOW()),
    ('マイグレーション成功！', 4, NOW())
ON CONFLICT DO NOTHING;
