from flask import Blueprint, request, jsonify
from database import query_dict, execute, get_connection

bp = Blueprint('api', __name__)

# EMPLEADO
@bp.route('/api/empleados', methods=['GET'])
def list_empleados():
    rows = query_dict("SELECT identificacion, nombre, cargo, fecha_ingreso::text AS fecha_ingreso, sueldo FROM empleado ORDER BY nombre;")
    return jsonify(rows)

@bp.route('/api/empleados', methods=['POST'])
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

@bp.route('/api/empleados/<identificacion>', methods=['PUT'])
def update_empleado(identificacion):
    data = request.json
    sql = """UPDATE empleado SET nombre=%s, cargo=%s, fecha_ingreso=%s, sueldo=%s WHERE identificacion=%s"""
    params = (data.get('nombre'), data.get('cargo'), data.get('fecha_ingreso'), data.get('sueldo'), identificacion)
    execute(sql, params)
    return jsonify({'ok': True})

@bp.route('/api/empleados/<identificacion>', methods=['DELETE'])
def delete_empleado(identificacion):
    try:
        execute("DELETE FROM empleado WHERE identificacion=%s", (identificacion,))
        return jsonify({'ok': True})
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 400


# Cascade delete for empleado
@bp.route('/api/empleados/<identificacion>/cascade', methods=['DELETE'])
def delete_empleado_cascade(identificacion):
    conn = get_connection()
    try:
        with conn:
            with conn.cursor() as cur:
                # counts before deletion
                cur.execute("SELECT COUNT(*) FROM empleado_animal WHERE identificacion=%s", (identificacion,))
                ca = cur.fetchone()[0]
                cur.execute("SELECT COUNT(*) FROM empleado_maquinaria WHERE identificacion=%s", (identificacion,))
                cm = cur.fetchone()[0]
                cur.execute("SELECT COUNT(*) FROM empleado_cultivo WHERE identificacion=%s", (identificacion,))
                cc = cur.fetchone()[0]

                # delete relations
                cur.execute("DELETE FROM empleado_animal WHERE identificacion=%s", (identificacion,))
                cur.execute("DELETE FROM empleado_maquinaria WHERE identificacion=%s", (identificacion,))
                cur.execute("DELETE FROM empleado_cultivo WHERE identificacion=%s", (identificacion,))

                # delete empleado
                cur.execute("DELETE FROM empleado WHERE identificacion=%s", (identificacion,))

        return jsonify({'ok': True, 'deleted_relations': {'animal': ca, 'maquinaria': cm, 'cultivo': cc}})
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 400
    finally:
        conn.close()

# MAQUINARIA
@bp.route('/api/maquinaria', methods=['GET'])
def list_maquinaria():
    rows = query_dict("SELECT id, nombre, tipo, modelo, estado FROM maquinaria ORDER BY id;")
    return jsonify(rows)

@bp.route('/api/maquinaria', methods=['POST'])
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

@bp.route('/api/maquinaria/<int:id>', methods=['PUT'])
def update_maquinaria(id):
    data = request.json
    execute("UPDATE maquinaria SET nombre=%s, tipo=%s, modelo=%s, estado=%s WHERE id=%s",
            (data.get('nombre'), data.get('tipo'), data.get('modelo'), data.get('estado'), id))
    return jsonify({'ok': True})

@bp.route('/api/maquinaria/<int:id>', methods=['DELETE'])
def delete_maquinaria(id):
    try:
        execute("DELETE FROM maquinaria WHERE id=%s", (id,))
        return jsonify({'ok': True})
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 400

# ANIMAL
@bp.route('/api/animales', methods=['GET'])
def list_animales():
    rows = query_dict("SELECT id, nombre, especie, raza, sexo, estado FROM animal ORDER BY id;")
    return jsonify(rows)

@bp.route('/api/animales', methods=['POST'])
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

@bp.route('/api/animales/<int:id>', methods=['PUT'])
def update_animal(id):
    data = request.json
    execute("UPDATE animal SET nombre=%s, especie=%s, raza=%s, sexo=%s, estado=%s WHERE id=%s",
            (data.get('nombre'), data.get('especie'), data.get('raza'), data.get('sexo'), data.get('estado'), id))
    return jsonify({'ok': True})

