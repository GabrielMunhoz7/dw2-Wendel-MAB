#!/usr/bin/env python3
"""
Script para configurar e migrar para o Supabase
Este script ajuda a configurar a conexão com o Supabase e migrar os dados
"""

import os
import sys
from dotenv import load_dotenv

def check_env_file():
    """Verificar se o arquivo .env existe e está configurado"""
    env_path = ".env"
    
    if not os.path.exists(env_path):
        print("❌ Arquivo .env não encontrado!")
        print("📋 Crie o arquivo .env na pasta api/ com sua DATABASE_URL do Supabase")
        return False
    
    load_dotenv()
    database_url = os.environ.get("DATABASE_URL")
    
    if not database_url or database_url.strip() == "":
        print("❌ DATABASE_URL não configurada no arquivo .env!")
        print("📋 Adicione sua string de conexão do Supabase no arquivo .env")
        print("💡 Exemplo: DATABASE_URL=postgresql://postgres.abc123:senha@db.abc123.supabase.co:5432/postgres")
        return False
    
    if database_url.startswith("sqlite"):
        print("⚠️  Ainda usando SQLite. Configure o Supabase para persistência global!")
        return False
        
    print("✅ Arquivo .env configurado corretamente")
    print(f"🔗 Banco: {database_url.split('@')[1].split('/')[0] if '@' in database_url else 'PostgreSQL'}")
    return True

def test_connection():
    """Testar conexão com o banco"""
    try:
        from database import engine
        from sqlalchemy import text
        
        with engine.connect() as conn:
            result = conn.execute(text("SELECT version()"))
            version = result.fetchone()[0]
            print(f"✅ Conexão bem-sucedida!")
            print(f"🐘 PostgreSQL: {version.split(',')[0]}")
            return True
            
    except Exception as e:
        print(f"❌ Erro na conexão: {e}")
        print("🔧 Verifique:")
        print("   - Se o projeto Supabase está ativo")
        print("   - Se a DATABASE_URL está correta")
        print("   - Se a senha está correta")
        return False

def migrate_to_supabase():
    """Executar migração para o Supabase"""
    print("🚀 Iniciando migração para o Supabase...")
    
    try:
        # Importar após carregar .env
        from database import engine
        from models import Base, User
        import bcrypt
        from sqlalchemy.orm import sessionmaker
        
        # Criar tabelas
        print("🏗️  Criando tabelas no Supabase...")
        Base.metadata.create_all(bind=engine)
        print("✅ Tabelas criadas com sucesso!")
        
        # Criar usuário admin
        print("👤 Criando usuário admin...")
        Session = sessionmaker(bind=engine)
        session = Session()
        
        try:
            admin = session.query(User).filter(User.username == 'admin').first()
            if not admin:
                password_hash = bcrypt.hashpw('admin123'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                admin = User(username='admin', password_hash=password_hash, role='admin')
                session.add(admin)
                session.commit()
                print("✅ Usuário admin criado (username: admin, password: admin123)")
            else:
                print("✅ Usuário admin já existe")
                
        finally:
            session.close()
            
        print("\n🎉 Migração para Supabase concluída!")
        print("📊 Agora seus dados serão persistidos globalmente!")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro na migração: {e}")
        return False

def main():
    """Função principal"""
    print("🔧 Configurador do Supabase para Moedinhas")
    print("=" * 50)
    
    # Passo 1: Verificar arquivo .env
    if not check_env_file():
        print("\n📋 PASSOS PARA CONFIGURAR:")
        print("1. Acesse https://supabase.com/dashboard")
        print("2. Selecione seu projeto (ou crie um novo)")
        print("3. Vá em Settings > Database")
        print("4. Copie a 'Connection string' (PostgreSQL)")
        print("5. Cole no arquivo .env na linha DATABASE_URL=")
        print("6. Execute este script novamente")
        return
    
    # Passo 2: Testar conexão
    print("\n🔍 Testando conexão...")
    if not test_connection():
        return
    
    # Passo 3: Confirmar migração
    print("\n⚠️  ATENÇÃO: Isso criará as tabelas no seu banco Supabase")
    resposta = input("Deseja continuar? (s/N): ").lower().strip()
    
    if resposta in ['s', 'sim', 'y', 'yes']:
        if migrate_to_supabase():
            print("\n🚀 PRONTO! Sua aplicação agora usa persistência global!")
            print("✅ Editar/adicionar/excluir moedas será salvo permanentemente")
            print("🌍 Acessível de qualquer lugar do mundo")
    else:
        print("❌ Migração cancelada")

if __name__ == "__main__":
    main()