import os
import bcrypt
from flask import Flask, request, jsonify
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
allowed_origins = os.environ.get('ALLOWED_ORIGINS', '*').split(',')
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

def verify_token(token):
    """Verificar token JWT"""
    try:
        data = serializer.loads(token, max_age=86400)  # 24 horas
        return data
    except:
        return None

# Rotas da API
@app.route('/api', methods=['GET'])
@app.route('/api/', methods=['GET'])
def hello():
    return jsonify({"message": "API do Catálogo de Moedas", "status": "online", "version": "1.0"})

@app.route('/api/health', methods=['GET'])
def health():
    try:
        # Testar conexão com banco
        db = get_db()
        db.execute("SELECT 1")
        return jsonify({
            "status": "healthy", 
            "database": "connected",
            "message": "API funcionando perfeitamente!"
        })
    except Exception as e:
        return jsonify({
            "status": "error", 
            "database": "disconnected",
            "error": str(e)
        }), 500

@app.route('/api/login', methods=['POST'])
def login():
    try:
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
    except Exception as e:
        return jsonify({"error": f"Erro no login: {str(e)}"}), 500

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
        # Verificar autenticação
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({"error": "Token de autorização necessário"}), 401
        
        token = auth_header.split(' ')[1]
        user_data = verify_token(token)
        if not user_data:
            return jsonify({"error": "Token inválido"}), 401
        
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

@app.route('/api/coins/<int:coin_id>', methods=['PUT'])
def update_coin(coin_id):
    try:
        # Verificar autenticação
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({"error": "Token de autorização necessário"}), 401
        
        token = auth_header.split(' ')[1]
        user_data = verify_token(token)
        if not user_data:
            return jsonify({"error": "Token inválido"}), 401
        
        data = request.get_json()
        db = get_db()
        
        coin = db.query(Coin).filter(Coin.id == coin_id).first()
        if not coin:
            return jsonify({"error": "Moeda não encontrada"}), 404
        
        # Atualizar campos
        if 'name' in data:
            coin.name = data['name']
        if 'year' in data:
            coin.year = data['year']
        if 'country' in data:
            coin.country = data['country']
        if 'value' in data:
            coin.value = data['value']
        if 'rarity' in data:
            coin.rarity = data['rarity']
        if 'description' in data:
            coin.description = data['description']
        if 'image_url' in data:
            coin.image_url = data['image_url']
        
        db.commit()
        db.refresh(coin)
        
        return jsonify({
            "message": "Moeda atualizada com sucesso",
            "coin": {
                "id": coin.id,
                "name": coin.name,
                "year": coin.year,
                "country": coin.country,
                "value": coin.value,
                "rarity": coin.rarity,
                "description": coin.description,
                "image_url": coin.image_url
            }
        })
        
    except Exception as e:
        return jsonify({"error": f"Erro ao atualizar moeda: {str(e)}"}), 500

@app.route('/api/coins/<int:coin_id>', methods=['DELETE'])
def delete_coin(coin_id):
    try:
        # Verificar autenticação
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({"error": "Token de autorização necessário"}), 401
        
        token = auth_header.split(' ')[1]
        user_data = verify_token(token)
        if not user_data:
            return jsonify({"error": "Token inválido"}), 401
        
        db = get_db()
        
        coin = db.query(Coin).filter(Coin.id == coin_id).first()
        if not coin:
            return jsonify({"error": "Moeda não encontrada"}), 404
        
        db.delete(coin)
        db.commit()
        
        return jsonify({"message": "Moeda deletada com sucesso"})
        
    except Exception as e:
        return jsonify({"error": f"Erro ao deletar moeda: {str(e)}"}), 500

# Inicializar admin na primeira execução
try:
    create_admin_if_not_exists()
except Exception as e:
    print(f"Erro na inicialização: {e}")

# Exportar para Vercel
app = app