from flask import Flask, jsonify, request, send_from_directory, abort
from sqlalchemy.orm import Session
import os
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from functools import wraps

from database import SessionLocal, engine
import models

# Create DB tables if they don't exist
models.Base.metadata.create_all(bind=engine)

app = Flask(__name__, static_folder=os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'frontend')))
app.config['SECRET_KEY'] = 'change-me-to-a-secure-random-value'
serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.route('/api/coins', methods=['GET'])
def list_coins():
    db = next(get_db())
    coins = db.query(models.Coin).all()
    result = [c.__dict__.copy() for c in coins]
    # remove _sa_instance_state
    for r in result:
        r.pop('_sa_instance_state', None)
    return jsonify(result)


def verify_token(token: str):
    try:
        data = serializer.loads(token, max_age=60*60*24)  # 1 day
        return data.get('username')
    except (BadSignature, SignatureExpired):
        return None


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.headers.get('Authorization')
        if not auth or not auth.startswith('Bearer '):
            return jsonify({'detail': 'Authentication required'}), 401
        token = auth.split(' ', 1)[1]
        user = verify_token(token)
        if not user:
            return jsonify({'detail': 'Invalid or expired token'}), 401
        return f(*args, **kwargs)
    return decorated


@app.route('/api/coins/<int:coin_id>', methods=['GET'])
def get_coin(coin_id):
    db = next(get_db())
    coin = db.query(models.Coin).filter(models.Coin.id == coin_id).first()
    if not coin:
        abort(404)
    data = coin.__dict__.copy()
    data.pop('_sa_instance_state', None)
    return jsonify(data)


@app.route('/api/coins', methods=['POST'])
@app.route('/api/coins', methods=['POST'])
@login_required
def create_coin():
    payload = request.get_json() or {}
    db = next(get_db())
    coin = models.Coin(**payload)
    db.add(coin)
    db.commit()
    db.refresh(coin)
    data = coin.__dict__.copy(); data.pop('_sa_instance_state', None)
    return jsonify(data), 201


@app.route('/api/coins/<int:coin_id>', methods=['PUT'])
@app.route('/api/coins/<int:coin_id>', methods=['PUT'])
@login_required
def update_coin(coin_id):
    payload = request.get_json() or {}
    db = next(get_db())
    coin = db.query(models.Coin).filter(models.Coin.id == coin_id).first()
    if not coin:
        abort(404)
    for k, v in payload.items():
        if hasattr(coin, k):
            setattr(coin, k, v)
    db.commit()
    db.refresh(coin)
    data = coin.__dict__.copy(); data.pop('_sa_instance_state', None)
    return jsonify(data)


@app.route('/api/coins/<int:coin_id>', methods=['DELETE'])
@app.route('/api/coins/<int:coin_id>', methods=['DELETE'])
@login_required
def delete_coin(coin_id):
    db = next(get_db())
    coin = db.query(models.Coin).filter(models.Coin.id == coin_id).first()
    if not coin:
        abort(404)
    db.delete(coin)
    db.commit()
    return jsonify({'ok': True})


@app.route('/api/login', methods=['POST'])
def login():
    payload = request.get_json() or {}
    username = payload.get('username')
    password = payload.get('password')
    if not username or not password:
        return jsonify({'detail': 'username and password required'}), 400

    db = next(get_db())
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user or not user.check_password(password):
        return jsonify({'detail': 'invalid credentials'}), 401

    token = serializer.dumps({'username': username})
    return jsonify({'token': token})


# Serve frontend static files
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_frontend(path):
    static_dir = app.static_folder
    if path != '' and os.path.exists(os.path.join(static_dir, path)):
        return send_from_directory(static_dir, path)
    return send_from_directory(static_dir, 'index.html')


if __name__ == '__main__':
    # debug server for development
    app.run(host='127.0.0.1', port=5000, debug=True)
