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
@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.username == username).first()
        if user and bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
            token = serializer.dumps({'user_id': user.id, 'username': user.username})
            return jsonify({'success': True, 'token': token})
        else:
            return jsonify({'success': False, 'message': 'Credenciais inválidas'}), 401
    finally:
        db.close()

@app.route('/api/coins', methods=['GET'])
def get_coins():
    db = SessionLocal()
    try:
        coins = db.query(Coin).all()
        return jsonify([{
            'id': c.id,
            'name': c.name,
            'period': c.period,
            'region': c.region,
            'material': c.material,
            'denomination': c.denomination,
            'year': c.year,
            'description': c.description,
            'historia': c.historia,
            'contexto': c.contexto,
            'referencia': c.referencia,
            'image_front': c.image_front,
            'image_back': c.image_back
        } for c in coins])
    finally:
        db.close()

@app.route('/api/coins', methods=['POST'])
def create_coin():
    # Verificar token
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    try:
        data = serializer.loads(token, max_age=86400)  # 24 horas
    except:
        return jsonify({'error': 'Token inválido'}), 401
    
    coin_data = request.json
    db = SessionLocal()
    try:
        coin = Coin(**coin_data)
        db.add(coin)
        db.commit()
        db.refresh(coin)
        return jsonify({'id': coin.id, 'message': 'Moeda criada com sucesso'})
    finally:
        db.close()

@app.route('/api/coins/<int:coin_id>', methods=['PUT'])
def update_coin(coin_id):
    # Verificar token
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    try:
        data = serializer.loads(token, max_age=86400)
    except:
        return jsonify({'error': 'Token inválido'}), 401
    
    coin_data = request.json
    db = SessionLocal()
    try:
        coin = db.query(Coin).filter(Coin.id == coin_id).first()
        if not coin:
            return jsonify({'error': 'Moeda não encontrada'}), 404
        
        for key, value in coin_data.items():
            setattr(coin, key, value)
        
        db.commit()
        return jsonify({'message': 'Moeda atualizada com sucesso'})
    finally:
        db.close()

@app.route('/api/coins/<int:coin_id>', methods=['DELETE'])
def delete_coin(coin_id):
    # Verificar token
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    try:
        data = serializer.loads(token, max_age=86400)
    except:
        return jsonify({'error': 'Token inválido'}), 401
    
    db = SessionLocal()
    try:
        coin = db.query(Coin).filter(Coin.id == coin_id).first()
        if not coin:
            return jsonify({'error': 'Moeda não encontrada'}), 404
        
        db.delete(coin)
        db.commit()
        return jsonify({'message': 'Moeda removida com sucesso'})
    finally:
        db.close()

# Servir arquivos estáticos (frontend)
@app.route('/')
def serve_frontend():
    return send_from_directory('../frontend', 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('../frontend', filename)

if __name__ == '__main__':
    create_admin_if_not_exists()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)