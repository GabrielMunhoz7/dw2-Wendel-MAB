#!/usr/bin/env python3
"""
Teste direto de persistência no Supabase
"""

import os
from dotenv import load_dotenv

# Carregar .env
load_dotenv()

def test_database_operations():
    """Testar operações CRUD diretamente no banco"""
    print("🧪 Testando persistência no Supabase...")
    
    try:
        from database import SessionLocal
        from models import Coin
        import datetime
        
        # Criar sessão
        db = SessionLocal()
        
        # Teste 1: Criar moeda
        print("\n1️⃣ Testando criação de moeda...")
        test_coin = Coin(
            name="Moeda Teste Persistência",
            period="Romano",
            region="Europa",
            material="Ouro",
            denomination="Aureus",
            year=100,
            description="Teste de persistência global"
        )
        
        db.add(test_coin)
        db.commit()
        db.refresh(test_coin)
        coin_id = test_coin.id
        print(f"✅ Moeda criada com ID: {coin_id}")
        
        # Teste 2: Buscar moeda
        print("\n2️⃣ Testando busca de moeda...")
        found_coin = db.query(Coin).filter(Coin.id == coin_id).first()
        if found_coin:
            print(f"✅ Moeda encontrada: {found_coin.name}")
            print(f"   Período: {found_coin.period}")
            print(f"   Região: {found_coin.region}")
            print(f"   Material: {found_coin.material}")
        else:
            print("❌ Moeda não encontrada")
        
        # Teste 3: Listar todas as moedas
        print("\n3️⃣ Testando listagem...")
        all_coins = db.query(Coin).all()
        print(f"✅ Total de moedas no banco: {len(all_coins)}")
        
        # Teste 4: Atualizar moeda
        print("\n4️⃣ Testando atualização...")
        found_coin.description = "Atualizada via teste de persistência"
        db.commit()
        print("✅ Moeda atualizada")
        
        # Teste 5: Deletar moeda de teste
        print("\n5️⃣ Testando exclusão...")
        db.delete(found_coin)
        db.commit()
        print("✅ Moeda de teste removida")
        
        # Fechar sessão
        db.close()
        
        print("\n🎉 TODOS OS TESTES PASSARAM!")
        print("✅ Persistência global funcionando perfeitamente")
        print("🌍 Suas alterações de moedas serão salvas permanentemente")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro nos testes: {e}")
        return False

def verify_connection():
    """Verificar se a conexão está funcionando"""
    try:
        from database import engine
        from sqlalchemy import text
        
        with engine.connect() as conn:
            result = conn.execute(text("SELECT current_database(), version()"))
            db_info = result.fetchone()
            print(f"✅ Conectado ao banco: {db_info[0]}")
            print(f"✅ PostgreSQL: {db_info[1].split(',')[0]}")
            return True
    except Exception as e:
        print(f"❌ Erro na conexão: {e}")
        return False

def main():
    print("🔍 Verificando persistência no Supabase")
    print("=" * 50)
    
    # Verificar conexão
    if not verify_connection():
        return
    
    # Executar testes
    test_database_operations()

if __name__ == "__main__":
    main()