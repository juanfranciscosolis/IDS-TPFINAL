# 📋 Flujo del Backend - Hotel IDS

## 1. Arquitectura General

```
┌─────────────────────────────────────────────────────────────────┐
│                        CLIENTE (Frontend)                        │
│                      (Flask App - Port 5010)                    │
└────────────────────────────┬────────────────────────────────────┘
                             │
                    (HTTP Requests/Responses)
                             │
         ┌───────────────────┼───────────────────┐
         │                   │                   │
         ▼                   ▼                   ▼
    ┌─────────┐         ┌─────────┐         ┌────────┐
    │USUARIOS │         │HABITACIONES│      │RESERVAS│
    │ Routes  │         │  Routes │         │ Routes │
    └─────────┘         └─────────┘         └────────┘
         │                   │                   │
         └───────────────────┼───────────────────┘
                             │
                   (Conexión a Base Datos)
                             │
         ┌───────────────────┼───────────────────┐
         │                   │                   │
         ▼                   ▼                   ▼
    ┌──────────┐         ┌────────────┐     ┌──────────┐
    │ USUARIOS │         │HABITACIONES│     │ RESERVAS │
    │  Tabla   │         │   Tabla    │     │  Tabla   │
    └──────────┘         └────────────┘     └──────────┘
         │                   │                   │
         └───────────────────┼───────────────────┘
                             │
                        ┌────────────┐
                        │ MySQL DB   │
                        └────────────┘
```

---

## 2. Estructura del Proyecto

```
backend/
│
├── app.py                    # Aplicación principal Flask
├── db.py                     # Conexión a Base de Datos
├── init_db.py                # Inicialización de BD
├── init_db.sql               # Script SQL
├── requirements.txt          # Dependencias Python
│
├── routes/                   # Rutas de la API REST
│   ├── usuarios.py           # Endpoints de usuarios
│   ├── habitaciones.py       # Endpoints de habitaciones
│   └── reservas.py           # Endpoints de reservas
│
└── .env                      # Variables de entorno
```

---

## 3. Flujo de Inicialización de la Aplicación

```
1. Ejecutar app.py
    │
    ├─→ Cargar variables de entorno (.env)
    │   ├─ DB_HOST, DB_NAME, DB_USER, DB_PASSWORD
    │   ├─ FLASK_SECRET_KEY
    │   ├─ MAIL_USERNAME, MAIL_PASSWORD
    │   └─ MAIL_DEFAULT_SENDER
    │
    ├─→ Crear instancia Flask
    │   └─ Activar CORS
    │
    ├─→ Configurar Flask-Mail (SMTP Gmail)
    │   ├─ Host: smtp.gmail.com
    │   ├─ Port: 587 (TLS)
    │   └─ Credenciales desde .env
    │
    ├─→ Registrar Blueprints (Rutas)
    │   ├─ /habitaciones → habitaciones_bp
    │   ├─ /reservas → reservas_bp
    │   └─ /usuarios → usuarios_bp
    │
    └─→ Iniciar servidor
        └─ Port: 5010 (debug=True)
```

---

## 4. Endpoints de la API

### 4.1 USUARIOS (url_prefix="/usuarios")

