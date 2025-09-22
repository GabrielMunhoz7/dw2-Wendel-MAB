"""
Versão ultra-simples para debug na Vercel
"""

from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api/simple')
def simple():
    return {"message": "API funcionando", "status": "ok"}

@app.route('/api/env')
def check_env():
    import os
    return {
        "DATABASE_URL": bool(os.environ.get("DATABASE_URL")),
        "SECRET_KEY": bool(os.environ.get("SECRET_KEY")),
        "ALLOWED_ORIGINS": bool(os.environ.get("ALLOWED_ORIGINS"))
    }

if __name__ == '__main__':
    app.run(debug=True)