@bp.route('/api/animales/<int:id>', methods=['DELETE'])
def delete_animal(id):
    try:
        execute("DELETE FROM animal WHERE id=%s", (id,))
        return jsonify({'ok': True})
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 400

# CULTIVO
@bp.route('/api/cultivos', methods=['GET'])
def list_cultivos():
    rows = query_dict("SELECT id, nombre, tipo, epoca, estado, fecha_siembra::text AS fecha_siembra FROM cultivo ORDER BY id;")
    return jsonify(rows)

@bp.route('/api/cultivos', methods=['POST'])
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

@bp.route('/api/cultivos/<int:id>', methods=['PUT'])
def update_cultivo(id):
    data = request.json
    execute("UPDATE cultivo SET nombre=%s, tipo=%s, epoca=%s, estado=%s, fecha_siembra=%s WHERE id=%s",
            (data.get('nombre'), data.get('tipo'), data.get('epoca'), data.get('estado'), data.get('fecha_siembra'), id))
    return jsonify({'ok': True})

@bp.route('/api/cultivos/<int:id>', methods=['DELETE'])
def delete_cultivo(id):
    try:
        execute("DELETE FROM cultivo WHERE id=%s", (id,))
        return jsonify({'ok': True})
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 400

# RECURSOS
@bp.route('/api/recursos', methods=['GET'])
def list_recursos():
    rows = query_dict("SELECT id, nombre, tipo_recurso, stock FROM recursos ORDER BY id;")
    return jsonify(rows)

@bp.route('/api/recursos', methods=['POST'])
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

@bp.route('/api/recursos/<int:id>', methods=['PUT'])
def update_recurso(id):
    data = request.json
    execute("UPDATE recursos SET nombre=%s, tipo_recurso=%s, stock=%s WHERE id=%s",
            (data.get('nombre'), data.get('tipo_recurso'), data.get('stock'), id))
    return jsonify({'ok': True})

@bp.route('/api/recursos/<int:id>', methods=['DELETE'])
def delete_recurso(id):
    try:
        execute("DELETE FROM recursos WHERE id=%s", (id,))
        return jsonify({'ok': True})
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 400

# PRODUCTO
@bp.route('/api/productos', methods=['GET'])
def list_productos():
    rows = query_dict("SELECT identificacion, nombre, tipo, precio FROM producto ORDER BY nombre;")
    return jsonify(rows)

@bp.route('/api/productos', methods=['POST'])
def create_producto():
    data = request.json
    sql = "INSERT INTO producto (identificacion, nombre, tipo, precio) VALUES (%s,%s,%s,%s)"
    try:
        execute(sql, (data.get('identificacion'), data.get('nombre'), data.get('tipo'), data.get('precio')))
        return jsonify({'ok': True}), 201
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 400

@bp.route('/api/productos/<identificacion>', methods=['PUT'])
def update_producto(identificacion):
    data = request.json
    execute("UPDATE producto SET nombre=%s, tipo=%s, precio=%s WHERE identificacion=%s",
            (data.get('nombre'), data.get('tipo'), data.get('precio'), identificacion))
    return jsonify({'ok': True})

@bp.route('/api/productos/<identificacion>', methods=['DELETE'])
def delete_producto(identificacion):
    try:
        execute("DELETE FROM producto WHERE identificacion=%s", (identificacion,))
        return jsonify({'ok': True})
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 400

# CLIENTE
@bp.route('/api/clientes', methods=['GET'])
def list_clientes():
    rows = query_dict("SELECT documento, nombre, direccion, telefono, email FROM cliente ORDER BY nombre;")
    return jsonify(rows)


@bp.route('/api/clientes/<documento>', methods=['GET'])
def get_cliente(documento):
    row = query_dict("SELECT documento, nombre, direccion, telefono, email FROM cliente WHERE documento=%s", (documento,), many=False)
    if not row:
        return jsonify({'ok': False, 'error': 'Cliente no encontrado'}), 404
    return jsonify(row)

@bp.route('/api/clientes', methods=['POST'])
def create_cliente():
    data = request.json
    sql = "INSERT INTO cliente (documento, nombre, direccion, telefono, email) VALUES (%s,%s,%s,%s,%s)"
    try:
        execute(sql, (data.get('documento'), data.get('nombre'), data.get('direccion'), data.get('telefono'), data.get('email')))
        return jsonify({'ok': True}), 201
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 400

