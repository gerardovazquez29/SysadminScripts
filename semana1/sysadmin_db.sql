DROP DATABASE IF EXISTS sysadmin_db;
CREATE DATABASE sysadmin_db;

CREATE TABLE reportes (
    id         SERIAL PRIMARY KEY,
    fecha      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    nombre_pc  VARCHAR(100) NOT NULL,
    os_nombre  VARCHAR(150),
    ram_gb     NUMERIC(5,2)
);

CREATE TABLE procesos (
    id          SERIAL PRIMARY KEY,
    reporte_id  INTEGER REFERENCES reportes(id) ON DELETE CASCADE,
    nombre      VARCHAR(100) NOT NULL,
    cpu         NUMERIC(10,4)
);

CREATE TABLE servicios (
    id          SERIAL PRIMARY KEY,
    reporte_id  INTEGER REFERENCES reportes(id) ON DELETE CASCADE,
    nombre      VARCHAR(100) NOT NULL,
    estado      VARCHAR(20)
);

