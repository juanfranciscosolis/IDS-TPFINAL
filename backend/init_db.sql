-- Crear tabla usuarios
CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    password VARCHAR(150) NOT NULL
);

-- Crear tabla habitaciones
CREATE TABLE IF NOT EXISTS habitaciones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    capacidad INT NOT NULL CHECK (capacidad > 0),
    precio_por_dia DECIMAL(10,2) NOT NULL CHECK (precio_por_dia > 0),
    disponible TINYINT(1) DEFAULT 1,
    imagen_url VARCHAR(255)
);

-- Crear tabla reservas 
CREATE TABLE IF NOT EXISTS reservas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_habitacion INT,
    id_usuario INT,
    fecha_entrada DATE NOT NULL,
    fecha_salida DATE NOT NULL,
    cantidad_personas INT NOT NULL,
    precio_total DECIMAL(10, 2) NOT NULL,
    estado VARCHAR(20) DEFAULT 'pendiente' CHECK (estado IN ('pendiente', 'cancelada')),
    CONSTRAINT fk_reserva_habitacion FOREIGN KEY (id_habitacion)
        REFERENCES habitaciones(id) ON DELETE CASCADE,
    CONSTRAINT fk_reserva_usuario FOREIGN KEY (id_usuario)
        REFERENCES usuarios(id) ON DELETE CASCADE
);

-- Datos de ejemplo
-- Insertar usuarios de ejemplo
INSERT INTO usuarios (nombre, email, password) VALUES
('María González', 'maria.gonzalez@email.com', 'password123'),
('Carlos Rodríguez', 'carlos.rodriguez@email.com', 'securepass456'),
('Ana Martínez', 'ana.martinez@email.com', 'ana789'),
('Javier López', 'javier.lopez@email.com', 'javier2024'),
('Laura Sánchez', 'laura.sanchez@email.com', 'laura_pass');

-- Insertar habitaciones de ejemplo
INSERT INTO habitaciones (nombre, descripcion, capacidad, precio_por_dia, disponible, imagen_url) VALUES
('Habitación Doble Estándar', 'Amplia habitación doble con baño privado, TV y WiFi', 2, 85.00, 1, '/img/doble-estandar.jpg'),
('Suite Ejecutiva', 'Lujosa suite con sala de estar y vista al mar', 3, 150.00, 1, '/img/suite-ejecutiva.jpg'),
('Habitación Familiar', 'Espaciosa habitación para familias, con dos camas dobles', 4, 120.00, 1, '/img/familiar.jpg'),
('Habitación Individual', 'Cómoda habitación individual para viajeros solos', 1, 65.00, 0, '/img/individual.jpg'),
('Suite Presidencial', 'Nuestra suite más exclusiva con jacuzzi y terraza privada', 2, 250.00, 1, '/img/presidencial.jpg');

-- Insertar reservas de ejemplo
INSERT INTO reservas (id_habitacion, id_usuario, fecha_entrada, fecha_salida, cantidad_personas, precio_total, estado) VALUES
(1, 1, '2024-01-15', '2024-01-18', 2, 255.00, 'pendiente'),
(2, 2, '2024-01-20', '2024-01-25', 2, 750.00, 'pendiente'),
(3, 3, '2024-02-01', '2024-02-05', 4, 480.00, 'pendiente'),
(5, 4, '2024-01-10', '2024-01-12', 2, 500.00, 'cancelada'),
(1, 5, '2024-01-22', '2024-01-24', 2, 170.00, 'pendiente');
