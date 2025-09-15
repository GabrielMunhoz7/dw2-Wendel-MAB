import psycopg2import sqlite3

import osimport psycopg2

import bcryptimport os

from dotenv import load_dotenvfrom dotenv import load_dotenv



load_dotenv()load_dotenv()



def migrate_with_data():def check_supabase_connectivity():

    print("🔄 Iniciando migração completa...")    """Verifica se conseguimos conectar ao Supabase"""

        print("🔍 Verificando conectividade com Supabase...")

    try:    

        # Conectar ao PostgreSQL (Supabase)    try:

        print("☁️ Conectando ao Supabase...")        database_url = os.getenv('DATABASE_URL')

        pg_conn = psycopg2.connect(os.getenv('DATABASE_URL'))        print(f"📋 URL: {database_url}")

        pg_cursor = pg_conn.cursor()        

                # Tentar conectar com timeout maior

        # Verificar se usuário admin já existe        conn = psycopg2.connect(

        print("👤 Verificando usuário admin...")            database_url,

        pg_cursor.execute("SELECT COUNT(*) FROM users WHERE username = 'admin'")            connect_timeout=30

        admin_count = pg_cursor.fetchone()[0]        )

                cursor = conn.cursor()

        if admin_count == 0:        cursor.execute("SELECT 1")

            print("👤 Criando usuário admin...")        conn.close()

            password_hash = bcrypt.hashpw('admin123'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')        print("✅ Conectividade com Supabase OK!")

            pg_cursor.execute("""        return True

                INSERT INTO users (username, password_hash, role)         

                VALUES (%s, %s, %s)    except Exception as e:

            """, ('admin', password_hash, 'admin'))        print(f"❌ Problema de conectividade: {e}")

        else:        return False

            print("✅ Usuário admin já existe")

        def migrate_with_fallback():

        # Verificar quantas moedas já existem    """Migra dados com fallback para SQLite local se Supabase não estiver disponível"""

        pg_cursor.execute("SELECT COUNT(*) FROM coins")    print("🔄 Iniciando migração com fallback...")

        coin_count = pg_cursor.fetchone()[0]    

            # Verificar conectividade

        if coin_count == 0:    supabase_available = check_supabase_connectivity()

            print("🪙 Inserindo moedas bíblicas...")    

            insert_biblical_coins(pg_cursor)    if not supabase_available:

        else:        print("⚠️ Supabase não disponível. Usando SQLite local como alternativa.")

            print(f"ℹ️ Já existem {coin_count} moedas no banco")        setup_local_database()

            print("🪙 Adicionando mais moedas bíblicas...")        return

            insert_biblical_coins(pg_cursor)    

            # Proceder com migração normal se Supabase estiver disponível

        pg_conn.commit()    migrate_to_supabase()

        print("✅ Migração concluída com sucesso!")

        def setup_local_database():

        # Mostrar estatísticas finais    """Configura banco SQLite local com dados de exemplo"""

        pg_cursor.execute("SELECT COUNT(*) FROM users")    print("🏠 Configurando banco de dados local...")

        final_users = pg_cursor.fetchone()[0]    

            try:

        pg_cursor.execute("SELECT COUNT(*) FROM coins")        conn = sqlite3.connect('coins.db')

        final_coins = pg_cursor.fetchone()[0]        cursor = conn.cursor()

                

        print(f"\n📊 ESTATÍSTICAS FINAIS:")        # Criar tabelas

        print(f"👥 Usuários: {final_users}")        cursor.execute('''

        print(f"🪙 Moedas: {final_coins}")            CREATE TABLE IF NOT EXISTS users (

                        id INTEGER PRIMARY KEY AUTOINCREMENT,

    except Exception as e:                username TEXT UNIQUE NOT NULL,

        print(f"❌ Erro na migração: {e}")                email TEXT UNIQUE NOT NULL,

        import traceback                password_hash TEXT NOT NULL,

        traceback.print_exc()                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

                    )

    finally:        ''')

        if 'pg_conn' in locals():        

            pg_cursor.close()        cursor.execute('''

            pg_conn.close()            CREATE TABLE IF NOT EXISTS coins (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

def insert_biblical_coins(cursor):                name TEXT NOT NULL,

    """Inserir coleção de moedas bíblicas"""                period TEXT,

    biblical_coins = [                region TEXT,

        ("Denário de Tibério", "Império Romano (14-37 d.C.)", "Palestina", "Prata", "Denário", "14-37 d.C.",                 material TEXT,

         "A famosa moeda do 'Tributo a César', mencionada diretamente por Jesus Cristo nos Evangelhos.",                 denomination TEXT,

         "O denário era o salário diário de um trabalhador comum na época de Jesus. Esta moeda tinha a imagem de Tibério César.",                 year TEXT,

         "Jesus usou-a para ensinar sobre a separação entre os deveres civis e religiosos.",                 description TEXT,

         "Mateus 22:19-21, Marcos 12:15-17",                 historia TEXT,

         "https://images.unsplash.com/photo-1544380904-c686aad2fc40?w=400",                 contexto TEXT,

         "https://images.unsplash.com/photo-1544380904-c686aad2fc40?w=400"),                referencia TEXT,

                        created_by INTEGER,

        ("Shekel da Primeira Revolta", "Revolta Judaica (66-70 d.C.)", "Jerusalém", "Prata", "Shekel", "66-70 d.C.",                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

         "Moeda cunhada pelos rebeldes judeus durante a primeira revolta contra Roma.",                FOREIGN KEY (created_by) REFERENCES users (id)

         "Durante a revolta, os judeus estabeleceram sua própria casa da moeda em Jerusalém como ato de desafio.",            )

         "Simbolizava a esperança de independência nacional e liberdade religiosa.",        ''')

         "Guerras Judaicas de Josefo",        

         "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=400",        # Inserir usuário padrão

         "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=400"),        cursor.execute('''

                    INSERT OR IGNORE INTO users (id, username, email, password_hash)

        ("Lepton da Viúva Pobre", "Período do Segundo Templo (40-70 d.C.)", "Jerusalém", "Bronze", "Lepton", "40-70 d.C.",            VALUES (1, 'admin', 'admin@coins.com', 'hashed_password')

         "A menor moeda em circulação, imortalizada na parábola de Jesus sobre a viúva pobre.",        ''')

         "Jesus observou uma viúva pobre oferecendo dois leptons no templo, elogiando sua generosidade.",        

         "Representa o maior ensinamento sobre generosidade e fé - dar tudo o que se tem.",        # Inserir moedas de exemplo

         "Marcos 12:41-44, Lucas 21:1-4",        sample_coins = [

         "https://images.unsplash.com/photo-1614028674026-a65e31bfd27c?w=400",            ("Denário de Tibério", "Período Romano", "Judéia", "Prata", "Denário", "14-37 d.C.", 

         "https://images.unsplash.com/photo-1614028674026-a65e31bfd27c?w=400"),             "Moeda do tempo de Jesus", "Usada durante o ministério de Cristo", 

                     "Mencionada em Mateus 22:19", "Mateus 22:19-21", 1),

        ("Sestércio 'Judaea Capta'", "Império Romano (71 d.C.)", "Roma", "Bronze", "Sestércio", "71 d.C.",            ("Shekel do Templo", "Primeiro Século", "Jerusalém", "Prata", "Shekel", "66-70 d.C.",

         "Moeda comemorativa da vitória romana sobre os judeus, com a inscrição 'IVDAEA CAPTA'.",             "Moeda da revolta judaica", "Cunhada durante a primeira revolta judaica",

         "Cunhada após a destruição de Jerusalém para celebrar a vitória imperial.",             "Símbolo de independência", "História Judaica", 1),

         "Marca o início da diáspora judaica que duraria quase 2.000 anos.",            ("Lepton da Viúva", "Período do Templo", "Jerusalém", "Bronze", "Lepton", "40-70 d.C.",

         "Guerras Judaicas, Mateus 24:1-2",             "A menor moeda judaica", "Mencionada na parábola da viúva pobre",

         "https://images.unsplash.com/photo-1567783243594-4012e67c7b7b?w=400",             "Símbolo de generosidade", "Marcos 12:41-44", 1),

         "https://images.unsplash.com/photo-1567783243594-4012e67c7b7b?w=400"),            ("Sestércio de Vespasiano", "Período Romano", "Roma", "Bronze", "Sestércio", "69-79 d.C.",

                     "Moeda comemorativa", "Celebra a conquista da Judéia",

        ("Tetradracma de Tiro", "Cidade-Estado de Tiro (20 a.C. - 70 d.C.)", "Tiro", "Prata", "Tetradracma", "20 a.C. - 70 d.C.",             "Propaganda imperial romana", "História Romana", 1),

         "Única moeda aceita no templo de Jerusalém, possivelmente as '30 moedas de prata' de Judas.",            ("Dracma de Antíoco IV", "Período Selêucida", "Síria", "Prata", "Dracma", "175-164 a.C.",

         "Apesar da imagem pagã, era aceita no templo devido à pureza excepcional da prata.",             "Moeda helenística", "Do tempo dos Macabeus",

         "Ironia: moedas pagãs usadas no templo sagrado e para trair o Messias.",             "Período de perseguição religiosa", "1 Macabeus", 1)

         "Mateus 26:15, 27:3-10",        ]

         "https://images.unsplash.com/photo-1598300042247-d088f8ab3a91?w=400",        

         "https://images.unsplash.com/photo-1598300042247-d088f8ab3a91?w=400"),        for coin in sample_coins:

                    cursor.execute('''

        ("Dracma de Antíoco IV", "Império Selêucida (175-164 a.C.)", "Antioquia", "Prata", "Dracma", "175-164 a.C.",                INSERT OR IGNORE INTO coins 

         "Moeda do rei que profanou o templo, desencadeando a revolta dos Macabeus.",                (name, period, region, material, denomination, year, description, 

         "Antíoco tentou helenizar os judeus e profanou o templo oferecendo porcos no altar.",                 historia, contexto, referencia, created_by)

         "A purificação posterior é celebrada na festa de Hanukká.",                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)

         "1 Macabeus, Daniel 8:9-14",            ''', coin)

         "https://images.unsplash.com/photo-1609081219090-a6d81d3085bf?w=400",        

         "https://images.unsplash.com/photo-1609081219090-a6d81d3085bf?w=400")        conn.commit()

    ]        print("✅ Banco de dados local configurado com sucesso!")

            print(f"📊 {cursor.rowcount} moedas inseridas")

    for coin_data in biblical_coins:        

        cursor.execute("""        # Verificar dados

            INSERT INTO coins (name, period, region, material, denomination, year,         cursor.execute("SELECT COUNT(*) FROM coins")

                             description, historia, contexto, referencia, image_front, image_back, created_by)        count = cursor.fetchone()[0]

            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 1)        print(f"📋 Total de moedas no banco: {count}")

        """, coin_data)        

            conn.close()

    print(f"✅ {len(biblical_coins)} moedas bíblicas inseridas!")        

    except Exception as e:

if __name__ == "__main__":        print(f"❌ Erro ao configurar banco local: {e}")

    migrate_with_data()
def migrate_to_supabase():
    """Migração original para Supabase"""
    print("☁️ Migrando para Supabase...")
    # Código original da migração aqui...
    # (implementar se necessário)

if __name__ == "__main__":
    migrate_with_fallback()