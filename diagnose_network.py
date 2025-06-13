#!/usr/bin/env python3
"""
ネットワーク診断スクリプト
"""
import socket
import subprocess
import os

def run_command(cmd):
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10)
        return result.stdout.strip()
    except Exception as e:
        return f"Error: {e}"

def diagnose_network():
    print("🔍 ネットワーク診断を開始...")
    print("=" * 50)
    
    # 1. 基本接続テスト
    print("\n1️⃣ 基本接続テスト:")
    
    # Google DNS ping
    result = run_command("ping -c 3 8.8.8.8")
    if "3 packets transmitted, 3 received" in result:
        print("  ✅ インターネット接続: OK")
    else:
        print("  ❌ インターネット接続: NG")
        print(f"  詳細: {result}")
    
    # 2. DNS解決テスト
    print("\n2️⃣ DNS解決テスト:")
    
    test_domains = [
        "google.com",
        "supabase.com", 
        "hmcqevbuwcnfqmfobnfo.supabase.com"
    ]
    
    for domain in test_domains:
        try:
            ip = socket.gethostbyname(domain)
            print(f"  ✅ {domain} -> {ip}")
        except Exception as e:
            print(f"  ❌ {domain} -> {e}")
    
    # 3. DNS設定確認
    print("\n3️⃣ DNS設定:")
    
    dns_servers = run_command("scutil --dns | grep nameserver")
    print(f"  現在のDNSサーバー:")
    for line in dns_servers.split('\n'):
        if 'nameserver' in line:
            print(f"    {line.strip()}")
    
    # 4. nslookup テスト
    print("\n4️⃣ nslookup テスト:")
    nslookup_result = run_command("nslookup hmcqevbuwcnfqmfobnfo.supabase.com")
    if "NXDOMAIN" in nslookup_result:
        print("  ❌ nslookup: ドメインが見つかりません")
    elif "Name:" in nslookup_result:
        print("  ✅ nslookup: 成功")
    else:
        print(f"  ⚠️ nslookup結果: {nslookup_result}")
    
    # 5. プロキシ設定確認
    print("\n5️⃣ プロキシ設定:")
    proxy_vars = ['http_proxy', 'https_proxy', 'HTTP_PROXY', 'HTTPS_PROXY']
    proxy_found = False
    for var in proxy_vars:
        value = os.environ.get(var)
        if value:
            print(f"  📡 {var}: {value}")
            proxy_found = True
    
    if not proxy_found:
        print("  ✅ プロキシ設定なし")
    
    print("\n" + "=" * 50)
    print("🔍 診断完了")

if __name__ == "__main__":
    diagnose_network()