@bp.route('/api/clientes/<documento>', methods=['PUT'])
def update_cliente(documento):
    data = request.json
    execute("UPDATE cliente SET nombre=%s, direccion=%s, telefono=%s, email=%s WHERE documento=%s",
            (data.get('nombre'), data.get('direccion'), data.get('telefono'), data.get('email'), documento))
    return jsonify({'ok': True})

@bp.route('/api/clientes/<documento>', methods=['DELETE'])
def delete_cliente(documento):
    try:
        execute("DELETE FROM cliente WHERE documento=%s", (documento,))
        return jsonify({'ok': True})
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 400

# VENTAS
@bp.route('/api/ventas', methods=['GET'])
def list_ventas():
    rows = query_dict("""
        SELECT v.id, v.documento_cliente, v.fecha::text AS fecha, v.total,
               c.nombre as cliente_nombre
        FROM venta v
        LEFT JOIN cliente c ON c.documento = v.documento_cliente
        ORDER BY v.fecha DESC
    """)
    return jsonify(rows)

@bp.route('/api/ventas/<int:id>', methods=['GET'])
def get_venta(id):
    venta = query_dict("SELECT id, documento_cliente, fecha::text AS fecha, total FROM venta WHERE id=%s", (id,), many=False)
    if not venta:
        return jsonify({'ok': False, 'error': 'Venta no encontrada'}), 404
    detalles = query_dict("SELECT identificacion_producto, cantidad, precio_unit FROM venta_detalle WHERE id_venta=%s", (id,))
    venta['detalles'] = detalles
    return jsonify(venta)

@bp.route('/api/ventas', methods=['POST'])
def create_venta():
    data = request.json
    items = data.get('items', [])
    if not items:
        return jsonify({'ok': False, 'error': 'Se requieren items'}), 400

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

@bp.route('/api/ventas/<int:id>', methods=['DELETE'])
def delete_venta(id):
    try:
        execute("DELETE FROM venta WHERE id=%s", (id,))
        return jsonify({'ok': True})
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 400

# CONSUMOS
@bp.route('/api/consumo/animal', methods=['GET'])
def list_consumo_animal():
    rows = query_dict("SELECT id, id_animal, id_recurso, destino, cantidad, observacion, fecha::text AS fecha FROM consumo_animal ORDER BY fecha DESC;")
    return jsonify(rows)

@bp.route('/api/consumo/animal', methods=['POST'])
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

@bp.route('/api/consumo/cultivo', methods=['GET'])
def list_consumo_cultivo():
    rows = query_dict("SELECT id, id_cultivo, id_recurso, destino, cantidad, observacion, fecha::text AS fecha FROM consumo_cultivo ORDER BY fecha DESC;")
    return jsonify(rows)

@bp.route('/api/consumo/cultivo', methods=['POST'])
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

# Relaciones M:N (empleado_maquinaria, empleado_animal, empleado_cultivo)
@bp.route('/api/empleado_maquinaria', methods=['GET'])
def list_empleado_maquinaria():
    rows = query_dict("SELECT identificacion, id_maquinaria, asignacion_fecha::text AS asignacion_fecha FROM empleado_maquinaria ORDER BY asignacion_fecha DESC;")
    return jsonify(rows)

@bp.route('/api/empleado_maquinaria', methods=['POST'])
def create_empleado_maquinaria():
    data = request.json
    sql = "INSERT INTO empleado_maquinaria (identificacion, id_maquinaria, asignacion_fecha) VALUES (%s,%s,%s)"
    try:
        execute(sql, (data.get('identificacion'), data.get('id_maquinaria'), data.get('asignacion_fecha')))
        return jsonify({'ok': True}), 201
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 400

@bp.route('/api/empleado_maquinaria', methods=['DELETE'])
def delete_empleado_maquinaria():
    data = request.json or {}
    try:
        execute("DELETE FROM empleado_maquinaria WHERE identificacion=%s AND id_maquinaria=%s", (data.get('identificacion'), data.get('id_maquinaria')))
        return jsonify({'ok': True})
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 400

@bp.route('/api/empleado_animal', methods=['GET'])
def list_empleado_animal():
    rows = query_dict("SELECT identificacion, id_animal, asignacion_fecha::text AS asignacion_fecha FROM empleado_animal ORDER BY asignacion_fecha DESC;")
    return jsonify(rows)

