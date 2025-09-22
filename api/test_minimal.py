#!/usr/bin/env python3
"""
Teste dos endpoints de debug
"""

import requests

def test_debug_endpoints():
    """Testar endpoints de debug da versão minimal"""
    
    base_url = "https://dw2-wendel-mab.vercel.app"
    
    print("🔍 TESTE DE DEBUG - API MINIMAL")
    print("=" * 50)
    
    # Teste 1: Endpoint básico
    try:
        print("1️⃣ Testando /api/test...")
        response = requests.get(f"{base_url}/api/test", timeout=10)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print(f"   ✅ Resposta: {response.json()}")
        else:
            print(f"   ❌ Erro: {response.text}")
    except Exception as e:
        print(f"   ❌ Erro: {e}")
    
    # Teste 2: Verificar variáveis de ambiente
    try:
        print("\n2️⃣ Testando /api/env-check...")
        response = requests.get(f"{base_url}/api/env-check", timeout=10)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            env_data = response.json()
            print(f"   📊 Variáveis de ambiente:")
            for key, value in env_data.items():
                print(f"      {key}: {value}")
        else:
            print(f"   ❌ Erro: {response.text}")
    except Exception as e:
        print(f"   ❌ Erro: {e}")
    
    # Teste 3: Testar conexão com banco
    try:
        print("\n3️⃣ Testando /api/db-test...")
        response = requests.get(f"{base_url}/api/db-test", timeout=15)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print(f"   ✅ Conexão com banco: {response.json()}")
        else:
            error_data = response.json() if response.headers.get('content-type') == 'application/json' else response.text
            print(f"   ❌ Erro na conexão: {error_data}")
    except Exception as e:
        print(f"   ❌ Erro: {e}")
    
    print("\n🎯 ANÁLISE:")
    print("- Se /api/test funciona: Deploy OK")
    print("- Se env-check mostra variáveis: Configuração OK") 
    print("- Se db-test funciona: Conexão Supabase OK")

if __name__ == "__main__":
    test_debug_endpoints()