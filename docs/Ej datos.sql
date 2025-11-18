----------------------------------------------------------
-- 1. EMPLEADOS
----------------------------------------------------------
INSERT INTO empleado (identificacion, nombre, cargo, fecha_ingreso, sueldo) VALUES
('E001', 'Juan Pérez',      'Veterinario',  '2021-01-10', 2500000),
('E002', 'Ana Gómez',       'Agrónomo',     '2020-03-15', 2300000),
('E003', 'Luis Martínez',   'Auxiliar',     '2023-07-01', 1500000),
('E004', 'María López',     'Administrador','2019-11-20', 3000000);  -- este no tiene maquinaria (para la consulta 14)


----------------------------------------------------------
-- 2. MAQUINARIA
----------------------------------------------------------
INSERT INTO maquinaria (id, nombre, tipo, modelo, estado) VALUES
(1, 'Tractor John Deere', 'TRACTOR',    'JD-5090', 'DISPONIBLE'),
(2, 'Fumigadora 1',       'FUMIGADORA', 'FUM-01',  'EN_USO'),
(3, 'Arado Principal',    'ARADO',      'AR-100',  'MANTENIMIENTO');


----------------------------------------------------------
-- 3. ANIMALES
----------------------------------------------------------
INSERT INTO animal (id, nombre, especie, raza, sexo, estado) VALUES
(1, 'Vaca 01',    'VACA',    'Holstein',  'HEMBRA', 'VIVO'),
(2, 'Vaca 02',    'VACA',    'Holstein',  'HEMBRA', 'VIVO'),
(3, 'Toro 01',    'VACA',    'Holstein',  'MACHO',  'VIVO'),
(4, 'Cerdo 01',   'CERDO',   NULL,        'MACHO',  'VIVO'),
(5, 'Gallina 01', 'GALLINA', NULL,        'HEMBRA', 'VENDIDO'),
(6, 'Caballo 01', 'CABALLO', NULL,        'MACHO',  'VIVO');   -- sin producción (para la consulta 15)


----------------------------------------------------------
-- 4. CULTIVOS
----------------------------------------------------------
INSERT INTO cultivo (id, nombre, tipo, epoca, estado, fecha_siembra) VALUES
(1, 'Maíz Lote 1',        'CEREAL',    'VERANO',    'COSECHADO', '2024-08-01'),
(2, 'Tomate Invernadero', 'HORTALIZA', 'INVIERNO',  'CRECIMIENTO','2024-09-15'),
(3, 'Lechuga Parcela',    'HORTALIZA', 'PRIMAVERA', 'COSECHADO', '2024-03-01');


----------------------------------------------------------
-- 5. RECURSOS
----------------------------------------------------------
INSERT INTO recursos (id, nombre, tipo_recurso, stock) VALUES
(1, 'Concentrado Bovino', 'Ganadero', 150.0),
(2, 'Agua de Riego',      'Agrícola', 500.0),
(3, 'Fertilizante NPK',   'Agrícola', 15.0),   -- stock bajo (<20) para alerta (consulta 19)
(4, 'Vacuna Aftosa',      'Veterinario', 5.0); -- stock bajo


----------------------------------------------------------
-- 6. PRODUCTOS
----------------------------------------------------------
INSERT INTO producto (identificacion, nombre, tipo, precio) VALUES
('P001', 'Leche Entera',    'Animal',  2500.00),
('P002', 'Huevos',          'Animal',  500.00),
('P003', 'Maíz en grano',   'Vegetal', 1500.00),
('P004', 'Tomate fresco',   'Vegetal', 2000.00);


----------------------------------------------------------
-- 7. CLIENTES
----------------------------------------------------------
INSERT INTO cliente (documento, nombre, direccion, telefono, email) VALUES
('C001', 'Restaurante El Trigal', 'Calle 1 #2-3',    '3001112233', 'trigal@example.com'),
('C002', 'Supermercado Central',  'Av 10 #20-30',    '3002223344', 'central@example.com'),
('C003', 'Cliente Particular',    'Calle 50 #10-20', '3003334455', 'particular@example.com');


----------------------------------------------------------
-- 8. VENTAS (CABECERA)
--   incluye fechas en 2025 para probar el filtro por rango (consulta 18)
----------------------------------------------------------
INSERT INTO venta (id, documento_cliente, fecha, total) VALUES
(1, 'C001', '2025-01-10 10:30:00', 150000.00),
(2, 'C002', '2025-06-05 15:45:00', 212000.00),
(3, 'C003', '2024-12-20 09:15:00', 20000.00);  -- fuera del rango 2025 en la consulta 18


