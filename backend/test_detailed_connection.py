import os
import psycopg2
import socket
from dotenv import load_dotenv
from urllib.parse import urlparse

load_dotenv()

def test_detailed_connection():
    print("🔄 Teste detalhado de conectividade...")
    
    database_url = os.getenv('DATABASE_URL')
    print(f"📋 URL do banco: {database_url}")
    
    # Parse da URL
    parsed = urlparse(database_url)
    host = parsed.hostname
    port = parsed.port or 5432
    
    print(f"🌐 Host: {host}")
    print(f"🔌 Porta: {port}")
    
    # Teste de socket primeiro
    print("\n🔍 Testando resolução DNS...")
    try:
        ip = socket.gethostbyname(host)
        print(f"✅ DNS resolvido: {host} -> {ip}")
    except socket.gaierror as e:
        print(f"❌ Erro de DNS: {e}")
        print("💡 Tentando com timeout maior...")
        
        # Configurar timeout maior
        socket.setdefaulttimeout(30)
        try:
            ip = socket.gethostbyname(host)
            print(f"✅ DNS resolvido com timeout maior: {host} -> {ip}")
        except Exception as e2:
            print(f"❌ Erro persistente de DNS: {e2}")
            return
    
    # Teste de conectividade de socket
    print(f"\n🔌 Testando conectividade TCP para {host}:{port}...")
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(30)
        result = sock.connect_ex((host, port))
        sock.close()
        
        if result == 0:
            print("✅ Conectividade TCP funcionando!")
        else:
            print(f"❌ Erro de conectividade TCP: código {result}")
            return
    except Exception as e:
        print(f"❌ Erro no teste TCP: {e}")
        return
    
    # Teste de conexão PostgreSQL
    print("\n🐘 Testando conexão PostgreSQL...")
    try:
        conn = psycopg2.connect(
            database_url,
            connect_timeout=30,
            keepalives=1,
            keepalives_idle=30,
            keepalives_interval=10,
            keepalives_count=5
        )
        cursor = conn.cursor()
        
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print(f"✅ Conectado com sucesso! Versão: {version[0][:50]}...")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Erro na conexão PostgreSQL: {e}")
        print(f"🔍 Tipo do erro: {type(e).__name__}")

if __name__ == "__main__":
    test_detailed_connection()