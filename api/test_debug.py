#!/usr/bin/env python3
"""
Teste rápido dos endpoints de debug
"""

import requests

def test_debug_endpoints():
    """Testar endpoints de debug"""
    base_url = "https://dw2-wendel-mab.vercel.app"
    
    print("🔍 Testando endpoints de debug...")
    
    # Teste 1: Health check
    try:
        print("\n1️⃣ Testando /api/health...")
        response = requests.get(f"{base_url}/api/health", timeout=10)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print(f"   Resposta: {response.json()}")
        else:
            print(f"   Erro: {response.text}")
    except Exception as e:
        print(f"   ❌ Erro: {e}")
    
    # Teste 2: Debug endpoint
    try:
        print("\n2️⃣ Testando /api/debug...")
        response = requests.get(f"{base_url}/api/debug", timeout=10)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            debug_info = response.json()
            print(f"   📊 Info de debug:")
            for key, value in debug_info.items():
                print(f"      {key}: {value}")
        else:
            print(f"   Erro: {response.text}")
    except Exception as e:
        print(f"   ❌ Erro: {e}")
    
    # Teste 3: Endpoint principal
    try:
        print("\n3️⃣ Testando /api/coins...")
        response = requests.get(f"{base_url}/api/coins", timeout=10)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            coins = response.json()
            print(f"   ✅ API funcionando! Total de moedas: {len(coins)}")
        else:
            print(f"   Erro: {response.text}")
    except Exception as e:
        print(f"   ❌ Erro: {e}")

if __name__ == "__main__":
    test_debug_endpoints()