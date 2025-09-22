import os
import bcrypt
from flask import Flask, request, jsonify
from flask_cors import CORS
from sqlalchemy.orm import Session
from itsdangerous import URLSafeTimedSerializer
import json
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'sua-chave-secreta-super-forte')

# Configurar CORS
allowed_origins = os.environ.get('ALLOWED_ORIGINS', '*').split(',')
CORS(app, origins=allowed_origins)

# Serializador para tokens
serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])

# Inicialização do banco com tratamento de erros
try:
    from database import SessionLocal, engine
    from models import Base, User, Coin
    
    # Criar tabelas se não existirem
    Base.metadata.create_all(bind=engine)
    print("✅ Banco inicializado com sucesso")
    
except Exception as e:
    print(f"❌ Erro na inicialização do banco: {e}")
    # Continuar mesmo com erro para permitir debug
    SessionLocal = None
    engine = None

def get_db():
    if SessionLocal is None:
        raise Exception("Banco de dados não inicializado")
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()

@app.route('/api/coins', methods=['GET'])
def get_coins():
    """Listar todas as moedas"""
    try:
        db = get_db()
        coins = db.query(Coin).all()
        
        coins_list = []
        for coin in coins:
            coins_list.append({
                'id': coin.id,
                'name': coin.name,
                'period': coin.period,
                'region': coin.region,
                'material': coin.material,
                'denomination': coin.denomination,
                'historia': coin.historia,
                'contexto': coin.contexto,
                'referencia': coin.referencia,
                'image_front': coin.image_front,
                'image_back': coin.image_back
            })
        
        return jsonify(coins_list)
        
    except Exception as e:
        print(f"Erro ao buscar moedas: {e}")
        return jsonify({'error': str(e)}), 500
    finally:
        if 'db' in locals():
            db.close()

@app.route('/api/test')
def test():
    """Endpoint de teste"""
    return jsonify({"status": "API funcionando", "db_available": SessionLocal is not None})

if __name__ == '__main__':
    app.run(debug=True)