#!/usr/bin/env python3

import requests

def test_ultra_simple():
    """Testar API ultra-simples"""
    
    base_url = "https://dw2-wendel-mab.vercel.app"
    
    print("🔧 TESTE ULTRA-SIMPLES")
    print("=" * 30)
    
    try:
        print("📡 Testando /api/test...")
        response = requests.get(f"{base_url}/api/test", timeout=10)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            print(f"   ✅ Sucesso: {response.json()}")
            print("   🎉 API está respondendo!")
        else:
            print(f"   ❌ Erro: {response.text}")
            print("   🔍 Problema pode ser na configuração do Vercel")
            
    except Exception as e:
        print(f"   ❌ Erro de conexão: {e}")

if __name__ == "__main__":
    test_ultra_simple()