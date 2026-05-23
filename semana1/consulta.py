
import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()
 
conn = psycopg2.connect(
     host="localhost",
    database="sysadmin_db",
    user="postgres",
    password=os.environ.get("DB_PASSWORD", ""),
    options="-c client_encoding=WIN1252" 
)
cur = conn.cursor()

# ver todos los reportes

cur.execute("SELECT id, fecha, nombre_pc, ram_gb FROM reportes")
for fila in cur.fetchall():
    print(fila)
    
# ver servicios del ultimo reporte
cur.execute(
    """
    SELECT s.nombre, s.estado
    FROM servicios s
    WHERE s.reporte_id = (
        SELECT id
        FROM reportes
        ORDER BY fecha DESC, id DESC
        LIMIT 1
    )
    ORDER BY s.id;
    """
)

print("\n-- Servicios ultimo reporte --")
for fila in cur.fetchall():
    print(fila)

cur.close()
conn.close()
