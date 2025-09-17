import os
import bcrypt
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from sqlalchemy.orm import Session
from itsdangerous import URLSafeTimedSerializer
import json

from database import SessionLocal, engine
from models import Base, User, Coin

# Criar tabelas se não existirem
Base.metadata.create_all(bind=engine)

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'sua-chave-secreta-super-forte')

# Configurar CORS
allowed_origins = os.environ.get('ALLOWED_ORIGINS', 'http://localhost:3000,http://127.0.0.1:5000').split(',')
CORS(app, origins=allowed_origins)

# Serializador para tokens
serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])

def get_db():
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()

def create_admin_if_not_exists():
    """Criar usuário admin se não existir"""
    db = SessionLocal()
    try:
        admin = db.query(User).filter(User.username == 'admin').first()
        if not admin:
            password_hash = bcrypt.hashpw('admin123'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            admin = User(username='admin', password_hash=password_hash, role='admin')
            db.add(admin)
            db.commit()
            print("✅ Usuário admin criado com sucesso")
        else:
            print("✅ Usuário admin já existe")
    except Exception as e:
        print(f"❌ Erro ao criar admin: {e}")
    finally:
        db.close()

# Rotas da API
@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({"status": "ok", "message": "API funcionando!"})

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({"error": "Username e password são obrigatórios"}), 400
    
    db = get_db()
    user = db.query(User).filter(User.username == username).first()
    
    if user and bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
        token = serializer.dumps({'user_id': user.id, 'role': user.role})
        return jsonify({
            "message": "Login realizado com sucesso",
            "token": token,
            "user": {
                "id": user.id,
                "username": user.username,
                "role": user.role
            }
        })
    else:
        return jsonify({"error": "Credenciais inválidas"}), 401

@app.route('/api/coins', methods=['GET'])
def get_coins():
    try:
        db = get_db()
        coins = db.query(Coin).all()
        
        coins_data = []
        for coin in coins:
            coins_data.append({
                "id": coin.id,
                "name": coin.name,
                "year": coin.year,
                "country": coin.country,
                "value": coin.value,
                "rarity": coin.rarity,
                "description": coin.description,
                "image_url": coin.image_url
            })
        
        return jsonify(coins_data)
    except Exception as e:
        return jsonify({"error": f"Erro ao buscar moedas: {str(e)}"}), 500

@app.route('/api/coins', methods=['POST'])
def create_coin():
    try:
        data = request.get_json()
        
        # Validar dados obrigatórios
        required_fields = ['name', 'year', 'country', 'value', 'rarity']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Campo '{field}' é obrigatório"}), 400
        
        db = get_db()
        
        new_coin = Coin(
            name=data['name'],
            year=data['year'],
            country=data['country'],
            value=data['value'],
            rarity=data['rarity'],
            description=data.get('description', ''),
            image_url=data.get('image_url', '')
        )
        
        db.add(new_coin)
        db.commit()
        db.refresh(new_coin)
        
        return jsonify({
            "message": "Moeda criada com sucesso",
            "coin": {
                "id": new_coin.id,
                "name": new_coin.name,
                "year": new_coin.year,
                "country": new_coin.country,
                "value": new_coin.value,
                "rarity": new_coin.rarity,
                "description": new_coin.description,
                "image_url": new_coin.image_url
            }
        }), 201
        
    except Exception as e:
        return jsonify({"error": f"Erro ao criar moeda: {str(e)}"}), 500

# Inicializar admin na primeira execução
create_admin_if_not_exists()

# Exportar para Vercel
app = app