@bp.route('/api/empleado_animal', methods=['POST'])
def create_empleado_animal():
    data = request.json
    sql = "INSERT INTO empleado_animal (identificacion, id_animal, asignacion_fecha) VALUES (%s,%s,%s)"
    try:
        execute(sql, (data.get('identificacion'), data.get('id_animal'), data.get('asignacion_fecha')))
        return jsonify({'ok': True}), 201
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 400

@bp.route('/api/empleado_animal', methods=['DELETE'])
def delete_empleado_animal():
    data = request.json or {}
    try:
        execute("DELETE FROM empleado_animal WHERE identificacion=%s AND id_animal=%s", (data.get('identificacion'), data.get('id_animal')))
        return jsonify({'ok': True})
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 400

@bp.route('/api/empleado_cultivo', methods=['GET'])
def list_empleado_cultivo():
    rows = query_dict("SELECT identificacion, id_cultivo, asignacion_fecha::text AS asignacion_fecha FROM empleado_cultivo ORDER BY asignacion_fecha DESC;")
    return jsonify(rows)

@bp.route('/api/empleado_cultivo', methods=['POST'])
def create_empleado_cultivo():
    data = request.json
    sql = "INSERT INTO empleado_cultivo (identificacion, id_cultivo, asignacion_fecha) VALUES (%s,%s,%s)"
    try:
        execute(sql, (data.get('identificacion'), data.get('id_cultivo'), data.get('asignacion_fecha')))
        return jsonify({'ok': True}), 201
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 400

@bp.route('/api/empleado_cultivo', methods=['DELETE'])
def delete_empleado_cultivo():
    data = request.json or {}
    try:
        execute("DELETE FROM empleado_cultivo WHERE identificacion=%s AND id_cultivo=%s", (data.get('identificacion'), data.get('id_cultivo')))
        return jsonify({'ok': True})
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 400

# Genera producto animal
@bp.route('/api/genera_producto_animal', methods=['GET'])
def list_genera_producto_animal():
    rows = query_dict("SELECT id, id_animal, identificacion_producto, cantidad, fecha::text AS fecha FROM genera_producto_animal ORDER BY fecha DESC;")
    return jsonify(rows)

@bp.route('/api/genera_producto_animal', methods=['POST'])
def create_genera_producto_animal():
    data = request.json
    sql = "INSERT INTO genera_producto_animal (id_animal, identificacion_producto, cantidad, fecha) VALUES (%s,%s,%s,%s) RETURNING id;"
    conn = get_connection()
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(sql, (data.get('id_animal'), data.get('identificacion_producto'), data.get('cantidad'), data.get('fecha')))
                new_id = cur.fetchone()[0]
        return jsonify({'ok': True, 'id': new_id}), 201
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 400
    finally:
        conn.close()

@bp.route('/api/genera_producto_animal/<int:id>', methods=['DELETE'])
def delete_genera_producto_animal(id):
    try:
        execute("DELETE FROM genera_producto_animal WHERE id=%s", (id,))
        return jsonify({'ok': True})
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 400

# Genera producto cultivo
@bp.route('/api/genera_producto_cultivo', methods=['GET'])
def list_genera_producto_cultivo():
    rows = query_dict("SELECT id, id_cultivo, identificacion_producto, cantidad, fecha::text AS fecha FROM genera_producto_cultivo ORDER BY fecha DESC;")
    return jsonify(rows)

@bp.route('/api/genera_producto_cultivo', methods=['POST'])
def create_genera_producto_cultivo():
    data = request.json
    sql = "INSERT INTO genera_producto_cultivo (id_cultivo, identificacion_producto, cantidad, fecha) VALUES (%s,%s,%s,%s) RETURNING id;"
    conn = get_connection()
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(sql, (data.get('id_cultivo'), data.get('identificacion_producto'), data.get('cantidad'), data.get('fecha')))
                new_id = cur.fetchone()[0]
        return jsonify({'ok': True, 'id': new_id}), 201
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 400
    finally:
        conn.close()

@bp.route('/api/genera_producto_cultivo/<int:id>', methods=['DELETE'])
def delete_genera_producto_cultivo(id):
    try:
        execute("DELETE FROM genera_producto_cultivo WHERE id=%s", (id,))
        return jsonify({'ok': True})
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 400
