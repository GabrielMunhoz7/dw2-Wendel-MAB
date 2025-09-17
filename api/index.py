import sys
import os

# Adicionar o diretório backend ao path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from app import app

def handler(request):
    return app

# Para compatibilidade com Vercel
app = app