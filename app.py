# app.py
from flask import Flask, render_template, request, jsonify
import json
from database import create_database_if_not_exists, initialize_tables, get_connection
from psycopg2.extras import RealDictCursor
from datetime import date

app = Flask(__name__, static_folder='static', template_folder='templates')

# --- Inicialización DB al arrancar la app ---
with app.app_context():
    create_database_if_not_exists()
    initialize_tables()


def query_dict(sql, params=None, many=True):
    conn = get_connection()
    try:
        with conn:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(sql, params or ())
                if cur.description:
                    if many:
                        return cur.fetchall()
                    else:
                        return cur.fetchone()
                return None
    finally:
        conn.close()

def execute(sql, params=None, fetchone=False):
    conn = get_connection()
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(sql, params or ())
                if fetchone:
                    return cur.fetchone()
                return None
    finally:
        conn.close()

# --- Rutas de páginas ---
@app.route('/')
def login_page():
    return render_template('login.html')

@app.route('/admin')
def admin_page():
    return render_template('admin.html')

@app.route('/about')
def about():
    return render_template('about.html')

#   EMPLEADO
@app.route('/api/empleados', methods=['GET'])
def list_empleados():
    rows = query_dict("SELECT identificacion, nombre, cargo, fecha_ingreso::text AS fecha_ingreso, sueldo FROM empleado ORDER BY nombre;")
    return jsonify(rows)

@app.route('/api/empleados', methods=['POST'])
def create_empleado():
    data = request.json
    sql = """INSERT INTO empleado (identificacion, nombre, cargo, fecha_ingreso, sueldo)
             VALUES (%s,%s,%s,%s,%s)"""
    params = (data.get('identificacion'), data.get('nombre'), data.get('cargo'), data.get('fecha_ingreso'), data.get('sueldo'))
    try:
        execute(sql, params)
        return jsonify({'ok': True}), 201
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 400

@app.route('/api/empleados/<identificacion>', methods=['PUT'])
def update_empleado(identificacion):
    data = request.json
    sql = """UPDATE empleado SET nombre=%s, cargo=%s, fecha_ingreso=%s, sueldo=%s WHERE identificacion=%s"""
    params = (data.get('nombre'), data.get('cargo'), data.get('fecha_ingreso'), data.get('sueldo'), identificacion)
    execute(sql, params)
    return jsonify({'ok': True})

@app.route('/api/empleados/<identificacion>', methods=['DELETE'])
def delete_empleado(identificacion):
    try:
        execute("DELETE FROM empleado WHERE identificacion=%s", (identificacion,))
        return jsonify({'ok': True})
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 400



#   MAQUINARIA

@app.route('/api/maquinaria', methods=['GET'])
def list_maquinaria():
    rows = query_dict("SELECT id, nombre, tipo, modelo, estado FROM maquinaria ORDER BY id;")
    return jsonify(rows)

@app.route('/api/maquinaria', methods=['POST'])
def create_maquinaria():
    data = request.json
    sql = "INSERT INTO maquinaria (nombre, tipo, modelo, estado) VALUES (%s,%s,%s,%s) RETURNING id;"
    conn = get_connection()
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(sql, (data.get('nombre'), data.get('tipo'), data.get('modelo'), data.get('estado')))
                new_id = cur.fetchone()[0]
        return jsonify({'ok': True, 'id': new_id}), 201
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 400
    finally:
        conn.close()

@app.route('/api/maquinaria/<int:id>', methods=['PUT'])
def update_maquinaria(id):
    data = request.json
    execute("UPDATE maquinaria SET nombre=%s, tipo=%s, modelo=%s, estado=%s WHERE id=%s",
            (data.get('nombre'), data.get('tipo'), data.get('modelo'), data.get('estado'), id))
    return jsonify({'ok': True})

@app.route('/api/maquinaria/<int:id>', methods=['DELETE'])
def delete_maquinaria(id):
    try:
        execute("DELETE FROM maquinaria WHERE id=%s", (id,))
        return jsonify({'ok': True})
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 400



#  ANIMAL

@app.route('/api/animales', methods=['GET'])
def list_animales():
    rows = query_dict("SELECT id, nombre, especie, raza, sexo, estado FROM animal ORDER BY id;")
    return jsonify(rows)

@app.route('/api/animales', methods=['POST'])
def create_animal():
    data = request.json
    sql = "INSERT INTO animal (nombre, especie, raza, sexo, estado) VALUES (%s,%s,%s,%s,%s) RETURNING id;"
    conn = get_connection()
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(sql, (data.get('nombre'), data.get('especie'), data.get('raza'), data.get('sexo'), data.get('estado')))
                new_id = cur.fetchone()[0]
        return jsonify({'ok': True, 'id': new_id}), 201
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 400
    finally:
        conn.close()

@app.route('/api/animales/<int:id>', methods=['PUT'])
def update_animal(id):
    data = request.json
    execute("UPDATE animal SET nombre=%s, especie=%s, raza=%s, sexo=%s, estado=%s WHERE id=%s",
            (data.get('nombre'), data.get('especie'), data.get('raza'), data.get('sexo'), data.get('estado'), id))
    return jsonify({'ok': True})

