import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def test_connection():
    print("🔄 Testando conexão com Supabase...")
    
    database_url = os.getenv('DATABASE_URL')
    print(f"📋 URL do banco: {database_url}")
    
    try:
        # Tentar conectar
        print("🔗 Tentando conectar...")
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor()
        
        # Testar uma query simples
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print(f"✅ Conectado com sucesso! Versão do PostgreSQL: {version[0]}")
        
        # Verificar se as tabelas existem
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        """)
        tables = cursor.fetchall()
        print(f"📋 Tabelas encontradas: {[table[0] for table in tables]}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Erro na conexão: {e}")
        print(f"🔍 Tipo do erro: {type(e).__name__}")

if __name__ == "__main__":
    test_connection()