import psycopg2
from database import get_connection

def insert_initial_data():
    """
    Inserta los datos iniciales completos en la base de datos Stardew
    """
    try:
        conn = get_connection()
        cur = conn.cursor()
        
        print("[INFO] Iniciando inserción de datos...")
        
        # =========================================
        # EMPLEADOS
        # =========================================
        print("→ Insertando empleados...")
        empleados = [
            ('100', 'Juan Pérez', 'Administrador', '2020-01-15', 2500000),
            ('101', 'Ana Gómez', 'Veterinaria', '2021-02-10', 2800000),
            ('102', 'Luis Torres', 'Agrónomo', '2019-09-12', 2600000),
            ('103', 'Sofía Morales', 'Operaria', '2022-03-20', 1800000)
        ]
        cur.executemany(
            "INSERT INTO empleado VALUES (%s, %s, %s, %s, %s) ON CONFLICT DO NOTHING",
            empleados
        )
        
        # =========================================
        # MAQUINARIA
        # =========================================
        print("→ Insertando maquinaria...")
        maquinaria = [
            ('Tractor JD 5080', 'Tractor', 'JD-5080', 'DISPONIBLE'),
            ('Arado Profundo', 'Arado', 'AP-12', 'EN_USO'),
            ('Cosechadora Serie X', 'Cosechadora', 'CX-50', 'MANTENIMIENTO'),
            ('Tractor Case IH', 'Tractor', 'C-90', 'DISPONIBLE')
        ]
        cur.executemany(
            "INSERT INTO maquinaria (nombre, tipo, modelo, estado) VALUES (%s, %s, %s, %s) ON CONFLICT DO NOTHING",
            maquinaria
        )
        
        # =========================================
        # EMPLEADO - MAQUINARIA (M:N)
        # =========================================
        print("→ Insertando relación empleado-maquinaria...")
        empleado_maquinaria = [
            ('100', 1, '2024-01-10'),
            ('101', 2, '2024-01-12'),
            ('102', 3, '2024-02-01'),
            ('103', 1, '2024-02-15')
        ]
        cur.executemany(
            "INSERT INTO empleado_maquinaria VALUES (%s, %s, %s) ON CONFLICT DO NOTHING",
            empleado_maquinaria
        )
        
        # =========================================
        # ANIMALES
        # =========================================
        print("→ Insertando animales...")
        animales = [
            ('Lola', 'Vaca', 'Holstein', 'HEMBRA', 'VIVO'),
            ('Braulio', 'Cerdo', 'Landrace', 'MACHO', 'VIVO'),
            ('Nieve', 'Gallina', 'Leghorn', 'HEMBRA', 'VIVO'),
            ('ToroMax', 'Toro', 'Brahman', 'MACHO', 'VIVO'),
            ('Copito', 'Cabra', 'Saanen', 'HEMBRA', 'MUERTO')
        ]
        cur.executemany(
            "INSERT INTO animal (nombre, especie, raza, sexo, estado) VALUES (%s, %s, %s, %s, %s) ON CONFLICT DO NOTHING",
            animales
        )
        
        # =========================================
        # EMPLEADO - ANIMAL (M:N)
        # =========================================
        print("→ Insertando relación empleado-animal...")
        empleado_animal = [
            ('101', 1, '2024-01-02'),
            ('101', 2, '2024-01-03'),
            ('103', 3, '2024-02-10'),
            ('100', 4, '2024-03-01')
        ]
        cur.executemany(
            "INSERT INTO empleado_animal VALUES (%s, %s, %s) ON CONFLICT DO NOTHING",
            empleado_animal
        )
        
        # =========================================
        # CULTIVOS
        # =========================================
        print("→ Insertando cultivos...")
        cultivos = [
            ('Maíz Amarillo', 'Grano', 'Verano', 'CRECIMIENTO', '2024-03-15'),
            ('Papa Criolla', 'Tubérculo', 'Otoño', 'SEMILLA', '2024-02-25'),
            ('Tomate Cherry', 'Hortaliza', 'Verano', 'CRECIMIENTO', '2024-01-10'),
            ('Trigo Duro', 'Grano', 'Primavera', 'COSECHADO', '2023-12-20')
        ]
        cur.executemany(
            "INSERT INTO cultivo (nombre, tipo, epoca, estado, fecha_siembra) VALUES (%s, %s, %s, %s, %s) ON CONFLICT DO NOTHING",
            cultivos
        )
        
        # =========================================
        # EMPLEADO - CULTIVO (M:N)
        # =========================================
        print("→ Insertando relación empleado-cultivo...")
        empleado_cultivo = [
            ('102', 1, '2024-02-01'),
            ('102', 2, '2024-02-20'),
            ('103', 3, '2024-01-15'),
            ('100', 4, '2023-12-21')
        ]
        cur.executemany(
            "INSERT INTO empleado_cultivo VALUES (%s, %s, %s) ON CONFLICT DO NOTHING",
            empleado_cultivo
        )
        
        # =========================================
        # RECURSOS
        # =========================================
        print("→ Insertando recursos...")
        recursos = [
            ('Alimento Bovino', 'Comida', 55),
            ('Fertilizante Orgánico', 'Fertilizante', 12),
            ('Alimento Porcino', 'Comida', 22),
            ('Insecticida Ultra', 'Químico', 8)
        ]
        cur.executemany(
            "INSERT INTO recursos (nombre, tipo_recurso, stock) VALUES (%s, %s, %s) ON CONFLICT DO NOTHING",
            recursos
        )
        
        # =========================================
        # CONSUMO DE RECURSOS - ANIMALES
        # =========================================
        print("→ Insertando consumo de recursos por animales...")
        consumo_animal = [
            (1, 1, 'Alimentación', 5, 'Consumo diario', '2024-03-01'),
            (2, 3, 'Alimentación', 3, 'Pendiente aumentar ración', '2024-03-02'),
            (4, 1, 'Mantenimiento', 4, 'Preparación para reproducción', '2024-03-04')
        ]
        cur.executemany(
            "INSERT INTO consumo_animal (id_animal, id_recurso, destino, cantidad, observacion, fecha) VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING",
            consumo_animal
        )
        
        # =========================================
        # CONSUMO DE RECURSOS - CULTIVOS
        # =========================================
        print("→ Insertando consumo de recursos por cultivos...")
        consumo_cultivo = [
            (1, 2, 'Fertilización', 10, 'Inicio de temporada', '2024-02-25'),
            (3, 4, 'Control de plagas', 2, 'Aplicación moderada', '2024-03-03'),
            (2, 2, 'Preparación de suelo', 4, 'Primera aplicación', '2024-03-05')
        ]
        cur.executemany(
            "INSERT INTO consumo_cultivo (id_cultivo, id_recurso, destino, cantidad, observacion, fecha) VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING",
            consumo_cultivo
        )
        
        # =========================================
        # PRODUCTOS
        # =========================================
        print("→ Insertando productos...")
        productos = [
            ('PR01', 'Leche Entera', 'Lácteo', 3000),
            ('PR02', 'Carne de Cerdo', 'Cárnico', 18000),
            ('PR03', 'Huevo Blanco', 'Avícola', 500),
            ('PR04', 'Queso Cabra', 'Lácteo', 8500),
            ('PR05', 'Harina de Trigo', 'Grano Procesado', 3200)
        ]
        cur.executemany(
            "INSERT INTO producto VALUES (%s, %s, %s, %s) ON CONFLICT DO NOTHING",
            productos
        )
        
        # =========================================
        # PRODUCTOS GENERADOS POR ANIMALES
        # =========================================
        print("→ Insertando productos generados por animales...")
        genera_producto_animal = [
            (1, 'PR01', 15, '2024-03-01'),
            (3, 'PR03', 24, '2024-03-02'),
            (5, 'PR04', 3, '2024-03-05')
        ]
        cur.executemany(
            "INSERT INTO genera_producto_animal (id_animal, identificacion_producto, cantidad, fecha) VALUES (%s, %s, %s, %s) ON CONFLICT DO NOTHING",
            genera_producto_animal
        )
        
        # =========================================
        # PRODUCTOS GENERADOS POR CULTIVOS
        # =========================================
        print("→ Insertando productos generados por cultivos...")
        genera_producto_cultivo = [
            (1, 'PR05', 40, '2024-03-01'),
            (4, 'PR05', 70, '2024-01-10')
        ]
        cur.executemany(
            "INSERT INTO genera_producto_cultivo (id_cultivo, identificacion_producto, cantidad, fecha) VALUES (%s, %s, %s, %s) ON CONFLICT DO NOTHING",
            genera_producto_cultivo
        )
        
        # =========================================
        # CLIENTES
        # =========================================
        print("→ Insertando clientes...")
        clientes = [
            ('CC01', 'Carlos Soto', 'Calle 10 #33-22', '3105557777', 'carlos@mail.com'),
            ('CC02', 'María López', 'Cra 50 #10-11', '3012228899', 'maria@mail.com'),
            ('CC03', 'Distribuidora Agrofoods', 'Zona Industrial Bodega 22', '3149902233', 'ventas@agrofoods.com')
        ]
        cur.executemany(
            "INSERT INTO cliente VALUES (%s, %s, %s, %s, %s) ON CONFLICT DO NOTHING",
            clientes
        )
        
        # =========================================
        # VENTAS
        # =========================================
        print("→ Insertando ventas...")
        ventas = [
            ('CC01', 30000, '2024-03-10'),
            ('CC02', 45000, '2024-03-12'),
            ('CC03', 120000, '2024-03-15')
        ]
        cur.executemany(
            "INSERT INTO venta (documento_cliente, total, fecha) VALUES (%s, %s, %s) ON CONFLICT DO NOTHING",
            ventas
        )
        
        # =========================================
        # DETALLE DE VENTA
        # =========================================
        print("→ Insertando detalles de venta...")
        venta_detalles = [
            (1, 'PR01', 10, 3000),
            (2, 'PR02', 2, 18000),
            (2, 'PR03', 30, 500),
            (3, 'PR05', 25, 3200),
            (3, 'PR01', 15, 3000)
        ]
        cur.executemany(
            "INSERT INTO venta_detalle (id_venta, identificacion_producto, cantidad, precio_unit) VALUES (%s, %s, %s, %s) ON CONFLICT DO NOTHING",
            venta_detalles
        )
        
        # Confirmar transacción
        conn.commit()
        print("\n[OK] ✓ Todos los datos fueron insertados exitosamente!")
        print("     Total de tablas pobladas: 16")
        
        cur.close()
        conn.close()
        
    except Exception as e:
        print(f"\n[ERROR] ✗ No se pudieron insertar los datos: {e}")
        if conn:
            conn.rollback()


if __name__ == "__main__":
    insert_initial_data()