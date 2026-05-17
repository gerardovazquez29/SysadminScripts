import subprocess
from datetime import datetime

def consultar_servicio(nombre):
    resultado = subprocess.run(
        ["powerShell", "-Command", f"Get-Service {nombre}"],
        capture_output=True, text=True
    )
    return resultado.stdout

servicios = [
    "Spooler", 
    "W32Time", 
    "wuauserv",
    "MpsSvc",
    "TermService",
    "Dnscache",
    "Schedule",
    "WinDefend",
    ]

ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

print("="*50)
print(f" Monitor de servicios - {ahora}")
print("="*50)

for s in servicios:
    info = consultar_servicio(s)
    if "Running" in info:
        estado = "RUNNING"
    elif "Stopped" in info:
        estado = "DETENIDO"
    else:
        estado = "No encontrado"
         
    print(f"[{ahora}] {s:<15}: {estado}")

print("="*50)