```
┌─────────────────────────────────────────────────────────────────┐
│                    USUARIOS - Endpoints                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│ GET /usuarios/                                                   │
│ └─→ Obtener todos los usuarios                                   │
│     ├─ SELECT id, nombre, email FROM usuarios                    │
│     └─ Return: JSON Array de usuarios [200]                      │
│                                                                   │
│ GET /usuarios/<id_usuario>                                       │
│ └─→ Obtener un usuario específico                                │
│     ├─ SELECT FROM usuarios WHERE id = id_usuario                │
│     ├─ Return: JSON Usuario [200]                                │
│     └─ Return: {error: "usuario no encontrado"} [404]            │
│                                                                   │
│ POST /usuarios/                                                  │
│ └─→ Crear nuevo usuario                                          │
│     ├─ Input JSON: { name, email, password }                     │
│     ├─ Validar: Email no duplicado (query SELECT)                │
│     ├─ INSERT INTO usuarios (nombre, email, password)            │
│     ├─ Return: Nuevo usuario creado [201]                        │
│     └─ Return: {error: "El usuario ya existe"} [409]             │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

### 4.2 HABITACIONES (url_prefix="/habitaciones")

```
┌─────────────────────────────────────────────────────────────────┐
│                  HABITACIONES - Endpoints                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│ GET /habitaciones/                                               │
│ └─→ Obtener todas las habitaciones                               │
│     ├─ SELECT * FROM habitaciones                                │
│     └─ Return: JSON Array de habitaciones [200]                  │
│                                                                   │
│ GET /habitaciones/<habitacion_id>                                │
│ └─→ Obtener habitación específica                                │
│     ├─ SELECT * FROM habitaciones WHERE id = habitacion_id       │
│     ├─ Return: JSON Habitación [200]                             │
│     └─ Return: {Error: "Habitacion no encontrada"} [404]         │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

### 4.3 RESERVAS (url_prefix="/reservas")

```
┌─────────────────────────────────────────────────────────────────┐
│                     RESERVAS - Endpoints                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│ GET /reservas/                                                   │
│ └─→ Listar todas las reservas                                    │
│     ├─ SELECT r.*, h.nombre, u.nombre                            │
│     ├─ LEFT JOIN habitaciones y usuarios                         │
│     ├─ ORDER BY r.id DESC                                        │
│     └─ Return: JSON Array de reservas [200]                      │
│                                                                   │
│ GET /reservas/usuario/<usuario_id>                               │
│ └─→ Obtener reservas de un usuario                               │
│     ├─ SELECT r.*, h.nombre, u.nombre                            │
│     ├─ WHERE r.id_usuario = usuario_id                           │
│     └─ Return: JSON Array de reservas del usuario [200]          │
│                                                                   │
│ POST /reservas/                                                  │
│ └─→ Crear nueva reserva                                          │
│     ├─ Input JSON: {id_usuario, id_habitacion, ...}              │
│     ├─ Validar: Usuario existe, Habitación existe                │
│     ├─ Validar: Fechas válidas y disponibilidad                  │
│     ├─ INSERT INTO reservas                                      │
│     ├─ Enviar email de confirmación (Flask-Mail)                 │
│     └─ Return: Reserva creada [201]                              │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

---

## 5. Flujo de Conexión a Base de Datos

```
Cada solicitud HTTP
│
├─→ Route handler (usuarios.py, habitaciones.py, reservas.py)
│
├─→ Llamar get_connection() desde db.py
│   │
│   └─→ mysql.connector.connect(
│       ├─ host: env("DB_HOST") → localhost
│       ├─ database: env("DB_NAME") → hotel_ids
│       ├─ user: env("DB_USER") → root
│       ├─ password: env("DB_PASSWORD")
│       └─ port: env("DB_PORT") → 3306
│       )
│
├─→ Crear cursor (dictionary=True → resultados como diccionarios)
│
├─→ Ejecutar query SQL
│   ├─ SELECT, INSERT, UPDATE, DELETE, etc.
│   └─ Usar %s para parámetros (SQL injection safe)
│
├─→ Procesar resultados
│   ├─ cursor.fetchall() → lista de registros
│   ├─ cursor.fetchone() → un registro
│   └─ conn.commit() → confirmar cambios en INSERT/UPDATE
│
├─→ Cerrar cursor y conexión
│   ├─ cursor.close()
│   └─ conn.close()
│
└─→ Retornar respuesta JSON al cliente
    └─ jsonify(data), HTTP_STATUS_CODE
