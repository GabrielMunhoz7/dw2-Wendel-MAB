"""
API ultra-simples para debug na Vercel
"""

from flask import Flask, jsonify
import os

app = Flask(__name__)

@app.route('/api/test')
def test():
    """Endpoint de teste simples"""
    return jsonify({"status": "working", "message": "API básica funcionando"})

@app.route('/api/env-check')
def env_check():
    """Verificar variáveis de ambiente"""
    return jsonify({
        "DATABASE_URL_exists": bool(os.environ.get("DATABASE_URL")),
        "SECRET_KEY_exists": bool(os.environ.get("SECRET_KEY")),
        "ALLOWED_ORIGINS_exists": bool(os.environ.get("ALLOWED_ORIGINS")),
        "DATABASE_URL_prefix": os.environ.get("DATABASE_URL", "")[:20] if os.environ.get("DATABASE_URL") else "None"
    })

@app.route('/api/db-test')
def db_test():
    """Teste básico de conexão com banco"""
    try:
        # Tentar importar e conectar
        from sqlalchemy import create_engine, text
        
        database_url = os.environ.get("DATABASE_URL")
        if not database_url:
            return jsonify({"error": "DATABASE_URL não encontrada"}), 500
        
        engine = create_engine(database_url, pool_pre_ping=True)
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1 as test"))
            return jsonify({"status": "connected", "test_query": "success"})
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)