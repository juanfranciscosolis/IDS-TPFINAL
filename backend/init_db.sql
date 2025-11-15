-- Crear base de datos
SELECT 'CREATE DATABASE hotel_db'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'hotel_db')\gexec

-- Conectar a la base de datos
\c hotel_db;

-- Crear tabla habitaciones
CREATE TABLE IF NOT EXISTS habitaciones (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    capacidad INTEGER NOT NULL,
    precio_por_dia DECIMAL(10,2) NOT NULL,
    disponible BOOLEAN DEFAULT TRUE,
    imagen_url VARCHAR(255)
);

-- Crear tabla reservas 
CREATE TABLE IF NOT EXISTS reservas (
    id SERIAL PRIMARY KEY,
    nombre_cliente VARCHAR(100) NOT NULL,
    email_cliente VARCHAR(150) NOT NULL,
    fecha_checkin DATE NOT NULL,
    fecha_checkout DATE NOT NULL,
    cantidad_personas INTEGER,
    id_habitaciones INTEGER NOT NULL,
    FOREIGN KEY (id_habitaciones) REFERENCES habitaciones(id) ON DELETE CASCADE
);

-- Datos de ejemplo
INSERT INTO habitaciones (id, nombre, descripcion, capacidad, precio_por_dia, disponible, imagen_url)
SELECT 1, 'Habitación Standard', 'Habitación cómoda con cama doble y baño privado', 2, 100.00, true, 'static/images/standard.jpg'
WHERE NOT EXISTS (SELECT 1 FROM habitaciones WHERE id = 1);

INSERT INTO habitaciones (id, nombre, descripcion, capacidad, precio_por_dia, disponible, imagen_url)
SELECT 2, 'Habitación Individual', 'Habitación ideal para una persona', 1, 80.00, true, 'static/images/individual.jpg'
WHERE NOT EXISTS (SELECT 1 FROM habitaciones WHERE id = 2);

INSERT INTO habitaciones (id, nombre, descripcion, capacidad, precio_por_dia, disponible, imagen_url)
SELECT 3, 'Habitación Económica', 'Habitación básica pero confortable', 1, 50.00, true, 'static/images/economica.jpg'
WHERE NOT EXISTS (SELECT 1 FROM habitaciones WHERE id = 3);


INSERT INTO reservas (id, nombre_cliente, email_cliente, fecha_checkin, fecha_checkout, cantidad_personas, id_habitaciones)
VALUES 
    (1, 'María González', 'maria.gonzalez@email.com', '2024-12-15', '2024-12-20', 2, 1)
ON CONFLICT (id) DO NOTHING;

-- Mostrar resultados
SELECT 'Habitaciones insertadas: ' || COUNT(*)::TEXT as total FROM habitaciones;
SELECT 'reservas insertadas: ' || COUNT(*)::TEXT as total FROM reservas;

SELECT 'DETALLES DE HABITACIONES:' as info;
SELECT 
    id, 
    nombre, 
    capacidad, 
    precio_por_dia, 
    disponible 
FROM habitaciones 
ORDER BY id;

SELECT '=== DETALLES DE RESERVAS ===' as info;
SELECT 
    r.id,
    r.nombre_cliente,
    r.email_cliente,
    r.fecha_checkin,
    r.fecha_checkout,
    r.cantidad_personas,
    h.nombre as habitacion,
    h.precio_por_dia
FROM reservas r
JOIN habitaciones h ON r.id_habitaciones = h.id
ORDER BY r.id;