#!/usr/bin/env python3
"""
Supabaseテーブル確認スクリプト
"""
import os
from dotenv import load_dotenv
from supabase import create_client, Client

# 環境変数読み込み
load_dotenv()

def main():
    # 環境変数取得
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    
    if not url or not key:
        print("❌ 環境変数が設定されていません")
        print("SUPABASE_URL:", "✅" if url else "❌")
        print("SUPABASE_KEY:", "✅" if key else "❌")
        return
    
    print(f"🔗 Supabase URL: {url[:30]}...")
    print(f"🔑 API Key: {key[:20]}...")
    
    # クライアント作成
    try:
        supabase: Client = create_client(url, key)
        print("✅ Supabaseクライアント作成成功")
    except Exception as e:
        print(f"❌ クライアント作成失敗: {e}")
        return
    
    # テーブル確認
    tables_to_check = ["users", "messages"]
    
    for table_name in tables_to_check:
        print(f"\n📋 テーブル '{table_name}' の確認:")
        
        try:
            # レコード数取得
            response = supabase.table(table_name).select("count", count="exact").execute()
            count = response.count
            print(f"  ✅ 存在: はい")
            print(f"  📊 レコード数: {count}")
            
            # 最初の数件を取得
            if count > 0:
                sample_response = supabase.table(table_name).select("*").limit(3).execute()
                print(f"  📄 サンプルデータ:")
                for i, record in enumerate(sample_response.data[:3], 1):
                    print(f"    {i}. {record}")
            else:
                print("  📄 データは空です")
                
        except Exception as e:
            print(f"  ❌ 存在: いいえ")
            print(f"  ⚠️  エラー: {e}")
    
    # カラム情報取得（テーブルが存在する場合）
    print(f"\n🔍 usersテーブルの構造確認:")
    try:
        # 空のクエリでカラム情報を確認
        response = supabase.table("users").select("*").limit(1).execute()
        if response.data:
            print("  📝 カラム:")
            for key in response.data[0].keys():
                print(f"    - {key}")
        else:
            print("  📝 データがないためカラム情報を取得できません")
    except Exception as e:
        print(f"  ❌ 構造確認失敗: {e}")

if __name__ == "__main__":
    main()
