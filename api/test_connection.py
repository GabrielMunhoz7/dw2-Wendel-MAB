#!/usr/bin/env python3
"""
Teste de conexão com banco - Local vs Produção
"""

import requests
import time

def test_database_connection():
    """Verificar se a aplicação está usando o banco correto"""
    
    print("🔍 INVESTIGAÇÃO: Banco Local vs Supabase")
    print("=" * 50)
    
    # URL da aplicação em produção
    prod_url = "https://dw2-wendel-mab.vercel.app"
    
    print("📊 Dados que vemos no Supabase:")
    print("   1. Denário de Tibério - Império Romano - Palestina - Prata")
    print("   2. Lepton da Viúva - Segundo Templo - Jerusalém - Bronze")
    
    print(f"\n🌐 Testando aplicação em: {prod_url}")
    
    try:
        # Testar endpoint de moedas
        response = requests.get(f"{prod_url}/api/coins", timeout=15)
        
        if response.status_code == 200:
            coins = response.json()
            print(f"\n✅ API respondeu! Total de moedas retornadas: {len(coins)}")
            
            if len(coins) == 0:
                print("\n❌ PROBLEMA IDENTIFICADO:")
                print("   - Supabase tem 2 moedas")
                print("   - API retorna 0 moedas")
                print("   - CONCLUSÃO: API não está conectada ao Supabase!")
                
            elif len(coins) == 2:
                print("\n✅ TUDO FUNCIONANDO:")
                print("   - Supabase tem 2 moedas")
                print("   - API retorna 2 moedas")
                print("   - CONCLUSÃO: Conexão OK!")
                
                print("\n📄 Moedas retornadas pela API:")
                for i, coin in enumerate(coins, 1):
                    print(f"   {i}. {coin.get('name', 'N/A')} - {coin.get('period', 'N/A')} - {coin.get('region', 'N/A')}")
                    
            else:
                print(f"\n⚠️ INCONSISTÊNCIA:")
                print(f"   - Supabase tem 2 moedas")
                print(f"   - API retorna {len(coins)} moedas")
                print("   - Possível problema de sincronização")
                
        elif response.status_code == 500:
            print(f"\n❌ ERRO 500 - Problema na API")
            print("   - API não consegue se conectar ao banco")
            print("   - Verifique variáveis de ambiente na Vercel")
            
        else:
            print(f"\n❌ Erro {response.status_code}: {response.text}")
            
    except requests.exceptions.Timeout:
        print("\n❌ Timeout - API muito lenta ou não respondendo")
    except requests.exceptions.ConnectionError:
        print("\n❌ Erro de conexão - API não disponível")
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
    
    print("\n🎯 PRÓXIMOS PASSOS:")
    print("1. Se API retorna 0 moedas: Problema de variáveis de ambiente")
    print("2. Se API retorna erro 500: Problema de configuração")
    print("3. Se API não responde: Problema de deploy")

def test_specific_endpoints():
    """Testar endpoints específicos para debug"""
    base_url = "https://dw2-wendel-mab.vercel.app"
    
    print(f"\n🔧 Testando endpoints específicos...")
    
    # Teste health check simples
    try:
        print("\n🔍 Testando endpoint raiz...")
        response = requests.get(f"{base_url}/", timeout=10)
        print(f"   Status: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Erro: {e}")

if __name__ == "__main__":
    test_database_connection()
    test_specific_endpoints()