@app.route('/api/animales/<int:id>', methods=['DELETE'])
def delete_animal(id):
    try:
        execute("DELETE FROM animal WHERE id=%s", (id,))
        return jsonify({'ok': True})
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 400


#  CULTIVO

@app.route('/api/cultivos', methods=['GET'])
def list_cultivos():
    rows = query_dict("SELECT id, nombre, tipo, epoca, estado, fecha_siembra::text AS fecha_siembra FROM cultivo ORDER BY id;")
    return jsonify(rows)

@app.route('/api/cultivos', methods=['POST'])
def create_cultivo():
    data = request.json
    sql = "INSERT INTO cultivo (nombre, tipo, epoca, estado, fecha_siembra) VALUES (%s,%s,%s,%s,%s) RETURNING id;"
    conn = get_connection()
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(sql, (data.get('nombre'), data.get('tipo'), data.get('epoca'), data.get('estado'), data.get('fecha_siembra')))
                new_id = cur.fetchone()[0]
        return jsonify({'ok': True, 'id': new_id}), 201
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 400
    finally:
        conn.close()

@app.route('/api/cultivos/<int:id>', methods=['PUT'])
def update_cultivo(id):
    data = request.json
    execute("UPDATE cultivo SET nombre=%s, tipo=%s, epoca=%s, estado=%s, fecha_siembra=%s WHERE id=%s",
            (data.get('nombre'), data.get('tipo'), data.get('epoca'), data.get('estado'), data.get('fecha_siembra'), id))
    return jsonify({'ok': True})

@app.route('/api/cultivos/<int:id>', methods=['DELETE'])
def delete_cultivo(id):
    try:
        execute("DELETE FROM cultivo WHERE id=%s", (id,))
        return jsonify({'ok': True})
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 400


#   RECURSOS

@app.route('/api/recursos', methods=['GET'])
def list_recursos():
    rows = query_dict("SELECT id, nombre, tipo_recurso, stock FROM recursos ORDER BY id;")
    return jsonify(rows)

@app.route('/api/recursos', methods=['POST'])
def create_recurso():
    data = request.json
    sql = "INSERT INTO recursos (nombre, tipo_recurso, stock) VALUES (%s,%s,%s) RETURNING id;"
    conn = get_connection()
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(sql, (data.get('nombre'), data.get('tipo_recurso'), data.get('stock')))
                new_id = cur.fetchone()[0]
        return jsonify({'ok': True, 'id': new_id}), 201
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 400
    finally:
        conn.close()

@app.route('/api/recursos/<int:id>', methods=['PUT'])
def update_recurso(id):
    data = request.json
    execute("UPDATE recursos SET nombre=%s, tipo_recurso=%s, stock=%s WHERE id=%s",
            (data.get('nombre'), data.get('tipo_recurso'), data.get('stock'), id))
    return jsonify({'ok': True})

@app.route('/api/recursos/<int:id>', methods=['DELETE'])
def delete_recurso(id):
    try:
        execute("DELETE FROM recursos WHERE id=%s", (id,))
        return jsonify({'ok': True})
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 400



# PRODUCTO

@app.route('/api/productos', methods=['GET'])
def list_productos():
    rows = query_dict("SELECT identificacion, nombre, tipo, precio FROM producto ORDER BY nombre;")
    return jsonify(rows)

@app.route('/api/productos', methods=['POST'])
def create_producto():
    data = request.json
    sql = "INSERT INTO producto (identificacion, nombre, tipo, precio) VALUES (%s,%s,%s,%s)"
    try:
        execute(sql, (data.get('identificacion'), data.get('nombre'), data.get('tipo'), data.get('precio')))
        return jsonify({'ok': True}), 201
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 400

@app.route('/api/productos/<identificacion>', methods=['PUT'])
def update_producto(identificacion):
    data = request.json
    execute("UPDATE producto SET nombre=%s, tipo=%s, precio=%s WHERE identificacion=%s",
            (data.get('nombre'), data.get('tipo'), data.get('precio'), identificacion))
    return jsonify({'ok': True})

@app.route('/api/productos/<identificacion>', methods=['DELETE'])
def delete_producto(identificacion):
    try:
        execute("DELETE FROM producto WHERE identificacion=%s", (identificacion,))
        return jsonify({'ok': True})
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 400



#CLIENTE
@app.route('/api/clientes', methods=['GET'])
def list_clientes():
    rows = query_dict("SELECT documento, nombre, direccion, telefono, email FROM cliente ORDER BY nombre;")
    return jsonify(rows)

@app.route('/api/clientes', methods=['POST'])
def create_cliente():
    data = request.json
    sql = "INSERT INTO cliente (documento, nombre, direccion, telefono, email) VALUES (%s,%s,%s,%s,%s)"
    try:
        execute(sql, (data.get('documento'), data.get('nombre'), data.get('direccion'), data.get('telefono'), data.get('email')))
        return jsonify({'ok': True}), 201
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 400

