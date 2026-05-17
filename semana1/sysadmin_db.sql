
CREATE DATABASE sysadmin_db;

\c sysadmin_db;

CREATE TABLE reportes (
    id         SERIAL PRIMARY KEY,
    fecha      TIMESTAMP DEFAULT NOW(),
    nombre_pc  VARCHAR(100),
    os_nombre  VARCHAR(150),
    ram_gb     NUMERIC(5,2)
);

CREATE TABLE procesos (
    id          SERIAL PRIMARY KEY,
    reporte_id  INTEGER REFERENCES reportes(id),
    nombre      VARCHAR(100),
    cpu         NUMERIC(10,4)
);

CREATE TABLE servicios (
    id          SERIAL PRIMARY KEY,
    reporte_id  INTEGER REFERENCES reportes(id),
    nombre      VARCHAR(100),
    estado      VARCHAR(20)
);

