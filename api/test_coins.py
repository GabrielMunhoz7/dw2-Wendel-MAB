#!/usr/bin/env python3

import requests

def test_coins_endpoint():
    """Testar diretamente o endpoint de moedas"""
    
    base_url = "https://dw2-wendel-mab.vercel.app"
    
    print("🪙 TESTE DIRETO DO ENDPOINT DE MOEDAS")
    print("=" * 50)
    
    # Teste 1: Verificar se API está funcionando
    try:
        print("1️⃣ Testando /api/test...")
        response = requests.get(f"{base_url}/api/test", timeout=10)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ API Status: {data}")
        else:
            print(f"   ❌ Erro: {response.text}")
    except Exception as e:
        print(f"   ❌ Erro: {e}")
    
    # Teste 2: Buscar moedas
    try:
        print("\n2️⃣ Testando /api/coins...")
        response = requests.get(f"{base_url}/api/coins", timeout=15)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            coins = response.json()
            print(f"   ✅ Total de moedas encontradas: {len(coins)}")
            
            if coins:
                for i, coin in enumerate(coins, 1):
                    print(f"   📍 Moeda {i}: {coin.get('name', 'Sem nome')}")
                    print(f"      - Período: {coin.get('period', 'N/A')}")
                    print(f"      - Região: {coin.get('region', 'N/A')}")
                    print(f"      - Material: {coin.get('material', 'N/A')}")
                print("\n   🎉 SUCESSO! As moedas estão sendo retornadas pela API!")
            else:
                print("   ⚠️ Nenhuma moeda encontrada (array vazio)")
                
        else:
            print(f"   ❌ Erro: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Erro: {e}")

if __name__ == "__main__":
    test_coins_endpoint()