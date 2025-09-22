#!/usr/bin/env python3
"""
Script de diagnóstico para verificar problemas na Vercel
"""

import os
import sys

def check_environment():
    """Verificar variáveis de ambiente"""
    print("🔍 Diagnóstico da Aplicação")
    print("=" * 40)
    
    print("📋 Variáveis de ambiente necessárias:")
    
    required_vars = [
        "DATABASE_URL",
        "SECRET_KEY", 
        "ALLOWED_ORIGINS"
    ]
    
    for var in required_vars:
        value = os.environ.get(var)
        if value:
            # Mascarar dados sensíveis
            if "DATABASE_URL" in var:
                masked = value[:20] + "..." + value[-10:] if len(value) > 30 else value
                print(f"   ✅ {var}: {masked}")
            else:
                print(f"   ✅ {var}: {value}")
        else:
            print(f"   ❌ {var}: NÃO CONFIGURADA")

def check_imports():
    """Verificar se as importações funcionam"""
    print("\n📦 Verificando importações:")
    
    try:
        import flask
        print(f"   ✅ Flask: {flask.__version__}")
    except ImportError as e:
        print(f"   ❌ Flask: {e}")
    
    try:
        import sqlalchemy
        print(f"   ✅ SQLAlchemy: {sqlalchemy.__version__}")
    except ImportError as e:
        print(f"   ❌ SQLAlchemy: {e}")
    
    try:
        import psycopg2
        print(f"   ✅ psycopg2: disponível")
    except ImportError as e:
        print(f"   ❌ psycopg2: {e}")
    
    try:
        from dotenv import load_dotenv
        print(f"   ✅ python-dotenv: disponível")
    except ImportError as e:
        print(f"   ❌ python-dotenv: {e}")

def test_database_connection():
    """Testar conexão com banco"""
    print("\n🔗 Testando conexão com banco:")
    
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        from database import engine
        from sqlalchemy import text
        
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("   ✅ Conexão com banco funcionando!")
            return True
            
    except Exception as e:
        print(f"   ❌ Erro na conexão: {e}")
        return False

def main():
    """Função principal"""
    check_environment()
    check_imports() 
    test_database_connection()
    
    print("\n🎯 SUGESTÕES:")
    print("1. Verifique os logs da Vercel para mais detalhes")
    print("2. Confirme se todas as variáveis estão corretas")
    print("3. Verifique se o projeto Supabase está ativo")

if __name__ == "__main__":
    main()