import sqlite3
import os

def update_database_structure_fixed():
    """Atualiza a estrutura do banco SQLite para corresponder aos modelos"""
    print("🔄 Atualizando estrutura do banco de dados...")
    
    try:
        conn = sqlite3.connect('coins.db')
        cursor = conn.cursor()
        
        # Verificar estrutura atual da tabela users
        cursor.execute("PRAGMA table_info(users)")
        user_columns = [col[1] for col in cursor.fetchall()]
        print(f"📋 Colunas atuais em users: {user_columns}")
        
        # Verificar estrutura atual da tabela coins
        cursor.execute("PRAGMA table_info(coins)")
        coin_columns = [col[1] for col in cursor.fetchall()]
        print(f"📋 Colunas atuais em coins: {coin_columns}")
        
        # Adicionar colunas faltantes na tabela coins (sem valores padrão problemáticos)
        missing_coin_columns = {
            'updated_at': 'TIMESTAMP'
        }
        
        for col_name, col_type in missing_coin_columns.items():
            if col_name not in coin_columns:
                print(f"➕ Adicionando coluna '{col_name}' à tabela coins...")
                cursor.execute(f"ALTER TABLE coins ADD COLUMN {col_name} {col_type}")
        
        # Atualizar usuário admin existente para ter role de admin (se coluna role existe)
        if 'role' in user_columns:
            cursor.execute("UPDATE users SET role = 'admin' WHERE username = 'admin'")
            print("✅ Role do admin atualizada")
        
        # Definir created_by para moedas existentes (usar ID 1 - admin)
        if 'created_by' in coin_columns:
            cursor.execute("UPDATE coins SET created_by = 1 WHERE created_by IS NULL")
            print("✅ Created_by das moedas atualizado")
        
        conn.commit()
        
        # Verificar estrutura final
        cursor.execute("PRAGMA table_info(users)")
        final_user_columns = [col[1] for col in cursor.fetchall()]
        cursor.execute("PRAGMA table_info(coins)")
        final_coin_columns = [col[1] for col in cursor.fetchall()]
        
        print("✅ Estrutura atualizada com sucesso!")
        print(f"👥 Colunas finais em users: {final_user_columns}")
        print(f"🪙 Colunas finais em coins: {final_coin_columns}")
        
        # Testar se a estrutura está funcionando
        print("\n🧪 Testando estrutura...")
        cursor.execute("SELECT COUNT(*) FROM users")
        user_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM coins")
        coin_count = cursor.fetchone()[0]
        print(f"👥 Usuários: {user_count}")
        print(f"🪙 Moedas: {coin_count}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Erro ao atualizar estrutura: {e}")

if __name__ == "__main__":
    update_database_structure_fixed()