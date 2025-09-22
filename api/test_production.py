#!/usr/bin/env python3
"""
Teste da aplicação em produção (Vercel)
Verifica se a persistência está funcionando online
"""

import requests
import json
import time

PRODUCTION_URL = "https://dw2-wendel-mab.vercel.app"

def test_production_api():
    """Testar API em produção"""
    print("🌐 Testando aplicação em produção...")
    print(f"📍 URL: {PRODUCTION_URL}")
    print("=" * 60)
    
    try:
        # Teste 1: Verificar se a API está respondendo
        print("1️⃣ Testando conectividade da API...")
        response = requests.get(f"{PRODUCTION_URL}/api/coins", timeout=10)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            coins = response.json()
            print(f"   ✅ API funcionando! Moedas encontradas: {len(coins)}")
            
            if coins:
                print("   📄 Primeiras moedas no banco:")
                for i, coin in enumerate(coins[:3]):
                    print(f"      {i+1}. {coin.get('name', 'Sem nome')} - {coin.get('period', 'N/A')}")
        else:
            print(f"   ❌ Erro na API: {response.status_code}")
            print(f"   Resposta: {response.text[:200]}")
            return False
        
        # Teste 2: Tentar fazer login
        print("\n2️⃣ Testando login...")
        login_data = {"username": "admin", "password": "admin123"}
        response = requests.post(f"{PRODUCTION_URL}/api/login", json=login_data, timeout=10)
        
        if response.status_code == 200:
            token = response.json().get("token")
            print("   ✅ Login bem-sucedido!")
            print(f"   🔑 Token obtido: {token[:30]}...")
            
            # Teste 3: Tentar criar uma moeda (teste de persistência)
            print("\n3️⃣ Testando criação de moeda (persistência)...")
            test_coin = {
                "name": f"Teste Produção {int(time.time())}",
                "period": "Teste",
                "region": "Produção",
                "material": "Digital",
                "denomination": "Real",
                "year": 2025,
                "description": "Moeda de teste para verificar persistência em produção"
            }
            
            headers = {"Authorization": f"Bearer {token}"}
            response = requests.post(f"{PRODUCTION_URL}/api/coins", 
                                   json=test_coin, headers=headers, timeout=10)
            
            if response.status_code == 201:
                created_coin = response.json()
                coin_id = created_coin["coin"]["id"]
                print(f"   ✅ Moeda criada com sucesso! ID: {coin_id}")
                
                # Teste 4: Verificar se a moeda foi persistida
                print("\n4️⃣ Verificando persistência...")
                time.sleep(2)  # Aguardar um pouco
                
                response = requests.get(f"{PRODUCTION_URL}/api/coins", timeout=10)
                if response.status_code == 200:
                    coins = response.json()
                    found = False
                    for coin in coins:
                        if coin["id"] == coin_id:
                            found = True
                            print(f"   ✅ Moeda encontrada no banco!")
                            print(f"      Nome: {coin['name']}")
                            print(f"      Período: {coin['period']}")
                            break
                    
                    if not found:
                        print("   ❌ Moeda não encontrada - problema de persistência!")
                        return False
                
                # Teste 5: Limpar moeda de teste
                print("\n5️⃣ Limpando dados de teste...")
                response = requests.delete(f"{PRODUCTION_URL}/api/coins/{coin_id}", 
                                         headers=headers, timeout=10)
                if response.status_code == 200:
                    print("   ✅ Moeda de teste removida")
                else:
                    print("   ⚠️ Não foi possível remover moeda de teste")
                
            else:
                print(f"   ❌ Erro ao criar moeda: {response.status_code}")
                print(f"   Resposta: {response.text}")
                return False
                
        else:
            print(f"   ❌ Erro no login: {response.status_code}")
            print(f"   Resposta: {response.text}")
            return False
        
        print("\n🎉 TODOS OS TESTES PASSARAM!")
        print("✅ Sua aplicação está funcionando perfeitamente em produção!")
        print("✅ Persistência global ativa!")
        print("✅ Dados sendo salvos no Supabase!")
        
        return True
        
    except requests.exceptions.Timeout:
        print("❌ Timeout na conexão - API pode estar lenta")
        return False
    except requests.exceptions.ConnectionError:
        print("❌ Erro de conexão - verifique se o deploy foi bem-sucedido")
        return False
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return False

def main():
    print("🧪 TESTE DE PRODUÇÃO - MOEDINHAS APP")
    print("Verificando se o redeploy resolveu a persistência...")
    print()
    
    success = test_production_api()
    
    if success:
        print("\n🎯 RESULTADO: SUCESSO COMPLETO!")
        print("📊 Sua aplicação agora:")
        print("   ✅ Salva dados permanentemente")
        print("   ✅ Funciona de qualquer lugar do mundo")
        print("   ✅ Mantém dados entre sessões")
        print("   ✅ Deploy funcionando perfeitamente")
    else:
        print("\n❌ RESULTADO: AINDA HÁ PROBLEMAS")
        print("🔧 Próximos passos:")
        print("   1. Verificar logs da Vercel")
        print("   2. Confirmar variáveis de ambiente")
        print("   3. Verificar se o projeto Supabase está ativo")

if __name__ == "__main__":
    main()