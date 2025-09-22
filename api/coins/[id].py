import os, json, re
import psycopg2
from psycopg2.extras import RealDictCursor

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
    path = request.get('path', '')  # e.g. /api/coins/3
    m = re.search(r'/coins/(\d+)$', path)
    if not m:
        return {'statusCode': 400,'body': json.dumps({'error':'ID inválido'}),'headers':{'Content-Type':'application/json'}}
    coin_id = int(m.group(1))

    if method == 'GET':
        try:
            conn = get_conn()
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute('SELECT id, name, period, region, material, denomination, historia, contexto, referencia, image_front, image_back FROM coins WHERE id=%s', [coin_id])
                row = cur.fetchone()
            if not row:
                return {'statusCode':404,'headers':{'Content-Type':'application/json'},'body':json.dumps({'error':'Moeda não encontrada'})}
            return {'statusCode':200,'headers':{'Content-Type':'application/json'},'body':json.dumps(row)}
        except Exception as e:
            return {'statusCode':500,'headers':{'Content-Type':'application/json'},'body':json.dumps({'error':str(e)})}

    if method in ('PUT','PATCH'):
        try:
            body = request.get('body') or '{}'
            data = json.loads(body)
            fields = ['name','period','region','material','denomination','historia','contexto','referencia','image_front','image_back']
            sets = []
            values = []
            for f in fields:
                if f in data:
                    sets.append(f"{f}=%s")
                    values.append(data[f])
            if not sets:
                return {'statusCode':400,'headers':{'Content-Type':'application/json'},'body':json.dumps({'error':'Nenhum campo para atualizar'})}
            values.append(coin_id)
            conn = get_conn()
            with conn.cursor() as cur:
                cur.execute(f"UPDATE coins SET {', '.join(sets)} WHERE id=%s", values)
                conn.commit()
            return {'statusCode':200,'headers':{'Content-Type':'application/json'},'body':json.dumps({'success':True})}
        except Exception as e:
            if _conn: _conn.rollback()
            return {'statusCode':500,'headers':{'Content-Type':'application/json'},'body':json.dumps({'error':str(e)})}

    if method == 'DELETE':
        try:
            conn = get_conn()
            with conn.cursor() as cur:
                cur.execute('DELETE FROM coins WHERE id=%s', [coin_id])
                conn.commit()
            return {'statusCode':204,'headers':{'Content-Type':'application/json'},'body':''}
        except Exception as e:
            if _conn: _conn.rollback()
            return {'statusCode':500,'headers':{'Content-Type':'application/json'},'body':json.dumps({'error':str(e)})}

    return {'statusCode':405,'headers':{'Content-Type':'application/json'},'body':json.dumps({'error':'Método não permitido'})}
