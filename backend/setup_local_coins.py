import sqlite3
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def check_supabase_connectivity():
    """Verifica se conseguimos conectar ao Supabase"""
    print("🔍 Verificando conectividade com Supabase...")
    
    try:
        database_url = os.getenv('DATABASE_URL')
        print(f"📋 URL: {database_url}")
        
        # Tentar conectar com timeout maior
        conn = psycopg2.connect(
            database_url,
            connect_timeout=30
        )
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        conn.close()
        print("✅ Conectividade com Supabase OK!")
        return True
        
    except Exception as e:
        print(f"❌ Problema de conectividade: {e}")
        return False

def populate_local_database():
    """Popula banco SQLite local com dados de exemplo usando estrutura existente"""
    print("🏠 Populando banco de dados local...")
    
    try:
        conn = sqlite3.connect('coins.db')
        cursor = conn.cursor()
        
        # Verificar se já existem dados
        cursor.execute("SELECT COUNT(*) FROM coins")
        existing_count = cursor.fetchone()[0]
        
        if existing_count > 0:
            print(f"📋 Banco já possui {existing_count} moedas.")
            response = input("Deseja limpar e recriar os dados? (s/n): ")
            if response.lower() == 's':
                cursor.execute("DELETE FROM coins")
                cursor.execute("DELETE FROM users")
                print("🧹 Dados anteriores removidos.")
            else:
                conn.close()
                return
        
        # Inserir usuário padrão (estrutura existente: id, username, password_hash)
        cursor.execute('''
            INSERT OR IGNORE INTO users (id, username, password_hash)
            VALUES (1, 'admin', 'hashed_password_123')
        ''')
        
        # Inserir moedas de exemplo (estrutura existente)
        sample_coins = [
            (1, "Denário de Tibério", "Período Romano", "Judéia", "Prata", "Denário", "14-37 d.C.", 
             "Moeda do tempo de Jesus Cristo, usada durante seu ministério.", "", ""),
            (2, "Shekel do Templo", "Primeiro Século", "Jerusalém", "Prata", "Shekel", "66-70 d.C.",
             "Moeda da primeira revolta judaica, símbolo de independência.", "", ""),
            (3, "Lepton da Viúva", "Período do Templo", "Jerusalém", "Bronze", "Lepton", "40-70 d.C.",
             "A menor moeda judaica, mencionada na parábola da viúva pobre.", "", ""),
            (4, "Sestércio de Vespasiano", "Período Romano", "Roma", "Bronze", "Sestércio", "69-79 d.C.",
             "Moeda comemorativa que celebra a conquista da Judéia.", "", ""),
            (5, "Dracma de Antíoco IV", "Período Selêucida", "Síria", "Prata", "Dracma", "175-164 a.C.",
             "Moeda helenística do tempo dos Macabeus.", "", ""),
            (6, "Aureus de Augusto", "Império Romano", "Roma", "Ouro", "Aureus", "27 a.C.-14 d.C.",
             "Moeda de ouro do primeiro imperador romano.", "", ""),
            (7, "Tetradracma de Tiro", "Período Fenício", "Tiro", "Prata", "Tetradracma", "126-65 a.C.",
             "Moeda usada para pagar o tributo do templo.", "", ""),
            (8, "Prutah de Herodes", "Reino da Judéia", "Jerusalém", "Bronze", "Prutah", "37-4 a.C.",
             "Pequena moeda de bronze do rei Herodes, o Grande.", "", "")
        ]
        
        for coin in sample_coins:
            cursor.execute('''
                INSERT OR IGNORE INTO coins 
                (id, name, period, region, material, denomination, year, description, image_front, image_back)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', coin)
        
        conn.commit()
        
        # Verificar resultados
        cursor.execute("SELECT COUNT(*) FROM users")
        user_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM coins")
        coin_count = cursor.fetchone()[0]
        
        print(f"✅ Banco de dados local configurado com sucesso!")
        print(f"👥 Usuários: {user_count}")
        print(f"🪙 Moedas: {coin_count}")
        
        # Mostrar algumas moedas
        cursor.execute("SELECT name, period, material FROM coins LIMIT 3")
        sample = cursor.fetchall()
        print("\n📋 Exemplos de moedas inseridas:")
        for coin in sample:
            print(f"  • {coin[0]} ({coin[1]}, {coin[2]})")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Erro ao configurar banco local: {e}")

def migrate_with_fallback():
    """Migra dados com fallback para SQLite local se Supabase não estiver disponível"""
    print("🔄 Iniciando migração com fallback...")
    
    # Verificar conectividade
    supabase_available = check_supabase_connectivity()
    
    if not supabase_available:
        print("⚠️ Supabase não disponível. Usando SQLite local como alternativa.")
        print("💡 Sugestões para resolver o problema do Supabase:")
        print("   1. Verificar se a URL do Supabase está correta")
        print("   2. Verificar conectividade de internet")
        print("   3. Verificar se o projeto Supabase está ativo")
        print("   4. Tentar usar um DNS público (8.8.8.8)")
        print()
        populate_local_database()
        return
    
    print("✅ Supabase disponível! Procedendo com migração normal...")
    # Implementar migração para Supabase se necessário

if __name__ == "__main__":
    migrate_with_fallback()