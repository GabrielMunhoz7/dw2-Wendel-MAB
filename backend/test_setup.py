import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def test_and_setup():
    print("🔄 Testando conexão e configurando banco...")
    
    try:
        # Conectar ao PostgreSQL (Supabase)
        print("☁️ Conectando ao Supabase...")
        pg_conn = psycopg2.connect(os.getenv('DATABASE_URL'))
        pg_cursor = pg_conn.cursor()
        
        # Testar conexão
        pg_cursor.execute("SELECT version();")
        version = pg_cursor.fetchone()
        print(f"✅ Conectado! Versão: {version[0][:50]}...")
        
        # Criar tabelas se não existirem
        print("📋 Criando tabelas...")
        create_tables_sql = """
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(255) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            role VARCHAR(50) DEFAULT 'user',
            created_at TIMESTAMP DEFAULT NOW()
        );

        CREATE TABLE IF NOT EXISTS coins (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            period VARCHAR(255),
            region VARCHAR(255),
            material VARCHAR(255),
            denomination VARCHAR(255),
            year VARCHAR(255),
            description TEXT,
            historia TEXT,
            contexto TEXT,
            referencia TEXT,
            image_front VARCHAR(500),
            image_back VARCHAR(500),
            created_by INTEGER REFERENCES users(id),
            created_at TIMESTAMP DEFAULT NOW(),
            updated_at TIMESTAMP DEFAULT NOW()
        );
        """
        
        pg_cursor.execute(create_tables_sql)
        pg_conn.commit()
        print("✅ Tabelas criadas/verificadas!")
        
        # Verificar se já existem dados
        pg_cursor.execute("SELECT COUNT(*) FROM users")
        user_count = pg_cursor.fetchone()[0]
        
        pg_cursor.execute("SELECT COUNT(*) FROM coins") 
        coin_count = pg_cursor.fetchone()[0]
        
        print(f"📊 Usuários existentes: {user_count}")
        print(f"📊 Moedas existentes: {coin_count}")
        
        pg_cursor.close()
        pg_conn.close()
        
        print("✅ Configuração concluída com sucesso!")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        print(f"Tipo do erro: {type(e).__name__}")

if __name__ == "__main__":
    test_and_setup()