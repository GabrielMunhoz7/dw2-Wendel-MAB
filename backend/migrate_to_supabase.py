import sqlite3import sqlite3import sqlite3

import psycopg2

import osimport psycopg2import psycopg2

import bcrypt

from dotenv import load_dotenvimport osimport os



load_dotenv()import bcryptimport sqlite3



def migrate_data():from dotenv import load_dotenvimport psycopg2

    print("🔄 Iniciando migração...")

    import os

    try:

        # Conectar ao PostgreSQL (Supabase)load_dotenv()import bcrypt

        print("☁️ Conectando ao Supabase...")

        pg_conn = psycopg2.connect(os.getenv('DATABASE_URL'))from dotenv import load_dotenv

        pg_cursor = pg_conn.cursor()

        def migrate_data():

        # Criar tabelas se não existirem

        print("📋 Criando tabelas...")    print("🔄 Iniciando migração...")load_dotenv()

        create_tables_sql = """

        CREATE TABLE IF NOT EXISTS users (    

            id SERIAL PRIMARY KEY,

            username VARCHAR(255) UNIQUE NOT NULL,    try:def migrate_data():

            password_hash VARCHAR(255) NOT NULL,

            role VARCHAR(50) DEFAULT 'user',        # Conectar ao PostgreSQL (Supabase)    print("🔄 Iniciando migração...")

            created_at TIMESTAMP DEFAULT NOW()

        );        print("☁️ Conectando ao Supabase...")    



        CREATE TABLE IF NOT EXISTS coins (        pg_conn = psycopg2.connect(os.getenv('DATABASE_URL'))    try:

            id SERIAL PRIMARY KEY,

            name VARCHAR(255) NOT NULL,        pg_cursor = pg_conn.cursor()        # Conectar ao PostgreSQL (Supabase)

            period VARCHAR(255),

            region VARCHAR(255),                print("☁️ Conectando ao Supabase...")

            material VARCHAR(255),

            denomination VARCHAR(255),        # Criar tabelas se não existirem        pg_conn = psycopg2.connect(os.getenv('DATABASE_URL'))

            year VARCHAR(255),

            description TEXT,        print("📋 Criando tabelas...")        pg_cursor = pg_conn.cursor()

            historia TEXT,

            contexto TEXT,        create_tables_sql = """        

            referencia TEXT,

            image_front VARCHAR(500),        CREATE TABLE IF NOT EXISTS users (        # Criar tabelas se não existirem

            image_back VARCHAR(500),

            created_by INTEGER REFERENCES users(id),            id SERIAL PRIMARY KEY,        print("📋 Criando tabelas...")

            created_at TIMESTAMP DEFAULT NOW(),

            updated_at TIMESTAMP DEFAULT NOW()            username VARCHAR(255) UNIQUE NOT NULL,        create_tables_sql = """

        );

        """            password_hash VARCHAR(255) NOT NULL,        CREATE TABLE IF NOT EXISTS users (

        

        pg_cursor.execute(create_tables_sql)            role VARCHAR(50) DEFAULT 'user',            id SERIAL PRIMARY KEY,

        

        # Inserir usuário admin            created_at TIMESTAMP DEFAULT NOW()            username VARCHAR(255) UNIQUE NOT NULL,

        print("👤 Criando usuário admin...")

        password_hash = bcrypt.hashpw('admin123'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')        );            password_hash VARCHAR(255) NOT NULL,

        pg_cursor.execute("""

            INSERT INTO users (username, password_hash, role)             role VARCHAR(50) DEFAULT 'user',

            VALUES (%s, %s, %s)

            ON CONFLICT (username) DO NOTHING        CREATE TABLE IF NOT EXISTS coins (            created_at TIMESTAMP DEFAULT NOW()

        """, ('admin', password_hash, 'admin'))

                    id SERIAL PRIMARY KEY,        );

        # Inserir dados de exemplo

        print("🪙 Inserindo moedas de exemplo...")            name VARCHAR(255) NOT NULL,

        create_sample_data(pg_cursor)

                    period VARCHAR(255),        CREATE TABLE IF NOT EXISTS coins (

        pg_conn.commit()

        print("✅ Migração concluída com sucesso!")            region VARCHAR(255),            id SERIAL PRIMARY KEY,

        

    except Exception as e:            material VARCHAR(255),            name VARCHAR(255) NOT NULL,

        print(f"❌ Erro na migração: {e}")

        print(f"Tipo do erro: {type(e).__name__}")            denomination VARCHAR(255),            period VARCHAR(255),

        import traceback

        traceback.print_exc()            year VARCHAR(255),            region VARCHAR(255),

        

    finally:            description TEXT,            material VARCHAR(255),

        if 'pg_conn' in locals():

            pg_cursor.close()            historia TEXT,            denomination VARCHAR(255),

            pg_conn.close()

            contexto TEXT,            year VARCHAR(255),

def create_sample_data(cursor):

    """Inserir dados de exemplo diretamente no Supabase"""            referencia TEXT,            description TEXT,

    sample_coins = [

        ("Denário de Tibério", "Período Romano", "Judéia", "Prata", "Denário", "14-37 d.C.",             image_front VARCHAR(500),            historia TEXT,

         "Moeda do tempo de Jesus Cristo, mencionada nos Evangelhos quando perguntaram a Jesus sobre pagar impostos a César.", 

         "Esta moeda representa o poder romano na Palestina durante o ministério de Jesus. O denário era o salário diário de um trabalhador comum.",             image_back VARCHAR(500),            contexto TEXT,

         "Jesus Cristo mencionou esta moeda quando disse 'Dai a César o que é de César, e a Deus o que é de Deus'", 

         "Mateus 22:19-21, Marcos 12:15-17",             created_by INTEGER REFERENCES users(id),            referencia TEXT,

         "https://images.unsplash.com/photo-1544380904-c686aad2fc40?w=400", 

         "https://images.unsplash.com/photo-1544380904-c686aad2fc40?w=400"),            created_at TIMESTAMP DEFAULT NOW(),            image_front VARCHAR(500),

        

        ("Shekel do Templo", "Primeiro Século", "Jerusalém", "Prata", "Shekel", "66-70 d.C.",            updated_at TIMESTAMP DEFAULT NOW()            image_back VARCHAR(500),

         "Moeda da primeira revolta judaica contra Roma, cunhada pelos rebeldes judeus durante o cerco de Jerusalém.",

         "Representa a luta pela independência judaica. Era usada para pagar o imposto do templo e para transações religiosas.",        );            created_by INTEGER REFERENCES users(id),

         "Moeda de resistência contra o domínio romano, símbolo da fé e identidade judaica",

         "História da Revolta Judaica (66-73 d.C.)",        """            created_at TIMESTAMP DEFAULT NOW(),

         "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=400",

         "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=400"),                    updated_at TIMESTAMP DEFAULT NOW()

        

        ("Lepton da Viúva", "Período do Templo", "Jerusalém", "Bronze", "Lepton", "40-70 d.C.",        pg_cursor.execute(create_tables_sql)        );

         "A menor moeda em circulação na Judéia, equivalente a 1/128 de denário. Mencionada por Jesus na parábola da viúva pobre.",

         "Jesus observou uma viúva pobre depositando dois leptons no tesouro do templo, elogiando sua generosidade acima das grandes ofertas dos ricos.",                """

         "Símbolo de generosidade e sacrifício. Jesus disse que ela deu mais que todos os outros, pois deu tudo o que tinha.",

         "Marcos 12:41-44, Lucas 21:1-4",        # Inserir usuário admin        

         "https://images.unsplash.com/photo-1614028674026-a65e31bfd27c?w=400",

         "https://images.unsplash.com/photo-1614028674026-a65e31bfd27c?w=400"),        print("👤 Criando usuário admin...")        pg_cursor.execute(create_tables_sql)

        

        ("Sestércio de Vespasiano", "Período Romano", "Roma", "Bronze", "Sestércio", "69-79 d.C.",        password_hash = bcrypt.hashpw('admin123'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')        

         "Moeda comemorativa da conquista da Judéia pelo imperador Vespasiano, com a inscrição 'IVDAEA CAPTA' (Judéia Capturada).",

         "Cunhada após a destruição de Jerusalém em 70 d.C., esta moeda celebrava a vitória romana sobre os judeus.",        pg_cursor.execute("""        # Inserir usuário admin

         "Propaganda imperial romana mostrando o triunfo sobre os judeus. Representa o fim do Segundo Templo.",

         "História da Destruição do Templo (70 d.C.)",            INSERT INTO users (username, password_hash, role)         print("� Criando usuário admin...")

         "https://images.unsplash.com/photo-1567783243594-4012e67c7b7b?w=400",

         "https://images.unsplash.com/photo-1567783243594-4012e67c7b7b?w=400"),            VALUES (%s, %s, %s)        password_hash = bcrypt.hashpw('admin123'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        

        ("Dracma de Antíoco IV", "Período Selêucida", "Síria", "Prata", "Dracma", "175-164 a.C.",            ON CONFLICT (username) DO NOTHING        pg_cursor.execute("""

         "Moeda do rei selêucida Antíoco IV Epífanes, conhecido por profanar o templo de Jerusalém.",

         "Antíoco IV tentou helenizar os judeus à força, profanou o templo e proibiu práticas judaicas, levando à revolta dos Macabeus.",        """, ('admin', password_hash, 'admin'))            INSERT INTO users (username, password_hash, role) 

         "Período de grande perseguição religiosa que resultou na festa de Hanukká após a reconsagração do templo.",

         "1 Macabeus, 2 Macabeus, Daniel 11",                    VALUES (%s, %s, %s)

         "https://images.unsplash.com/photo-1609081219090-a6d81d3085bf?w=400",

         "https://images.unsplash.com/photo-1609081219090-a6d81d3085bf?w=400"),        # Inserir dados de exemplo            ON CONFLICT (username) DO NOTHING

        

        ("Tetradracma de Tiro", "Período Romano", "Tiro", "Prata", "Tetradracma", "20 a.C. - 70 d.C.",        print("🪙 Inserindo moedas de exemplo...")        """, ('admin', password_hash, 'admin'))

         "Moeda de alta pureza de prata usada para pagar o imposto anual do templo em Jerusalém.",

         "Era a única moeda aceita no templo por sua pureza de prata. Possivelmente as '30 moedas de prata' pagas a Judas.",        create_sample_data(pg_cursor)        

         "Ironia histórica: moedas com imagens pagãs sendo usadas no templo judaico por necessidade prática.",

         "Mateus 26:15, Êxodo 30:13-16",                # Inserir dados de exemplo

         "https://images.unsplash.com/photo-1598300042247-d088f8ab3a91?w=400",

         "https://images.unsplash.com/photo-1598300042247-d088f8ab3a91?w=400")        pg_conn.commit()        print("🪙 Inserindo moedas de exemplo...")

    ]

            print("✅ Migração concluída com sucesso!")        create_sample_data(pg_cursor)

    for coin in sample_coins:

        cursor.execute("""            

            INSERT INTO coins (name, period, region, material, denomination, year, 

                             description, historia, contexto, referencia, image_front, image_back, created_by)    except Exception as e:    try:

            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 1)

        """, coin)        print(f"❌ Erro na migração: {e}")        # Conectar ao SQLite local

    

    print(f"✅ {len(sample_coins)} moedas de exemplo inseridas!")        print(f"Tipo do erro: {type(e).__name__}")        print("📱 Conectando ao SQLite...")



if __name__ == "__main__":        import traceback        sqlite_conn = sqlite3.connect('coins.db')

    migrate_data()
        traceback.print_exc()        sqlite_cursor = sqlite_conn.cursor()

                

    finally:        # Conectar ao PostgreSQL (Supabase)

        if 'pg_conn' in locals():        print("☁️ Conectando ao Supabase...")

            pg_cursor.close()        pg_conn = psycopg2.connect(os.getenv('DATABASE_URL'))

            pg_conn.close()        pg_cursor = pg_conn.cursor()

        

def create_sample_data(cursor):        # Verificar quais tabelas existem no SQLite

    """Inserir dados de exemplo diretamente no Supabase"""        sqlite_cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")

    sample_coins = [        tables = [table[0] for table in sqlite_cursor.fetchall()]

        ("Denário de Tibério", "Período Romano", "Judéia", "Prata", "Denário", "14-37 d.C.",         print(f"📋 Tabelas encontradas no SQLite: {tables}")

         "Moeda do tempo de Jesus Cristo, mencionada nos Evangelhos quando perguntaram a Jesus sobre pagar impostos a César.",         

         "Esta moeda representa o poder romano na Palestina durante o ministério de Jesus. O denário era o salário diário de um trabalhador comum.",         # Migrar dados se existirem

         "Jesus Cristo mencionou esta moeda quando disse 'Dai a César o que é de César, e a Deus o que é de Deus'",         for table in ['users', 'coins']:

         "Mateus 22:19-21, Marcos 12:15-17",             if table in tables:

         "https://images.unsplash.com/photo-1544380904-c686aad2fc40?w=400",                 print(f"🔄 Migrando tabela {table}...")

         "https://images.unsplash.com/photo-1544380904-c686aad2fc40?w=400"),                

                        # Buscar dados do SQLite

        ("Shekel do Templo", "Primeiro Século", "Jerusalém", "Prata", "Shekel", "66-70 d.C.",                sqlite_cursor.execute(f"SELECT * FROM {table}")

         "Moeda da primeira revolta judaica contra Roma, cunhada pelos rebeldes judeus durante o cerco de Jerusalém.",                rows = sqlite_cursor.fetchall()

         "Representa a luta pela independência judaica. Era usada para pagar o imposto do templo e para transações religiosas.",                

         "Moeda de resistência contra o domínio romano, símbolo da fé e identidade judaica",                if rows:

         "História da Revolta Judaica (66-73 d.C.)",                    # Obter nomes das colunas

         "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=400",                    sqlite_cursor.execute(f"PRAGMA table_info({table})")

         "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=400"),                    columns = [col[1] for col in sqlite_cursor.fetchall()]

                            

        ("Lepton da Viúva", "Período do Templo", "Jerusalém", "Bronze", "Lepton", "40-70 d.C.",                    # Limpar tabela no PostgreSQL

         "A menor moeda em circulação na Judéia, equivalente a 1/128 de denário. Mencionada por Jesus na parábola da viúva pobre.",                    pg_cursor.execute(f"DELETE FROM {table}")

         "Jesus observou uma viúva pobre depositando dois leptons no tesouro do templo, elogiando sua generosidade acima das grandes ofertas dos ricos.",                    

         "Símbolo de generosidade e sacrifício. Jesus disse que ela deu mais que todos os outros, pois deu tudo o que tinha.",                    # Inserir dados

         "Marcos 12:41-44, Lucas 21:1-4",                    placeholders = ','.join(['%s'] * len(columns))

         "https://images.unsplash.com/photo-1614028674026-a65e31bfd27c?w=400",                    insert_sql = f"INSERT INTO {table} ({','.join(columns)}) VALUES ({placeholders})"

         "https://images.unsplash.com/photo-1614028674026-a65e31bfd27c?w=400"),                    pg_cursor.executemany(insert_sql, rows)

                            

        ("Sestércio de Vespasiano", "Período Romano", "Roma", "Bronze", "Sestércio", "69-79 d.C.",                    print(f"✅ {len(rows)} registros migrados para {table}")

         "Moeda comemorativa da conquista da Judéia pelo imperador Vespasiano, com a inscrição 'IVDAEA CAPTA' (Judéia Capturada).",                else:

         "Cunhada após a destruição de Jerusalém em 70 d.C., esta moeda celebrava a vitória romana sobre os judeus.",                    print(f"⚠️ Tabela {table} está vazia")

         "Propaganda imperial romana mostrando o triunfo sobre os judeus. Representa o fim do Segundo Templo.",            else:

         "História da Destruição do Templo (70 d.C.)",                print(f"⚠️ Tabela {table} não existe no SQLite")

         "https://images.unsplash.com/photo-1567783243594-4012e67c7b7b?w=400",        

         "https://images.unsplash.com/photo-1567783243594-4012e67c7b7b?w=400"),        pg_conn.commit()

                print("✅ Migração concluída com sucesso!")

        ("Dracma de Antíoco IV", "Período Selêucida", "Síria", "Prata", "Dracma", "175-164 a.C.",        

         "Moeda do rei selêucida Antíoco IV Epífanes, conhecido por profanar o templo de Jerusalém.",    except Exception as e:

         "Antíoco IV tentou helenizar os judeus à força, profanou o templo e proibiu práticas judaicas, levando à revolta dos Macabeus.",        print(f"❌ Erro na migração: {e}")

         "Período de grande perseguição religiosa que resultou na festa de Hanukká após a reconsagração do templo.",        

         "1 Macabeus, 2 Macabeus, Daniel 11",    finally:

         "https://images.unsplash.com/photo-1609081219090-a6d81d3085bf?w=400",        if 'sqlite_conn' in locals():

         "https://images.unsplash.com/photo-1609081219090-a6d81d3085bf?w=400"),            sqlite_conn.close()

                if 'pg_conn' in locals():

        ("Tetradracma de Tiro", "Período Romano", "Tiro", "Prata", "Tetradracma", "20 a.C. - 70 d.C.",            pg_conn.close()

         "Moeda de alta pureza de prata usada para pagar o imposto anual do templo em Jerusalém.",

         "Era a única moeda aceita no templo por sua pureza de prata. Possivelmente as '30 moedas de prata' pagas a Judas.",def create_sample_data():

         "Ironia histórica: moedas com imagens pagãs sendo usadas no templo judaico por necessidade prática.",    """Criar dados de exemplo diretamente no Supabase"""

         "Mateus 26:15, Êxodo 30:13-16",    try:

         "https://images.unsplash.com/photo-1598300042247-d088f8ab3a91?w=400",        pg_conn = psycopg2.connect(os.getenv('DATABASE_URL'))

         "https://images.unsplash.com/photo-1598300042247-d088f8ab3a91?w=400")        pg_cursor = pg_conn.cursor()

    ]        

            # Inserir moedas de exemplo

    for coin in sample_coins:        sample_coins = [

        cursor.execute("""            ("Denário de Tibério", "Período Romano", "Judéia", "Prata", "Denário", "14-37 d.C.", 

            INSERT INTO coins (name, period, region, material, denomination, year,              "Moeda do tempo de Jesus", "Usada durante o ministério de Cristo", 

                             description, historia, contexto, referencia, image_front, image_back, created_by)             "Mencionada em Mateus 22:19", "Mateus 22:19-21"),

            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 1)            ("Shekel do Templo", "Primeiro Século", "Jerusalém", "Prata", "Shekel", "66-70 d.C.",

        """, coin)             "Moeda da revolta judaica", "Cunhada durante a primeira revolta judaica",

                 "Símbolo de independência", "História Judaica"),

    print(f"✅ {len(sample_coins)} moedas de exemplo inseridas!")            ("Lepton da Viúva", "Período do Templo", "Jerusalém", "Bronze", "Lepton", "40-70 d.C.",

             "A menor moeda judaica", "Mencionada na parábola da viúva pobre",

if __name__ == "__main__":             "Símbolo de generosidade", "Marcos 12:41-44"),

    migrate_data()            ("Sestércio de Vespasiano", "Período Romano", "Roma", "Bronze", "Sestércio", "69-79 d.C.",
             "Moeda comemorativa", "Celebra a conquista da Judéia",
             "Propaganda imperial romana", "História Romana"),
            ("Dracma de Antíoco IV", "Período Selêucida", "Síria", "Prata", "Dracma", "175-164 a.C.",
             "Moeda helenística", "Do tempo dos Macabeus",
             "Período de perseguição religiosa", "1 Macabeus")
        ]
        
        for coin in sample_coins:
            pg_cursor.execute("""
                INSERT INTO coins (name, period, region, material, denomination, year, 
                                 description, historia, contexto, referencia, created_by)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 1)
            """, coin)
        
        pg_conn.commit()
        print("✅ Dados de exemplo criados!")
        
    except Exception as e:
        print(f"❌ Erro ao criar dados de exemplo: {e}")
    finally:
        pg_conn.close()

if __name__ == "__main__":
    migrate_data()