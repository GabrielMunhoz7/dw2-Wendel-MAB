import os, json
import psycopg2
from psycopg2.extras import RealDictCursor

# Conexão única reutilizável
_conn = None

def get_conn():
    global _conn
    if _conn and _conn.closed == 0:
        return _conn
    db_url = os.environ.get('DATABASE_URL')
    if not db_url:
        raise RuntimeError('DATABASE_URL não configurada')
    _conn = psycopg2.connect(db_url)
    return _conn

def handler(request):
    method = request.get('method', 'GET')

    if method == 'GET':
        try:
            conn = get_conn()
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute('SELECT id, name, period, region, material, denomination, historia, contexto, referencia, image_front, image_back FROM coins ORDER BY id')
                rows = cur.fetchall()
            return {
                'statusCode': 200,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps(rows)
            }
        except Exception as e:
            return {
                'statusCode': 500,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'error': str(e)})
            }

    if method == 'POST':
        try:
            body = request.get('body') or '{}'
            data = json.loads(body)
            required = ['name','period','region','material']
            missing = [r for r in required if not data.get(r)]
            if missing:
                return {
                    'statusCode': 400,
                    'headers': {'Content-Type': 'application/json'},
                    'body': json.dumps({'error': f'Campos obrigatórios faltando: {", ".join(missing)}'})
                }
            conn = get_conn()
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute('''INSERT INTO coins (name, period, region, material, denomination, historia, contexto, referencia, image_front, image_back)
                               VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id''',
                            [data.get('name'), data.get('period'), data.get('region'), data.get('material'),
                             data.get('denomination'), data.get('historia'), data.get('contexto'), data.get('referencia'),
                             data.get('image_front'), data.get('image_back')])
                new_id = cur.fetchone()['id']
                conn.commit()
            return {
                'statusCode': 201,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'id': new_id, 'success': True})
            }
        except Exception as e:
            if _conn: _conn.rollback()
            return {
                'statusCode': 500,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'error': str(e)})
            }

    return {
        'statusCode': 405,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps({'error': 'Método não permitido'})
    }
