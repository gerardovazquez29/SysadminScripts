
import subprocess
from datetime import datetime

def ejecutar_ps(comando):
    resultado = subprocess.run(
        ["powershell", "-command", comando],
        capture_output=True, text=True
    )
    return resultado.stdout.strip()

# info del sistema
nombre_pc = ejecutar_ps("(Get-ComputerInfo).CsName")
os_nombre = ejecutar_ps("(Get-ComputerInfo).OsName")
#ram = ejecutar_ps("(Get-ComputerInfo).TotalPhysicalMemory / 1GB")
ram_comando = "[math]::Round((Get-CimInstance Win32_ComputerSystem).TotalPhysicalMemory / 1GB, 2)"
ram = ejecutar_ps(ram_comando)

# top 5 procesos
top_procesos = ejecutar_ps(
    "Get-Process | Sort-Object CPU -Descending | "
    "Select-Object -First 5 Name, CPU | "
    "Format-Table -AutoSize | Out-String"
)


# usuarios locales
usuarios = ejecutar_ps(
    "Get-LocalUser | Select-Object Name, Enabled | "
    "Format-Table | Out-String"
)

# imprimir reporte
ram_valor = 0.0
try:
    print("=" *45)
    print(f" REPORTE DEL SISTEMA")
    print(f" {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" *45)
    print(f"PC:         {nombre_pc}")
    print(f"OS:         {os_nombre}")
    ram_valor = float(ram.replace(',', '.')) # Remplazar coma por punto por si acaso
    print(f"RAM  (GB):  {ram_valor:.2f}")
    print("\n-- TOP 5 PROCESOS --")
    print(top_procesos)
    print("\n-- USUARIOS --")
    print(usuarios)
except ValueError:
    print(f"RAM (GB): Error al leer dato ({ram})")


# guardar reporte en archivo
nombre_archivo = (
    f"reporte_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
)

with open(nombre_archivo, "w", encoding="utf-8") as f:
    f.write("=" * 45 + "\n")
    f.write(f"REPORTE DEL SISTEMA\n")
    f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    f.write("=" * 45 + "\n")
    f.write(f"PC:  {nombre_pc}\n")
    f.write(f"OS:  {os_nombre}\n")
    f.write(f"RAM  (GB):  {ram_valor:.2f}")
    f.write("\n TOP 5 PROCESOS: \n")
    f.write(top_procesos)
    f.write("\n USUARIOS: \n")
    f.write(usuarios)
    
print(f"\n  Reporte guardado como: {nombre_archivo}")

