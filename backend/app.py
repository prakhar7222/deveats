import os
from decimal import Decimal
from flask import Flask, jsonify, request
import psycopg
from psycopg.rows import dict_row

app = Flask(__name__)

def db():
    return psycopg.connect(host=os.getenv('DB_HOST','localhost'), port=os.getenv('DB_PORT','5432'), dbname=os.getenv('DB_NAME','deveats'), user=os.getenv('DB_USER','deveats'), password=os.getenv('DB_PASSWORD','deveats'), row_factory=dict_row)

@app.get('/api/health')
def health():
    try:
        with db() as conn:
            with conn.cursor() as cur: cur.execute('SELECT 1')
        return jsonify({'status':'healthy','database':'reachable'})
    except Exception:
        return jsonify({'status':'unhealthy','database':'unreachable'}), 503

@app.get('/api/restaurants')
def restaurants():
    with db() as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT id,name,address,is_open FROM restaurants ORDER BY id')
            return jsonify(cur.fetchall())

@app.get('/api/restaurants/<int:rid>')
def restaurant(rid):
    with db() as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT id,name,address,is_open FROM restaurants WHERE id=%s',(rid,))
            row=cur.fetchone()
    return jsonify(row) if row else (jsonify({'error':'Restaurant not found'}),404)

@app.get('/api/restaurants/<int:rid>/menu')
def menu(rid):
    with db() as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT id,name,description,price,available FROM menu_items WHERE restaurant_id=%s ORDER BY id',(rid,))
            rows=cur.fetchall()
    for row in rows: row['price']=float(row['price'])
    return jsonify(rows)

@app.get('/api/orders/<int:oid>')
def order(oid):
    with db() as conn:
        with conn.cursor() as cur:
            cur.execute('SELECT id,customer_name,restaurant_id,total_amount,status,created_at FROM orders WHERE id=%s',(oid,))
            row=cur.fetchone()
    if not row: return jsonify({'error':'Order not found'}),404
    row['total_amount']=float(row['total_amount']); row['created_at']=row['created_at'].isoformat()
    return jsonify(row)

@app.post('/api/orders')
def create_order():
    data=request.get_json(silent=True) or {}; name=data.get('customer_name'); rid=data.get('restaurant_id'); items=data.get('items')
    if not name or not rid or not isinstance(items,list) or not items:
        return jsonify({'error':'customer_name, restaurant_id and items are required'}),400
    try:
        with db() as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT id FROM restaurants WHERE id=%s AND is_open=TRUE',(rid,))
                if not cur.fetchone(): return jsonify({'error':'Restaurant not found or closed'}),404
                total=Decimal('0'); valid=[]
                for item in items:
                    mid=item.get('menu_item_id'); qty=item.get('quantity')
                    if not isinstance(qty,int) or qty<=0: return jsonify({'error':'quantity must be positive'}),400
                    cur.execute('SELECT id,price FROM menu_items WHERE id=%s AND restaurant_id=%s AND available=TRUE',(mid,rid))
                    mi=cur.fetchone()
                    if not mi: return jsonify({'error':f'Menu item {mid} not available'}),400
                    total += mi['price']*qty; valid.append((mid,qty,mi['price']))
                cur.execute("INSERT INTO orders(customer_name,restaurant_id,total_amount,status) VALUES(%s,%s,%s,'PLACED') RETURNING id,created_at",(name,rid,total))
                o=cur.fetchone()
                for mid,qty,price in valid: cur.execute('INSERT INTO order_items(order_id,menu_item_id,quantity,unit_price) VALUES(%s,%s,%s,%s)',(o['id'],mid,qty,price))
                conn.commit()
        return jsonify({'order_id':o['id'],'status':'PLACED','total_amount':float(total)}),201
    except Exception as exc:
        return jsonify({'error':'Could not create order','detail':str(exc)}),500

if __name__=='__main__': app.run(host='0.0.0.0',port=5000)
