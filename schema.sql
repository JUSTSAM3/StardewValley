
-- 1. EMPLEADO
CREATE TABLE IF NOT EXISTS empleado (
    identificacion VARCHAR(30) PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    cargo VARCHAR(50) NOT NULL,
    fecha_ingreso DATE NOT NULL,
    sueldo NUMERIC(12,2) NOT NULL
);

-- 2. MAQUINARIA
CREATE TABLE IF NOT EXISTS maquinaria (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    tipo VARCHAR(50) NOT NULL,
    modelo VARCHAR(50),
    estado VARCHAR(30) NOT NULL CHECK (estado IN ('DISPONIBLE', 'EN_USO', 'MANTENIMIENTO'))
);

-- 3. EMPLEADO – MAQUINARIA (M:N)
CREATE TABLE IF NOT EXISTS empleado_maquinaria (
    identificacion VARCHAR(30) REFERENCES empleado(identificacion) ON DELETE RESTRICT,
    id_maquinaria INT REFERENCES maquinaria(id) ON DELETE RESTRICT,
    asignacion_fecha DATE NOT NULL,
    PRIMARY KEY (identificacion, id_maquinaria)
);

-- 4. ANIMAL
CREATE TABLE IF NOT EXISTS animal (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100),
    especie VARCHAR(50) NOT NULL,
    raza VARCHAR(50),
    sexo VARCHAR(10) CHECK (sexo IN ('MACHO', 'HEMBRA')),
    estado VARCHAR(30) NOT NULL CHECK (estado IN ('VIVO', 'MUERTO', 'VENDIDO'))
);

-- 5. EMPLEADO – ANIMAL (M:N)
CREATE TABLE IF NOT EXISTS empleado_animal (
    identificacion VARCHAR(30) REFERENCES empleado(identificacion) ON DELETE RESTRICT,
    id_animal INT REFERENCES animal(id) ON DELETE RESTRICT,
    asignacion_fecha DATE NOT NULL,
    PRIMARY KEY (identificacion, id_animal)
);

-- 6. CULTIVO
CREATE TABLE IF NOT EXISTS cultivo (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100),
    tipo VARCHAR(50) NOT NULL,
    epoca VARCHAR(50),
    estado VARCHAR(30) NOT NULL CHECK (estado IN ('SEMILLA', 'CRECIMIENTO', 'COSECHADO')),
    fecha_siembra DATE
);

-- 7. EMPLEADO – CULTIVO (M:N)
CREATE TABLE IF NOT EXISTS empleado_cultivo (
    identificacion VARCHAR(30) REFERENCES empleado(identificacion) ON DELETE RESTRICT,
    id_cultivo INT REFERENCES cultivo(id) ON DELETE RESTRICT,
    asignacion_fecha DATE NOT NULL,
    PRIMARY KEY (identificacion, id_cultivo)
);

-- 8. RECURSOS
CREATE TABLE IF NOT EXISTS recursos (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    tipo_recurso VARCHAR(50) NOT NULL,
    stock NUMERIC(10,2) NOT NULL CHECK (stock >= 0)
);

-- 9. CONSUMO DE RECURSOS – ANIMALES
CREATE TABLE IF NOT EXISTS consumo_animal (
    id SERIAL PRIMARY KEY,
    id_animal INT NOT NULL REFERENCES animal(id) ON DELETE RESTRICT,
    id_recurso INT NOT NULL REFERENCES recursos(id) ON DELETE RESTRICT,
    destino VARCHAR(100),
    cantidad NUMERIC(10,2) NOT NULL CHECK (cantidad > 0),
    observacion TEXT,
    fecha DATE NOT NULL
);

-- 10. CONSUMO DE RECURSOS – CULTIVOS
CREATE TABLE IF NOT EXISTS consumo_cultivo (
    id SERIAL PRIMARY KEY,
    id_cultivo INT NOT NULL REFERENCES cultivo(id) ON DELETE RESTRICT,
    id_recurso INT NOT NULL REFERENCES recursos(id) ON DELETE RESTRICT,
    destino VARCHAR(100),
    cantidad NUMERIC(10,2) NOT NULL CHECK (cantidad > 0),
    observacion TEXT,
    fecha DATE NOT NULL
);

-- 11. PRODUCTO
CREATE TABLE IF NOT EXISTS producto (
    identificacion VARCHAR(30) PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    tipo VARCHAR(50) NOT NULL,
    precio NUMERIC(12,2) NOT NULL CHECK (precio >= 0)
);


-- 12. PRODUCTOS GENERADOS POR ANIMALES
CREATE TABLE IF NOT EXISTS genera_producto_animal (
    id SERIAL PRIMARY KEY,
    id_animal INT REFERENCES animal(id) ON DELETE RESTRICT,
    identificacion_producto VARCHAR(30) REFERENCES producto(identificacion) ON DELETE RESTRICT,
    cantidad NUMERIC(10,2) NOT NULL CHECK (cantidad > 0),
    fecha DATE NOT NULL
);

-- 13. PRODUCTOS GENERADOS POR CULTIVOS
CREATE TABLE IF NOT EXISTS genera_producto_cultivo (
    id SERIAL PRIMARY KEY,
    id_cultivo INT REFERENCES cultivo(id) ON DELETE RESTRICT,
    identificacion_producto VARCHAR(30) REFERENCES producto(identificacion) ON DELETE RESTRICT,
    cantidad NUMERIC(10,2) NOT NULL CHECK (cantidad > 0),
    fecha DATE NOT NULL
);


-- 14. CLIENTE
CREATE TABLE IF NOT EXISTS cliente (
    documento VARCHAR(30) PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    direccion VARCHAR(200),
    telefono VARCHAR(30),
    email VARCHAR(100)
);

-- 15. VENTA (CABECERA)
CREATE TABLE IF NOT EXISTS venta (
    id SERIAL PRIMARY KEY,
    documento_cliente VARCHAR(30) REFERENCES cliente(documento) ON DELETE RESTRICT,
    fecha TIMESTAMP NOT NULL DEFAULT NOW(),
    total NUMERIC(12,2)
);

-- 16. DETALLE DE VENTA
CREATE TABLE IF NOT EXISTS venta_detalle (
    id SERIAL PRIMARY KEY,
    id_venta INT REFERENCES venta(id) ON DELETE CASCADE,
    identificacion_producto VARCHAR(30) REFERENCES producto(identificacion) ON DELETE RESTRICT,
    cantidad NUMERIC(10,2) NOT NULL CHECK (cantidad > 0),
    precio_unit NUMERIC(12,2) NOT NULL CHECK (precio_unit >= 0)
);

CREATE INDEX IF NOT EXISTS idx_animal_recurso_fecha 
    ON consumo_animal(fecha);

CREATE INDEX IF NOT EXISTS idx_cultivo_recurso_fecha 
    ON consumo_cultivo(fecha);

CREATE INDEX IF NOT EXISTS idx_producto_tipo 
    ON producto(tipo);

CREATE INDEX IF NOT EXISTS idx_venta_fecha 
    ON venta(fecha);
