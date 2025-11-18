
SELECT identificacion, nombre, cargo, fecha_ingreso
FROM empleado;



SELECT identificacion, nombre, cargo, sueldo
FROM empleado
WHERE sueldo > 2000000;



SELECT e.identificacion,
       e.nombre,
       m.id AS id_maquinaria,
       m.nombre AS nombre_maquinaria,
       em.asignacion_fecha
FROM empleado e
JOIN empleado_maquinaria em
  ON e.identificacion = em.identificacion
JOIN maquinaria m
  ON em.id_maquinaria = m.id;



SELECT DISTINCT e.identificacion,
       e.nombre,
       a.id AS id_animal,
       a.nombre AS nombre_animal
FROM empleado e
JOIN empleado_animal ea
  ON e.identificacion = ea.identificacion
JOIN animal a
  ON ea.id_animal = a.id
WHERE a.especie = 'VACA'
  AND a.estado = 'VIVO';




SELECT DISTINCT e.identificacion,
       e.nombre,
       c.id AS id_cultivo,
       c.nombre AS nombre_cultivo,
       c.tipo
FROM empleado e
JOIN empleado_cultivo ec
  ON e.identificacion = ec.identificacion
JOIN cultivo c
  ON ec.id_cultivo = c.id
WHERE c.tipo = 'HORTALIZA';




SELECT a.id AS id_animal,
       COALESCE(a.nombre, '(sin nombre)') AS nombre_animal,
       r.nombre AS recurso,
       SUM(ca.cantidad) AS total_consumido
FROM consumo_animal ca
JOIN animal a
  ON ca.id_animal = a.id
JOIN recursos r
  ON ca.id_recurso = r.id
GROUP BY a.id, a.nombre, r.nombre
ORDER BY a.id, r.nombre;



SELECT c.id AS id_cultivo,
       COALESCE(c.nombre, '(sin nombre)') AS nombre_cultivo,
       r.nombre AS recurso,
       SUM(cc.cantidad) AS total_consumido
FROM consumo_cultivo cc
JOIN cultivo c
  ON cc.id_cultivo = c.id
JOIN recursos r
  ON cc.id_recurso = r.id
GROUP BY c.id, c.nombre, r.nombre
ORDER BY c.id, r.nombre;



SELECT a.id AS id_animal,
       COALESCE(a.nombre, '(sin nombre)') AS nombre_animal,
       p.identificacion AS id_producto,
       p.nombre AS producto,
       SUM(gpa.cantidad) AS total_producido
FROM genera_producto_animal gpa
JOIN animal a
  ON gpa.id_animal = a.id
JOIN producto p
  ON gpa.identificacion_producto = p.identificacion
GROUP BY a.id, a.nombre, p.identificacion, p.nombre
ORDER BY a.id, p.identificacion;




SELECT c.id AS id_cultivo,
       COALESCE(c.nombre, '(sin nombre)') AS nombre_cultivo,
       p.identificacion AS id_producto,
       p.nombre AS producto,
       SUM(gpc.cantidad) AS total_producido
FROM genera_producto_cultivo gpc
JOIN cultivo c
  ON gpc.id_cultivo = c.id
JOIN producto p
  ON gpc.identificacion_producto = p.identificacion
GROUP BY c.id, c.nombre, p.identificacion, p.nombre
ORDER BY c.id, p.identificacion;



SELECT p.identificacion,
       p.nombre,
       SUM(x.cantidad) AS total_producido
FROM (
    SELECT identificacion_producto AS id_prod, cantidad
    FROM genera_producto_animal
    UNION ALL
    SELECT identificacion_producto AS id_prod, cantidad
    FROM genera_producto_cultivo
) x
JOIN producto p
  ON p.identificacion = x.id_prod
GROUP BY p.identificacion, p.nombre
ORDER BY total_producido DESC;



SELECT v.id AS id_venta,
       v.fecha,
       c.nombre AS cliente,
       p.nombre AS producto,
       vd.cantidad,
       vd.precio_unit,
       vd.cantidad * vd.precio_unit AS subtotal
FROM venta v
JOIN cliente c
  ON v.documento_cliente = c.documento
JOIN venta_detalle vd
  ON v.id = vd.id_venta
JOIN producto p
  ON vd.identificacion_producto = p.identificacion
ORDER BY v.fecha DESC, v.id;




SELECT c.documento,
       c.nombre,
       SUM(vd.cantidad * vd.precio_unit) AS total_comprado
FROM cliente c
JOIN venta v
  ON c.documento = v.documento_cliente
JOIN venta_detalle vd
  ON v.id = vd.id_venta
GROUP BY c.documento, c.nombre
ORDER BY total_comprado DESC;




SELECT p.identificacion,
       p.nombre,
       SUM(vd.cantidad) AS total_cantidad
FROM venta_detalle vd
JOIN producto p
  ON vd.identificacion_producto = p.identificacion
GROUP BY p.identificacion, p.nombre
ORDER BY total_cantidad DESC
LIMIT 1;




SELECT e.identificacion,
       e.nombre,
       e.cargo
FROM empleado e
LEFT JOIN empleado_maquinaria em
  ON e.identificacion = em.identificacion
WHERE em.identificacion IS NULL;




SELECT a.id,
       COALESCE(a.nombre, '(sin nombre)') AS nombre_animal,
       a.especie,
       a.estado
FROM animal a
LEFT JOIN genera_producto_animal gpa
  ON a.id = gpa.id_animal
WHERE gpa.id_animal IS NULL;





SELECT cargo,
       AVG(sueldo) AS sueldo_promedio
FROM empleado
GROUP BY cargo
ORDER BY sueldo_promedio DESC;




SELECT a.id,
       COALESCE(a.nombre, '(sin nombre)') AS nombre_animal,
       SUM(ca.cantidad) AS total_consumido
FROM animal a
JOIN consumo_animal ca
  ON a.id = ca.id_animal
GROUP BY a.id, a.nombre
HAVING SUM(ca.cantidad) > 100
ORDER BY total_consumido DESC;




SELECT v.id,
       v.fecha,
       c.nombre AS cliente,
       v.total
FROM venta v
JOIN cliente c
  ON v.documento_cliente = c.documento
WHERE v.fecha BETWEEN '2025-01-01' AND '2025-12-31'
ORDER BY v.fecha;



SELECT id,
       nombre,
       tipo_recurso,
       stock
FROM recursos
WHERE stock < 20
ORDER BY stock ASC;




SELECT especie,
       estado,
       COUNT(*) AS cantidad
FROM animal
GROUP BY especie, estado
ORDER BY especie, estado;