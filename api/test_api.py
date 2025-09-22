import requests
import json

# Testar API
base_url = "http://localhost:5000/api"

def test_api():
    print("🧪 Testando API...")
    
    try:
        # Teste 1: Listar moedas
        print("1️⃣ Testando GET /api/coins...")
        response = requests.get(f"{base_url}/coins")
        print(f"   Status: {response.status_code}")
        print(f"   Resposta: {response.json()}")
        
        # Teste 2: Login
        print("\n2️⃣ Testando login...")
        login_data = {"username": "admin", "password": "admin123"}
        response = requests.post(f"{base_url}/login", json=login_data)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            token = response.json().get("token")
            print(f"   Token obtido: {token[:50]}...")
            
            # Teste 3: Criar moeda
            print("\n3️⃣ Testando POST /api/coins...")
            coin_data = {
                "name": "Moeda de Teste",
                "period": "Romano",
                "region": "Europa",
                "material": "Ouro",
                "denomination": "Aureus",
                "year": 100,
                "description": "Moeda de teste da migração"
            }
            
            headers = {"Authorization": f"Bearer {token}"}
            response = requests.post(f"{base_url}/coins", json=coin_data, headers=headers)
            print(f"   Status: {response.status_code}")
            print(f"   Resposta: {response.json()}")
            
            if response.status_code == 201:
                coin_id = response.json()["coin"]["id"]
                
                # Teste 4: Listar moedas novamente
                print("\n4️⃣ Testando GET /api/coins (com dados)...")
                response = requests.get(f"{base_url}/coins")
                coins = response.json()
                print(f"   Status: {response.status_code}")
                print(f"   Total de moedas: {len(coins)}")
                if coins:
                    print(f"   Primeira moeda: {coins[0]['name']}")
                
                # Teste 5: Deletar moeda
                print("\n5️⃣ Testando DELETE /api/coins...")
                response = requests.delete(f"{base_url}/coins/{coin_id}", headers=headers)
                print(f"   Status: {response.status_code}")
                print(f"   Resposta: {response.json()}")
        
        print("\n✅ Testes concluídos!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Erro: Não foi possível conectar à API. Certifique-se de que o servidor está rodando.")
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    test_api()