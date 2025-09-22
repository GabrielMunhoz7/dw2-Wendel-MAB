import os
from flask import Flask, jsonify
from flask_cors import CORS
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

app = Flask(__name__)

# Configurar CORS
CORS(app, origins=['*'])

# Configuração do banco
Base = declarative_base()

class Coin(Base):
    __tablename__ = 'coins'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    period = Column(String(100), nullable=False)
    region = Column(String(100), nullable=False)
    material = Column(String(100), nullable=False)
    denomination = Column(String(100))
    historia = Column(Text)
    contexto = Column(Text)
    referencia = Column(Text)
    image_front = Column(Text)
    image_back = Column(Text)

# Inicialização do banco
try:
    database_url = os.environ.get('DATABASE_URL')
    if database_url:
        engine = create_engine(database_url, pool_pre_ping=True)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        print("✅ Banco conectado")
    else:
        engine = None
        SessionLocal = None
        print("❌ DATABASE_URL não encontrada")
except Exception as e:
    print(f"❌ Erro no banco: {e}")
    engine = None
    SessionLocal = None

@app.route('/api/test')
def test():
    """Endpoint de teste"""
    return jsonify({
        "status": "API funcionando",
        "database_url_exists": bool(os.environ.get('DATABASE_URL')),
        "session_available": SessionLocal is not None
    })

@app.route('/api/coins', methods=['GET'])
def get_coins():
    """Listar todas as moedas"""
    if not SessionLocal:
        return jsonify({'error': 'Banco não disponível'}), 500
        
    try:
        db = SessionLocal()
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
        return jsonify({'error': str(e)}), 500
    finally:
        if 'db' in locals():
            db.close()

if __name__ == '__main__':
    app.run(debug=True)