```

---

## 6. Flujo de Creación de Usuario

```
Cliente HTTP
│
├─→ POST /usuarios/ con JSON:
│   {
│     "name": "Juan Pérez",
│     "email": "juan@email.com",
│     "password": "micontraseña"
│   }
│
├─→ crear_usuario() en usuarios.py
│   │
│   ├─→ Extraer datos: name, email, password
│   │
│   ├─→ Conectar a BD
│   │
│   ├─→ Validar: ¿Email ya existe?
│   │   └─ SELECT id FROM usuarios WHERE email = email
│   │   └─ Si existe → Return {error: "El usuario ya existe"} [409]
│   │
│   ├─→ Insertar nuevo usuario
│   │   └─ INSERT INTO usuarios (nombre, email, password)
│   │   └─ conn.commit()
│   │
│   ├─→ Cerrar conexión
│   │
│   └─→ Return Usuario creado [201]
│
└─→ Cliente recibe respuesta JSON con nuevo usuario
```

---

## 7. Flujo de Creación de Reserva (con Email)

```
Cliente HTTP
│
├─→ POST /reservas/ con JSON:
│   {
│     "id_usuario": 1,
│     "id_habitacion": 5,
│     "fecha_inicio": "2024-12-10",
│     "fecha_fin": "2024-12-15",
│     "comentarios": "..."
│   }
│
├─→ Crear_reserva() en reservas.py
│   │
│   ├─→ Extraer datos del JSON
│   │
│   ├─→ Conectar a BD
│   │
│   ├─→ Validaciones
│   │   ├─ ¿Usuario existe? SELECT FROM usuarios WHERE id
│   │   ├─ ¿Habitación existe? SELECT FROM habitaciones WHERE id
│   │   ├─ ¿Fechas válidas? (fecha_fin > fecha_inicio)
│   │   └─ ¿Habitación disponible? SELECT FROM reservas (overlapping dates)
│   │
│   ├─→ INSERT INTO reservas (id_usuario, id_habitacion, ...)
│   │   └─ conn.commit()
│   │
│   ├─→ Obtener datos del usuario y habitación para email
│   │   ├─ SELECT nombre, email FROM usuarios WHERE id
│   │   └─ SELECT nombre, precio FROM habitaciones WHERE id
│   │
│   ├─→ Preparar email con Flask-Mail
│   │   ├─ Usar SMTP Gmail (config en app.py)
│   │   ├─ To: correo_usuario
│   │   ├─ Subject: "Reserva confirmada - Hotel IDS"
│   │   ├─ Body: HTML con detalles de la reserva
│   │   └─ msg.send(mail)
│   │
│   ├─→ Cerrar conexión a BD
│   │
│   └─→ Return Reserva creada [201]
│
└─→ Cliente recibe JSON + Email fue enviado al usuario
```

---

## 8. Stack Tecnológico

| Componente | Tecnología | Versión |
|-----------|-----------|---------|
| Framework Web | Flask | - |
| Extensiones | Flask-CORS | - |
| | Flask-Mail | - |
| Base de Datos | MySQL | - |
| Driver MySQL | mysql-connector-python | - |
| Env Manager | python-dotenv | - |
| Lenguaje | Python | 3.x |

---

## 9. Variables de Entorno (.env)

```
# Base de Datos
DB_HOST=localhost
DB_PORT=3306
DB_NAME=hotel_ids
DB_USER=root
DB_PASSWORD=tu_contraseña

# Flask
FLASK_SECRET_KEY=c7f1f6e8e9c54b3db5a2f0b0c2a4c3f6e1d9d8f7a6b5c4d3e2f1a0b9c8d7e6f5

