from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api')
def hello():
    return jsonify({"message": "Hello from Vercel!", "status": "working"})

@app.route('/api/test')
def test():
    return jsonify({"test": "API funcionando perfeitamente!"})

# Para Vercel
def handler(request):
    return app