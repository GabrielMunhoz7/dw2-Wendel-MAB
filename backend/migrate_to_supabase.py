import sqlite3
import psycopg2
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env (se existir)
load_dotenv()

def migrate_data():
    print("🚀 Iniciando migração de dados...")
    
    # === CONECTAR AO SQLITE LOCAL ===
    sqlite_path = 'coins.db'
    if not os.path.exists(sqlite_path):
        print("❌ Arquivo coins.db não encontrado na pasta backend.")
        print("   Se você não tem dados locais, pule para o Passo 5.")
        return
    
    print(f"📁 Conectando ao SQLite: {sqlite_path}")
    sqlite_conn = sqlite3.connect(sqlite_path)
    cursor = sqlite_conn.cursor()
    
    try:
        # Verificar se tabela coins existe no SQLite
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='coins'")
        if not cursor.fetchone():
            print("❌ Tabela 'coins' não encontrada no SQLite.")
            print("   Isso é normal se você nunca adicionou moedas localmente.")
            return
        
        # Buscar todas as moedas do SQLite
        cursor.execute("SELECT * FROM coins")
        coins_data = cursor.fetchall()
        
        # Buscar nomes das colunas
        cursor.execute("PRAGMA table_info(coins)")
        columns_info = cursor.fetchall()
        columns = [row[1] for row in columns_info]  # row[1] é o nome da coluna
        
        print(f"📊 Encontradas {len(coins_data)} moedas no SQLite local")
        print(f"📋 Colunas encontradas: {', '.join(columns)}")
        
        if len(coins_data) == 0:
            print("✅ Nenhuma moeda para migrar. Prossiga para o Passo 5.")
            return
        
        # === CONECTAR AO POSTGRESQL (SUPABASE) ===
        postgres_url = os.environ.get('DATABASE_URL')
        if not postgres_url:
            print("❌ DATABASE_URL não encontrada.")
            print("   Configure: set DATABASE_URL=sua_url_do_supabase")
            return
        
        print("🔗 Conectando ao Supabase PostgreSQL...")
        pg_conn = psycopg2.connect(postgres_url)
        pg_cursor = pg_conn.cursor()
        
        # Verificar se tabela existe no PostgreSQL
        pg_cursor.execute("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'coins')")
        table_exists = pg_cursor.fetchone()[0]
        
        if not table_exists:
            print("❌ Tabela 'coins' não existe no Supabase.")
            print("   Volte ao Passo 2.3 e execute o SQL no Supabase.")
            return
        
        # === MIGRAR CADA MOEDA ===
        migrated = 0
        errors = 0
        
        for row in coins_data:
            # Converter linha em dicionário
            coin_dict = dict(zip(columns, row))
            
            # Mapear campos do SQLite para PostgreSQL
            # (ajuste os nomes conforme sua estrutura atual)
            insert_data = {
                'name': coin_dict.get('name') or coin_dict.get('nome') or 'Moeda sem nome',
                'period': coin_dict.get('period') or coin_dict.get('periodo'),
                'region': coin_dict.get('region') or coin_dict.get('regiao'),
                'material': coin_dict.get('material'),
                'denomination': coin_dict.get('denomination') or coin_dict.get('denominacao'),
                'year': coin_dict.get('year') or coin_dict.get('ano'),
                'description': coin_dict.get('description') or coin_dict.get('descricao'),
                'historia': coin_dict.get('historia'),
                'contexto': coin_dict.get('contexto'),
                'referencia': coin_dict.get('referencia'),
                'image_front': coin_dict.get('image_front') or coin_dict.get('image'),
                'image_back': coin_dict.get('image_back') or coin_dict.get('image_rev')
            }
            
            try:
                # Inserir no PostgreSQL
                pg_cursor.execute("""
                    INSERT INTO coins (name, period, region, material, denomination, year, 
                                     description, historia, contexto, referencia, image_front, image_back)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    insert_data['name'], insert_data['period'], insert_data['region'],
                    insert_data['material'], insert_data['denomination'], insert_data['year'],
                    insert_data['description'], insert_data['historia'], insert_data['contexto'],
                    insert_data['referencia'], insert_data['image_front'], insert_data['image_back']
                ))
                migrated += 1
                print(f"✅ Migrada: {insert_data['name']}")
                
            except Exception as e:
                errors += 1
                print(f"❌ Erro ao migrar '{coin_dict.get('name', 'sem nome')}': {e}")
        
        # Confirmar todas as inserções
        pg_conn.commit()
        
        print(f"\n🎉 MIGRAÇÃO CONCLUÍDA!")
        print(f"✅ {migrated} moedas transferidas com sucesso")
        if errors > 0:
            print(f"❌ {errors} erros encontrados")
        print(f"📊 Total processado: {len(coins_data)} moedas")
        
    except Exception as e:
        print(f"❌ Erro durante migração: {e}")
        
    finally:
        # Fechar conexões
        sqlite_conn.close()
        if 'pg_conn' in locals():
            pg_conn.close()
        print("🔐 Conexões fechadas.")

if __name__ == "__main__":
    migrate_data()