# Email (SMTP Gmail)
MAIL_USERNAME=tu_email@gmail.com
MAIL_PASSWORD=tu_contraseña_app
MAIL_DEFAULT_SENDER_NAME=Hotel IDS
MAIL_DEFAULT_SENDER_EMAIL=tu_email@gmail.com
```

---

## 10. Ciclo de una Solicitud HTTP Completo

```
┌─────────────────────────────────────────────────────────────────┐
│ 1. Cliente (Frontend) envía solicitud HTTP                       │
│    GET /usuarios/ (o POST, PUT, DELETE)                         │
└─────────────────────┬───────────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────────┐
│ 2. Flask recibe la solicitud                                     │
│    • Valida la ruta (URL routing)                                │
│    • Mapea al endpoint correcto                                  │
└─────────────────────┬───────────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────────┐
│ 3. Ejecuta el function handler correspondiente                   │
│    (get_usuarios, crear_usuario, crear_reserva, etc.)          │
└─────────────────────┬───────────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────────┐
│ 4. Conectar a BD (get_connection)                                │
│    • Lee variables de entorno                                    │
│    • Crea conexión MySQL                                         │
│    • Retorna objeto de conexión                                  │
└─────────────────────┬───────────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────────┐
│ 5. Ejecutar query SQL                                            │
│    • Crear cursor                                                │
│    • execute() con parámetros                                    │
│    • fetchall() / fetchone() para SELECT                         │
│    • commit() para INSERT/UPDATE/DELETE                          │
└─────────────────────┬───────────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────────┐
│ 6. Procesar resultados                                           │
│    • Transformar datos si es necesario                           │
│    • Validar datos                                               │
│    • Manejar errores                                             │
└─────────────────────┬───────────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────────┐
│ 7. (Opcional) Enviar emails                                      │
│    • Preparar mensaje                                            │
│    • Usar Flask-Mail (SMTP)                                      │
│    • msg.send(mail)                                              │
└─────────────────────┬───────────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────────┐
│ 8. Cerrar conexión a BD                                          │
│    • cursor.close()                                              │
│    • conn.close()                                                │
└─────────────────────┬───────────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────────┐
│ 9. Crear respuesta JSON                                          │
│    • jsonify(data)                                               │
│    • HTTP Status Code (200, 201, 404, 409, etc.)                │
└─────────────────────┬───────────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────────┐
│ 10. Retornar respuesta al cliente                                │
│     Cliente recibe JSON + status code                            │
└─────────────────────────────────────────────────────────────────┘
```

---

## 11. Tabla de HTTP Status Codes Utilizados

| Código | Significado | Uso |
|--------|-----------|-----|
| 200 | OK | GET exitoso, datos encontrados |
| 201 | Created | POST exitoso, recurso creado |
| 400 | Bad Request | Error en los datos enviados |
| 404 | Not Found | Recurso no encontrado |
| 409 | Conflict | Email duplicado, conflicto de datos |
| 500 | Server Error | Error del servidor |

---

## 12. Modelo de Datos (Tablas)

```
┌─────────────────────────────┐
│     USUARIOS                │
├─────────────────────────────┤
│ id (PK)                     │
│ nombre (VARCHAR)            │
│ email (VARCHAR, UNIQUE)     │
│ password (VARCHAR)          │
│ created_at (TIMESTAMP)      │
└─────────────────────────────┘
         △
         │ FK
         │
┌─────────────────────────────┐
│     RESERVAS                │
├─────────────────────────────┤
│ id (PK)                     │
│ id_usuario (FK)──────────────
│ id_habitacion (FK)──┐       │
│ fecha_inicio        │       │
│ fecha_fin           │       │
│ comentarios         │       │
│ created_at          │       │
└─────────────────────┼───────┘
                      │
                      △
                      │ FK
         ┌────────────┘
         │
┌─────────────────────────────┐
│   HABITACIONES              │
├─────────────────────────────┤
│ id (PK)                     │
│ nombre (VARCHAR)            │
│ descripcion (TEXT)          │
│ precio (DECIMAL)            │
│ capacidad (INT)             │
│ disponible (BOOLEAN)        │
│ created_at (TIMESTAMP)      │
└─────────────────────────────┘
```

---

## Notas Importantes

1. **CORS Habilitado**: Las solicitudes desde el frontend (otro puerto/dominio) son permitidas
2. **Variables de Entorno**: Todas las credenciales sensibles están en `.env` (no en el código)
3. **Parámetros Seguros**: Se usan placeholders `%s` para evitar SQL Injection
4. **Gestión de Conexiones**: Cada request abre y cierra su conexión (no hay pool)
5. **Email Asincrónico**: Los emails se envían de forma síncrona (puede optimizarse con Celery/RabbitMQ)

---

Este documento te servirá como guía para entender el flujo completo del backend 🚀