@app.route('/api/clientes/<documento>', methods=['PUT'])
def update_cliente(documento):
    data = request.json
    execute("UPDATE cliente SET nombre=%s, direccion=%s, telefono=%s, email=%s WHERE documento=%s",
            (data.get('nombre'), data.get('direccion'), data.get('telefono'), data.get('email'), documento))
    return jsonify({'ok': True})

@app.route('/api/clientes/<documento>', methods=['DELETE'])
def delete_cliente(documento):
    try:
        execute("DELETE FROM cliente WHERE documento=%s", (documento,))
        return jsonify({'ok': True})
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 400


#  VENTAS (cabecera + detalle)

@app.route('/api/ventas', methods=['GET'])
def list_ventas():
    rows = query_dict("""
        SELECT v.id, v.documento_cliente, v.fecha::text AS fecha, v.total,
               c.nombre as cliente_nombre
        FROM venta v
        LEFT JOIN cliente c ON c.documento = v.documento_cliente
        ORDER BY v.fecha DESC
    """)
    return jsonify(rows)

@app.route('/api/ventas/<int:id>', methods=['GET'])
def get_venta(id):
    venta = query_dict("SELECT id, documento_cliente, fecha::text AS fecha, total FROM venta WHERE id=%s", (id,), many=False)
    if not venta:
        return jsonify({'ok': False, 'error': 'Venta no encontrada'}), 404
    detalles = query_dict("SELECT identificacion_producto, cantidad, precio_unit FROM venta_detalle WHERE id_venta=%s", (id,))
    venta['detalles'] = detalles
    return jsonify(venta)

@app.route('/api/ventas', methods=['POST'])
def create_venta():
    """
    Espera JSON:
    {
      "documento_cliente": "123",
      "items": [
        {"identificacion_producto":"P01","cantidad":2,"precio_unit":10000},
        ...
      ]
    }
    """
    data = request.json
    items = data.get('items', [])
    if not items:
        return jsonify({'ok': False, 'error': 'Se requieren items'}), 400

    # calcular total
    total = sum([float(it['cantidad']) * float(it['precio_unit']) for it in items])

    conn = get_connection()
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute("INSERT INTO venta (documento_cliente, total) VALUES (%s,%s) RETURNING id;", (data.get('documento_cliente'), total))
                venta_id = cur.fetchone()[0]
                sql_det = "INSERT INTO venta_detalle (id_venta, identificacion_producto, cantidad, precio_unit) VALUES (%s,%s,%s,%s);"
                for it in items:
                    cur.execute(sql_det, (venta_id, it['identificacion_producto'], it['cantidad'], it['precio_unit']))
        return jsonify({'ok': True, 'id': venta_id}), 201
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 400
    finally:
        conn.close()



#  CONSUMOS (ANIMAL / CULTIVO)

@app.route('/api/consumo/animal', methods=['GET'])
def list_consumo_animal():
    rows = query_dict("SELECT id, id_animal, id_recurso, destino, cantidad, observacion, fecha::text AS fecha FROM consumo_animal ORDER BY fecha DESC;")
    return jsonify(rows)

@app.route('/api/consumo/animal', methods=['POST'])
def create_consumo_animal():
    data = request.json
    sql = """INSERT INTO consumo_animal (id_animal, id_recurso, destino, cantidad, observacion, fecha)
             VALUES (%s,%s,%s,%s,%s,%s) RETURNING id;"""
    conn = get_connection()
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(sql, (data.get('id_animal'), data.get('id_recurso'), data.get('destino'), data.get('cantidad'), data.get('observacion'), data.get('fecha')))
                new_id = cur.fetchone()[0]
        return jsonify({'ok': True, 'id': new_id}), 201
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 400
    finally:
        conn.close()

@app.route('/api/consumo/cultivo', methods=['GET'])
def list_consumo_cultivo():
    rows = query_dict("SELECT id, id_cultivo, id_recurso, destino, cantidad, observacion, fecha::text AS fecha FROM consumo_cultivo ORDER BY fecha DESC;")
    return jsonify(rows)

@app.route('/api/consumo/cultivo', methods=['POST'])
def create_consumo_cultivo():
    data = request.json
    sql = """INSERT INTO consumo_cultivo (id_cultivo, id_recurso, destino, cantidad, observacion, fecha)
             VALUES (%s,%s,%s,%s,%s,%s) RETURNING id;"""
    conn = get_connection()
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(sql, (data.get('id_cultivo'), data.get('id_recurso'), data.get('destino'), data.get('cantidad'), data.get('observacion'), data.get('fecha')))
                new_id = cur.fetchone()[0]
        return jsonify({'ok': True, 'id': new_id}), 201
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 400
    finally:
        conn.close()

#  Misc: comprobar conexión
@app.route('/api/ping', methods=['GET'])
def ping():
    try:
        r = query_dict("SELECT 1 as ok", many=False)
        return jsonify({'ok': True})
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 500


# --- Run ---
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
