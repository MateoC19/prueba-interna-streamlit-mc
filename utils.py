import os
import pandas as pd
from datetime import datetime

# --- Rutas base ---
BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, "datos")
CSV_FILE = os.path.join(DATA_DIR, "tareas.csv")

# Crear carpeta datos si no existe
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# Crear CSV si no existe
if not os.path.exists(CSV_FILE):
    pd.DataFrame(
        columns=[
            "id",
            "tipo_tarea",
            "lote",
            "operador",
            "herramientas",
            "inicio",
            "fin",
            "duracion_segundos",
            "duracion_hhmmss",
            "nota",
        ]
    ).to_csv(CSV_FILE, index=False)

# --- Persistencia ---
def cargar_datos():
    return pd.read_csv(CSV_FILE)

def guardar_datos(df):
    df.to_csv(CSV_FILE, index=False)

# --- Utilidades de tiempo ---
def ahora_iso():
    return datetime.now().isoformat(sep=" ", timespec="seconds")

def duracion_segundos(inicio_iso, fin_iso):
    inicio = datetime.fromisoformat(inicio_iso)
    fin = datetime.fromisoformat(fin_iso)
    return (fin - inicio).total_seconds()

def segundos_a_hhmmss(s):
    s = int(s)
    h = s // 3600
    m = (s % 3600) // 60
    sec = s % 60
    return f"{h:02d}:{m:02d}:{sec:02d}"

def agregar_registro(
    df,
    tipo_tarea,
    lote,
    operador,
    herramientas,
    inicio_iso,
    fin_iso,
    nota="",
):
    dur_s = duracion_segundos(inicio_iso, fin_iso)
    if dur_s <= 0:
        raise ValueError("Duración inválida: fin anterior o igual al inicio.")
    nuevo_id = int(df["id"].max() + 1) if not df.empty else 1
    nuevo = {
        "id": nuevo_id,
        "tipo_tarea": tipo_tarea,
        "lote": lote,
        "operador": operador,
        "herramientas": herramientas,
        "inicio": inicio_iso,
        "fin": fin_iso,
        "duracion_segundos": dur_s,
        "duracion_hhmmss": segundos_a_hhmmss(dur_s),
        "nota": nota,
    }
    return pd.concat([df, pd.DataFrame([nuevo])], ignore_index=True)