----------------------------------------------------------
-- 9. TABLAS M:N: empleado_maquinaria / empleado_animal / empleado_cultivo
----------------------------------------------------------
-- Empleado - Maquinaria (M:N)
INSERT INTO empleado_maquinaria (identificacion, id_maquinaria, asignacion_fecha) VALUES
('E001', 1, '2024-01-01'),
('E002', 2, '2024-02-01'),
('E002', 3, '2024-03-01'),
('E003', 2, '2024-04-01');
-- E004 queda sin maquinaria para la consulta 14


-- Empleado - Animal (M:N)
INSERT INTO empleado_animal (identificacion, id_animal, asignacion_fecha) VALUES
('E001', 1, '2024-01-10'),
('E001', 2, '2024-01-11'),
('E002', 4, '2024-02-05');


-- Empleado - Cultivo (M:N)
INSERT INTO empleado_cultivo (identificacion, id_cultivo, asignacion_fecha) VALUES
('E002', 2, '2024-02-10'),  -- HORTALIZA
('E002', 3, '2024-03-10'),  -- HORTALIZA
('E003', 1, '2024-04-10');  -- CEREAL


----------------------------------------------------------
-- 10. CONSUMO DE RECURSOS – ANIMALES
--     Diseñado para que algunos animales superen 100 de consumo (consulta 17)
----------------------------------------------------------
INSERT INTO consumo_animal (id, id_animal, id_recurso, destino, cantidad, observacion, fecha) VALUES
(1, 1, 1, 'Alimentación', 60.0,  NULL, '2024-05-01'),
(2, 1, 1, 'Alimentación', 50.0,  NULL, '2024-05-02'),
(3, 1, 2, 'Hidratación',  40.0,  NULL, '2024-05-03'), -- total animal 1 = 150
(4, 2, 1, 'Alimentación', 30.0,  NULL, '2024-05-01'),
(5, 4, 1, 'Alimentación', 25.0,  NULL, '2024-05-01');


----------------------------------------------------------
-- 11. CONSUMO DE RECURSOS – CULTIVOS
----------------------------------------------------------
INSERT INTO consumo_cultivo (id, id_cultivo, id_recurso, destino, cantidad, observacion, fecha) VALUES
(1, 1, 2, 'Riego',        100.0, NULL, '2024-06-01'),
(2, 1, 3, 'Fertilización', 10.0, NULL, '2024-06-02'),
(3, 2, 2, 'Riego',         80.0, NULL, '2024-06-03'),
(4, 3, 3, 'Fertilización', 5.0, NULL, '2024-06-04');


----------------------------------------------------------
-- 12. PRODUCCIÓN DE PRODUCTOS – ANIMALES
----------------------------------------------------------
INSERT INTO genera_producto_animal (id, id_animal, identificacion_producto, cantidad, fecha) VALUES
(1, 1, 'P001',  50.0, '2024-07-01'),
(2, 2, 'P001',  40.0, '2024-07-02'),
(3, 5, 'P002', 200.0, '2024-07-03');  -- Gallina 01 produjo huevos
-- Animal 6 no tiene registros aquí (para la consulta de animales sin producción)


----------------------------------------------------------
-- 13. PRODUCCIÓN DE PRODUCTOS – CULTIVOS
----------------------------------------------------------
INSERT INTO genera_producto_cultivo (id, id_cultivo, identificacion_producto, cantidad, fecha) VALUES
(1, 1, 'P003', 1000.0, '2024-09-01'),   -- Maíz
(2, 2, 'P004',  300.0, '2024-09-15'),   -- Tomate
(3, 3, 'P004',  400.0, '2024-09-20');   -- Tomate


----------------------------------------------------------
-- 14. DETALLE DE VENTAS
--     Diseñado para probar:
--     - producto más vendido (consulta 13)
--     - totales por cliente (consulta 12)
--     - detalle con join (consulta 11)
--     - filtro por fecha (consulta 18)
----------------------------------------------------------
INSERT INTO venta_detalle (id, id_venta, identificacion_producto, cantidad, precio_unit) VALUES
(1, 1, 'P001', 30.0, 2500.00),  -- venta 1
(2, 1, 'P003', 50.0, 1500.00),
(3, 2, 'P004', 80.0, 2000.00),  -- venta 2
(4, 2, 'P001', 20.0, 2600.00),
(5, 3, 'P002', 40.0,  500.00);  -- venta 3 (2024)