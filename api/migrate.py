#!/usr/bin/env python3
"""
Script de migração para atualizar o schema do banco de dados
de value/rarity/country para period/region/material
"""

import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from models import Base, Coin, User
from database import DATABASE_URL

def backup_existing_data(engine):
    """Fazer backup dos dados existentes antes da migração"""
    print("📦 Fazendo backup dos dados existentes...")
    
    with engine.connect() as conn:
        try:
            # Verificar se a tabela existe
            result = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table' AND name='coins'"))
            if not result.fetchone():
                print("✅ Tabela 'coins' não existe ainda. Nenhum backup necessário.")
                return []
            
            # Fazer backup dos dados
            backup_data = []
            result = conn.execute(text("SELECT * FROM coins"))
            columns = result.keys()
            
            for row in result:
                backup_data.append(dict(zip(columns, row)))
            
            print(f"✅ Backup concluído: {len(backup_data)} moedas salvas")
            return backup_data
            
        except Exception as e:
            print(f"⚠️  Erro no backup (pode ser normal se a tabela não existir): {e}")
            return []

def migrate_data(engine, backup_data):
    """Migrar dados antigos para o novo formato"""
    if not backup_data:
        print("✅ Nenhum dado para migrar")
        return
    
    print(f"🔄 Migrando {len(backup_data)} moedas para o novo formato...")
    
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        migrated_count = 0
        for old_coin in backup_data:
            # Mapear campos antigos para novos
            new_coin = Coin(
                name=old_coin.get('name', 'Moeda sem nome'),
                period=old_coin.get('country', 'Período não especificado'),  # country -> period
                region=old_coin.get('value', 'Região não especificada'),     # value -> region  
                material=old_coin.get('rarity', 'Material não especificado'), # rarity -> material
                denomination=old_coin.get('denomination', ''),
                year=old_coin.get('year'),
                description=old_coin.get('description', ''),
                historia=old_coin.get('historia', ''),
                contexto=old_coin.get('contexto', ''),
                referencia=old_coin.get('referencia', ''),
                image_front=old_coin.get('image_url', ''),  # image_url -> image_front
                image_back=old_coin.get('image_back', '')
            )
            
            session.add(new_coin)
            migrated_count += 1
        
        session.commit()
        print(f"✅ Migração concluída: {migrated_count} moedas migradas")
        
    except Exception as e:
        session.rollback()
        print(f"❌ Erro na migração: {e}")
        raise
    finally:
        session.close()

def create_fresh_schema(engine):
    """Criar o novo schema do banco"""
    print("🏗️  Criando novo schema do banco...")
    
    # Dropar todas as tabelas existentes
    Base.metadata.drop_all(bind=engine)
    print("✅ Tabelas antigas removidas")
    
    # Criar novas tabelas
    Base.metadata.create_all(bind=engine)
    print("✅ Novas tabelas criadas")

def create_admin_user(engine):
    """Criar usuário admin se não existir"""
    print("👤 Verificando usuário admin...")
    
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        admin = session.query(User).filter(User.username == 'admin').first()
        if not admin:
            import bcrypt
            password_hash = bcrypt.hashpw('admin123'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            admin = User(username='admin', password_hash=password_hash, role='admin')
            session.add(admin)
            session.commit()
            print("✅ Usuário admin criado (username: admin, password: admin123)")
        else:
            print("✅ Usuário admin já existe")
    except Exception as e:
        session.rollback()
        print(f"❌ Erro ao criar admin: {e}")
    finally:
        session.close()

def main():
    """Função principal da migração"""
    print("🚀 Iniciando migração do banco de dados...")
    print(f"📍 Usando banco: {DATABASE_URL}")
    
    if not DATABASE_URL:
        print("❌ DATABASE_URL não configurada!")
        sys.exit(1)
    
    # Conectar ao banco
    try:
        if DATABASE_URL.startswith("sqlite"):
            engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
        else:
            engine = create_engine(DATABASE_URL, pool_pre_ping=True)
        
        print("✅ Conexão com banco estabelecida")
        
        # Testar conexão
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print("✅ Teste de conexão bem-sucedido")
        
    except Exception as e:
        print(f"❌ Erro na conexão: {e}")
        print("🔧 Verifique se o Supabase está ativo e a DATABASE_URL está correta")
        sys.exit(1)
    
    try:
        # Passo 1: Backup
        backup_data = backup_existing_data(engine)
        
        # Passo 2: Recriar schema
        create_fresh_schema(engine)
        
        # Passo 3: Migrar dados
        migrate_data(engine, backup_data)
        
        # Passo 4: Criar admin
        create_admin_user(engine)
        
        print("\n🎉 Migração concluída com sucesso!")
        print("📋 Resumo:")
        print(f"   - {len(backup_data)} moedas migradas")
        print("   - Novo schema aplicado")
        print("   - Usuário admin configurado")
        print("\n🚀 Você pode agora testar adicionar/excluir moedas!")
        
    except Exception as e:
        print(f"\n❌ Erro durante a migração: {e}")
        print("🔧 Verifique os logs acima para mais detalhes")
        sys.exit(1)

if __name__ == "__main__":
    main()