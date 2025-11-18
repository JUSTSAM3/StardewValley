import urllib.request, urllib.error, json

base = 'http://127.0.0.1:5000'

def request(method, path, data=None):
    url = base + path
    data_bytes = None
    headers = {}
    if data is not None:
        data_bytes = json.dumps(data).encode('utf-8')
        headers['Content-Type'] = 'application/json'
    req = urllib.request.Request(url, data=data_bytes, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            text = resp.read().decode('utf-8')
            try:
                payload = json.loads(text) if text else None
            except Exception:
                payload = text
            return resp.status, payload
    except urllib.error.HTTPError as e:
        try:
            text = e.read().decode('utf-8')
            payload = json.loads(text) if text else None
        except Exception:
            payload = None
        return e.code, payload
    except Exception as e:
        print('REQUEST ERROR', method, path, e)
        return None, None

print('--- EMPLEADOS CRUD ---')
# Create
status, payload = request('POST', '/api/empleados', {
    'identificacion': '999',
    'nombre': 'Test User',
    'cargo': 'Tester',
    'fecha_ingreso': '2025-11-17',
    'sueldo': '1000.00'
})
print('CREATE', status, payload)

# Get all and find
status, payload = request('GET', '/api/empleados')
found = [p for p in (payload or []) if p.get('identificacion') == '999']
print('FOUND AFTER CREATE', status, found)

# Update
status, payload = request('PUT', '/api/empleados/999', {
    'nombre': 'Test User Updated',
    'cargo': 'Tester2',
    'fecha_ingreso': '2025-11-18',
    'sueldo': '1200.00'
})
print('UPDATE', status, payload)

# Verify update
status, payload = request('GET', '/api/empleados')
found = [p for p in (payload or []) if p.get('identificacion') == '999']
print('FOUND AFTER UPDATE', status, found)

# Delete
status, payload = request('DELETE', '/api/empleados/999')
print('DELETE', status, payload)

# Verify deletion
status, payload = request('GET', '/api/empleados')
found = [p for p in (payload or []) if p.get('identificacion') == '999']
print('FOUND AFTER DELETE', status, found)

print('\n--- MAQUINARIA CRUD ---')
# Create maquinaria (estado must be one of DISPONIBLE, EN_USO, MANTENIMIENTO)
status, payload = request('POST', '/api/maquinaria', {
    'nombre': 'Tractor Test',
    'tipo': 'Tractor',
    'modelo': 'TX-1',
    'estado': 'DISPONIBLE'
})
print('CREATE MAQ', status, payload)
maq_id = None
if isinstance(payload, dict) and 'id' in payload:
    maq_id = payload['id']

# Verify create
status, payload = request('GET', '/api/maquinaria')
found = [p for p in (payload or []) if p.get('id') == maq_id]
print('FOUND MAQ', status, found)

# Update maquinaria
if maq_id is not None:
    status, payload = request('PUT', f'/api/maquinaria/{maq_id}', {
        'nombre': 'Tractor Updated',
        'tipo': 'Tractor',
        'modelo': 'TX-1U',
        'estado': 'MANTENIMIENTO'
    })
    print('UPDATE MAQ', status, payload)

    # Delete
    status, payload = request('DELETE', f'/api/maquinaria/{maq_id}')
    print('DELETE MAQ', status, payload)

    # Verify deletion
    status, payload = request('GET', '/api/maquinaria')
    found = [p for p in (payload or []) if p.get('id') == maq_id]
    print('FOUND AFTER DELETE MAQ', status, found)
else:
    print('MAQ CREATE did not return id; skipping update/delete')

print('\n--- PRODUCTOS CRUD ---')
# create product
status, payload = request('POST', '/api/productos', {
    'identificacion': 'TSTP1',
    'nombre': 'Producto Test',
    'tipo': 'Test',
    'precio': '123.45'
})
print('CREATE PRODUCT', status, payload)

# verify
status, payload = request('GET', '/api/productos')
found = [p for p in (payload or []) if str(p.get('identificacion')) == 'TSTP1']
print('FOUND PRODUCT', status, found)

# update
status, payload = request('PUT', '/api/productos/TSTP1', {
    'nombre': 'Producto Test U', 'tipo': 'TestU', 'precio': '200.00'
})
print('UPDATE PRODUCT', status, payload)

# delete
status, payload = request('DELETE', '/api/productos/TSTP1')
print('DELETE PRODUCT', status, payload)

print('\n--- CLIENTES CRUD ---')
status, payload = request('POST', '/api/clientes', {
    'documento': 'DOCTST1', 'nombre': 'Cliente Test', 'direccion': 'Calle 1', 'telefono': '3001234', 'email': 'test@example.com'
})
print('CREATE CLIENT', status, payload)

status, payload = request('GET', '/api/clientes')
found = [c for c in (payload or []) if c.get('documento') == 'DOCTST1']
print('FOUND CLIENT', status, found)

status, payload = request('PUT', '/api/clientes/DOCTST1', {'nombre':'Cliente Upd','direccion':'Calle 2','telefono':'3000000','email':'upd@example.com'})
print('UPDATE CLIENT', status, payload)

status, payload = request('DELETE', '/api/clientes/DOCTST1')
print('DELETE CLIENT', status, payload)

print('\n--- RECURSOS CRUD ---')
status, payload = request('POST', '/api/recursos', {'nombre':'Recurso Test','tipo_recurso':'Insumo','stock': 10})
print('CREATE RECURSO', status, payload)
recurso_id = None
if isinstance(payload, dict) and 'id' in payload:
    recurso_id = payload['id']

status, payload = request('GET', '/api/recursos')
found = [r for r in (payload or []) if recurso_id and r.get('id') == recurso_id]
print('FOUND RECURSO', status, found)

if recurso_id:
    status, payload = request('PUT', f'/api/recursos/{recurso_id}', {'nombre':'Recurso Test Up','tipo_recurso':'Insumo','stock':5})
    print('UPDATE RECURSO', status, payload)
    status, payload = request('DELETE', f'/api/recursos/{recurso_id}')
    print('DELETE RECURSO', status, payload)
else:
    print('RECURSO CREATE did not return id; skipping update/delete')

print('\n--- VENTAS (create) ---')
# ensure a product and client exist for the sale
status, payload = request('POST', '/api/productos', {'identificacion':'TSTP2','nombre':'Producto Venta','tipo':'VT','precio':'50.00'})
print('CREATE PRODUCT FOR SALE', status)
status, payload = request('POST', '/api/clientes', {'documento':'DOCSALE1','nombre':'Cliente Venta','direccion':'X','telefono':'123','email':'sale@example.com'})
print('CREATE CLIENT FOR SALE', status)

# get precio from product list
status, payload = request('GET', '/api/productos')
prod = None
for p in (payload or []):
    if str(p.get('identificacion')) == 'TSTP2': prod = p; break

if not prod:
    print('Could not find product for sale; skipping sale test')
else:
    items = [{'identificacion_producto': prod['identificacion'], 'cantidad': 2, 'precio_unit': prod['precio']}]
    status, payload = request('POST', '/api/ventas', {'documento_cliente': 'DOCSALE1', 'items': items})
    print('CREATE VENTA', status, payload)
    venta_id = payload.get('id') if isinstance(payload, dict) else None
    if venta_id:
        status, payload = request('GET', f'/api/ventas/{venta_id}')
        print('GET VENTA', status, payload)
        status, payload = request('DELETE', f'/api/ventas/{venta_id}')
        print('DELETE VENTA', status, payload)

    # cleanup product and client
    request('DELETE', '/api/productos/TSTP2')
    request('DELETE', '/api/clientes/DOCSALE1')

    print('\n--- CONSUMOS CRUD ---')
    # create recurso for consumo
    status, payload = request('POST', '/api/recursos', {'nombre':'RecursoCons','tipo_recurso':'Insumo','stock':100})
    print('CREATE RECURSO FOR CONSUMO', status, payload)
    recurso_id = payload.get('id') if isinstance(payload, dict) else None

    # create animal for consumo
    status, payload = request('POST', '/api/animales', {'nombre':'AnimalCons','especie':'Vaca','raza':'Holstein','sexo':'HEMBRA','estado':'VIVO'})
    print('CREATE ANIMAL FOR CONSUMO', status, payload)
    animal_id = payload.get('id') if isinstance(payload, dict) else None

    if recurso_id and animal_id:
        status, payload = request('POST', '/api/consumo/animal', {'id_animal': animal_id, 'id_recurso': recurso_id, 'destino': 'Alimentacion', 'cantidad': 5, 'observacion':'Test consumo animal', 'fecha':'2025-11-17'})
        print('CREATE CONSUMO ANIMAL', status, payload)
        status, payload = request('GET', '/api/consumo/animal')
        found = [c for c in (payload or []) if c.get('id_animal') == animal_id and c.get('id_recurso') == recurso_id]
        print('FOUND CONSUMO ANIMAL', status, found)
    else:
        print('Skipping consumo animal test due missing recurso/animal ids')

    # create cultivo for consumo
    status, payload = request('POST', '/api/cultivos', {'nombre':'CultivoCons','tipo':'Maiz','epoca':'Primavera','estado':'SEMILLA','fecha_siembra':'2025-11-01'})
    print('CREATE CULTIVO FOR CONSUMO', status, payload)
    cultivo_id = payload.get('id') if isinstance(payload, dict) else None

    if recurso_id and cultivo_id:
        status, payload = request('POST', '/api/consumo/cultivo', {'id_cultivo': cultivo_id, 'id_recurso': recurso_id, 'destino': 'Fertilizacion', 'cantidad': 2.5, 'observacion':'Test consumo cultivo', 'fecha':'2025-11-17'})
        print('CREATE CONSUMO CULTIVO', status, payload)
        status, payload = request('GET', '/api/consumo/cultivo')
        found = [c for c in (payload or []) if c.get('id_cultivo') == cultivo_id and c.get('id_recurso') == recurso_id]
        print('FOUND CONSUMO CULTIVO', status, found)
    else:
        print('Skipping consumo cultivo test due missing recurso/cultivo ids')

    print('\n--- RELACIONES M:N CRUD ---')
    # create empleado and maquinaria for relation
    status, payload = request('POST', '/api/empleados', {'identificacion':'EMPMN1','nombre':'Empleado MN','cargo':'Operario','fecha_ingreso':'2025-11-17','sueldo':'900.00'})
    print('CREATE EMPLEADO MN', status, payload)
    status, payload = request('POST', '/api/maquinaria', {'nombre':'EquipMN','tipo':'Cosechadora','modelo':'C-1','estado':'DISPONIBLE'})
    print('CREATE MAQUINARIA MN', status, payload)
    maq_id = payload.get('id') if isinstance(payload, dict) else None

    if maq_id:
        status, payload = request('POST', '/api/empleado_maquinaria', {'identificacion':'EMPMN1','id_maquinaria': maq_id,'asignacion_fecha':'2025-11-17'})
        print('ASSIGN EMPLEADO->MAQ', status, payload)
        status, payload = request('GET', '/api/empleado_maquinaria')
        found = [r for r in (payload or []) if r.get('identificacion') == 'EMPMN1' and int(r.get('id_maquinaria')) == int(maq_id)]
        print('FOUND EMPLEADO_MAQUINARIA', status, found)
        # delete relation
        status, payload = request('DELETE', '/api/empleado_maquinaria', {'identificacion':'EMPMN1','id_maquinaria': maq_id})
        print('DELETE EMPLEADO_MAQUINARIA', status, payload)
    else:
        print('Skipping empleado_maquinaria tests; maquinaría id missing')

    # empleado_animal relation
    status, payload = request('POST', '/api/animales', {'nombre':'AnimRel','especie':'Oveja','raza':'Merino','sexo':'MACHO','estado':'VIVO'})
    anim_rel_id = payload.get('id') if isinstance(payload, dict) else None
    print('CREATE ANIMAL FOR MN', anim_rel_id)
    if anim_rel_id:
        status, payload = request('POST', '/api/empleado_animal', {'identificacion':'EMPMN1','id_animal': anim_rel_id,'asignacion_fecha':'2025-11-17'})
        print('ASSIGN EMPLEADO->ANIMAL', status, payload)
        status, payload = request('GET', '/api/empleado_animal')
        found = [r for r in (payload or []) if r.get('identificacion') == 'EMPMN1' and int(r.get('id_animal')) == int(anim_rel_id)]
        print('FOUND EMPLEADO_ANIMAL', status, found)
        status, payload = request('DELETE', '/api/empleado_animal', {'identificacion':'EMPMN1','id_animal': anim_rel_id})
        print('DELETE EMPLEADO_ANIMAL', status, payload)
    else:
        print('Skipping empleado_animal tests; animal id missing')

    # empleado_cultivo relation
    if cultivo_id:
        status, payload = request('POST', '/api/empleado_cultivo', {'identificacion':'EMPMN1','id_cultivo': cultivo_id,'asignacion_fecha':'2025-11-17'})
        print('ASSIGN EMPLEADO->CULTIVO', status, payload)
        status, payload = request('GET', '/api/empleado_cultivo')
        found = [r for r in (payload or []) if r.get('identificacion') == 'EMPMN1' and int(r.get('id_cultivo')) == int(cultivo_id)]
        print('FOUND EMPLEADO_CULTIVO', status, found)
        status, payload = request('DELETE', '/api/empleado_cultivo', {'identificacion':'EMPMN1','id_cultivo': cultivo_id})
        print('DELETE EMPLEADO_CULTIVO', status, payload)
    else:
        print('Skipping empleado_cultivo tests; cultivo id missing')

    # cleanup created helper records
    request('DELETE', f'/api/maquinaria/{maq_id}') if maq_id else None
    request('DELETE', f'/api/animales/{anim_rel_id}') if anim_rel_id else None
    request('DELETE', f'/api/animales/{animal_id}') if animal_id else None
    request('DELETE', f'/api/cultivos/{cultivo_id}') if cultivo_id else None
    request('DELETE', f'/api/recursos/{recurso_id}') if recurso_id else None
    request('DELETE', '/api/empleados/EMPMN1')
