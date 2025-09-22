"""
Ultra simples para debug
"""

from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api/test')
def test():
    return jsonify({"message": "API funcionando"})

if __name__ == '__main__':
    app.run()