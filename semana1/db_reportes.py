
import psycopg2
import subprocess
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()


# conexion
conn = psycopg2.connect(
    host="localhost",
    database="sysadmin_db",
    user="postgres",
    password=os.environ.get("DB_PASSWORD", ""),
    options="-c client_encoding=WIN1252" 
)
cur = conn.cursor()

def ejecutar_ps(comando):
    r = subprocess.run(
        ["powershell", "-command", comando],
        capture_output=True, text=True
    )
    return r.stdout.strip()

#Recolectar datos
nombre_pc = ejecutar_ps("(Get-ComputerInfo).CsName")
os_nombre = ejecutar_ps("(Get-ComputerInfo).OsName")
ram_raw = ejecutar_ps(
    "[math]::Round((Get-CimInstance Win32_ComputerSystem)"
    ".TotalPhysicalMemory / 1GB, 2)"
)
ram_gb = float(ram_raw.replace(',', '.'))

# Insertar reporte principal
cur.execute(
    """
    INSERT INTO reportes (nombre_pc, os_nombre, ram_gb)
    VALUES(%s, %s, %s)
    RETURNING id
    """,
    (nombre_pc, os_nombre, ram_gb)
)
resultado = cur.fetchone()
if resultado is None:
    raise RuntimeError("No se obtuvo el id del reporte insertado")
reporte_id = resultado[0]

# Insertar top 5 procesos
procesos_raw = ejecutar_ps(
    "Get-Process | Sort-Object CPU -Descending | "
    "Select-Object -First 5 Name, CPU | "
    "ConvertTo-Csv -NoTypeInformation | Out-String"
)

for linea in procesos_raw.strip().splitlines()[1:]:
    partes = linea.replace('"', '').split(',')
    if len(partes) == 2:
        nombre_p = partes[0].strip()
        cpu_p = float(partes[1].strip() or 0)
        cur.execute(
            "INSERT INTO procesos (reporte_id, nombre, cpu)"
            "VALUES (%s, %s, %s)",
            (reporte_id, nombre_p, cpu_p)
        )
# Insertar servicios
servicios = [
    "Spooler", "W32Time", "wuauserv",
    "MpsSvc", "TermService", "Dnscache",
    "Schedule", "WinDefend"
]

for s in servicios:
    info = subprocess.run(
        ["powershell", "-Command", f"Get-Service {s}"],
        capture_output=True, text=True
    ).stdout
    estado = (
        "RUNNING" if "Running" in info
        else "DETENIDO" if "Stopped" in info
        else "NO ENCONTRADO"
    )
    cur.execute(
        "INSERT INTO servicios (reporte_id, nombre, estado) "
        "VALUES (%s, %s, %s)",
        (reporte_id, s, estado)
    )
    
conn.commit()
cur.close()
conn.close()
print(f" Reporte #{reporte_id} guardado en PostgreSQL")

