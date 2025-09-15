import psycopg2
import os
from dotenv import load_dotenv
import socket

load_dotenv()

def test_dns_resolution():
    """Testar se conseguimos resolver o DNS do Supabase"""
    print("🔍 Testando resolução DNS...")
    
    # Extrair hostname da DATABASE_URL
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        print("❌ DATABASE_URL não encontrada no .env")
        return False
    
    print(f"📋 DATABASE_URL: {database_url[:50]}...")
    
    # Extrair hostname
    try:
        if '@' in database_url:
            # Formato: postgresql://user:pass@host:port/db
            hostname = database_url.split('@')[1].split(':')[0]
        else:
            print("❌ Formato de URL inválido")
            return False
        
        print(f"🌐 Hostname extraído: {hostname}")
        
        # Testar resolução DNS
        try:
            ip = socket.gethostbyname(hostname)
            print(f"✅ DNS resolvido: {hostname} → {ip}")
            return True
        except socket.gaierror as e:
            print(f"❌ Erro DNS: {e}")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao extrair hostname: {e}")
        return False

def test_connection_variations():
    """Testar diferentes formatos de conexão"""
    print("\n🔄 Testando variações de conexão...")
    
    # Configurações base
    base_config = {
        'host': 'db.hphxswhwwfxvxxylhmhm.supabase.co',
        'database': 'postgres',
        'user': 'postgres',
        'password': 'MabCoins73!',
        'port': 5432
    }
    
    # Testar com pooler
    pooler_config = base_config.copy()
    pooler_config['port'] = 6543
    
    # Testar diferentes configurações
    configs = [
        ("Conexão direta (porta 5432)", base_config),
        ("Conexão pooler (porta 6543)", pooler_config),
    ]
    
    for name, config in configs:
        print(f"\n📡 {name}:")
        try:
            conn = psycopg2.connect(**config)
            cursor = conn.cursor()
            cursor.execute("SELECT version();")
            version = cursor.fetchone()[0]
            print(f"✅ SUCESSO! Versão: {version[:50]}...")
            cursor.close()
            conn.close()
            return config
        except Exception as e:
            print(f"❌ Erro: {e}")
    
    return None

def test_with_ssl_modes():
    """Testar com diferentes modos SSL"""
    print("\n🔒 Testando configurações SSL...")
    
    base_config = {
        'host': 'db.hphxswhwwfxvxxylhmhm.supabase.co',
        'database': 'postgres',
        'user': 'postgres',
        'password': 'MabCoins73!',
        'port': 5432
    }
    
    ssl_modes = [
        ('require', {'sslmode': 'require'}),
        ('prefer', {'sslmode': 'prefer'}),
        ('disable', {'sslmode': 'disable'}),
        ('sem SSL', {})
    ]
    
    for name, ssl_config in ssl_modes:
        config = {**base_config, **ssl_config}
        print(f"🔐 Testando SSL {name}:")
        try:
            conn = psycopg2.connect(**config)
            cursor = conn.cursor()
            cursor.execute("SELECT 1;")
            result = cursor.fetchone()
            print(f"✅ SSL {name} funcionou!")
            cursor.close()
            conn.close()
            return config
        except Exception as e:
            print(f"❌ SSL {name}: {e}")
    
    return None

def generate_new_database_url(config):
    """Gerar nova DATABASE_URL baseada na configuração que funcionou"""
    if not config:
        return None
    
    ssl_part = f"?sslmode={config['sslmode']}" if 'sslmode' in config else ""
    
    new_url = f"postgresql://{config['user']}:{config['password']}@{config['host']}:{config['port']}/{config['database']}{ssl_part}"
    
    return new_url

def main():
    print("🔍 DIAGNÓSTICO COMPLETO DO SUPABASE")
    print("=" * 50)
    
    # Teste 1: DNS
    dns_ok = test_dns_resolution()
    
    if not dns_ok:
        print("\n❌ Problema de DNS detectado!")
        print("🔧 Soluções possíveis:")
        print("1. Verificar se o projeto Supabase não está pausado")
        print("2. Confirmar se a URL está correta no dashboard")
        print("3. Tentar com VPN se houver bloqueio regional")
        return
    
    # Teste 2: Variações de porta
    working_config = test_connection_variations()
    
    if not working_config:
        # Teste 3: SSL
        working_config = test_with_ssl_modes()
    
    if working_config:
        print("\n🎉 CONFIGURAÇÃO QUE FUNCIONA ENCONTRADA!")
        print(f"📋 Configuração: {working_config}")
        
        new_url = generate_new_database_url(working_config)
        print(f"\n🔧 NOVA DATABASE_URL:")
        print(f"{new_url}")
        print("\n📝 Copie esta URL e substitua no seu arquivo .env")
        
    else:
        print("\n❌ Nenhuma configuração funcionou")
        print("🔧 Próximos passos:")
        print("1. Verificar credenciais no dashboard Supabase")
        print("2. Confirmar se o projeto não está pausado")
        print("3. Verificar firewall/antivírus")

if __name__ == "__main__":
    main()