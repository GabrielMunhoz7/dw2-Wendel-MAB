"""
Endpoint de diagnóstico simples para debug na Vercel
"""

from flask import Flask, jsonify
import os
import sys

app = Flask(__name__)

@app.route('/api/debug')
def debug():
    """Endpoint simples para debug"""
    try:
        debug_info = {
            "status": "ok",
            "python_version": sys.version,
            "environment_vars": {
                "DATABASE_URL": "CONFIGURADA" if os.environ.get("DATABASE_URL") else "NÃO CONFIGURADA",
                "SECRET_KEY": "CONFIGURADA" if os.environ.get("SECRET_KEY") else "NÃO CONFIGURADA", 
                "ALLOWED_ORIGINS": "CONFIGURADA" if os.environ.get("ALLOWED_ORIGINS") else "NÃO CONFIGURADA"
            }
        }
        return jsonify(debug_info)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/simple')
def simple():
    """Endpoint super simples"""
    return {"message": "API funcionando!"}

if __name__ == '__main__':
    app.run(debug=True)