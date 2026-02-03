import streamlit as st
import uuid
from datetime import datetime
from Interfaz import aplicar_estilo_oscuro

# Siempre primero la configuración
st.set_page_config(page_title="Estimador", layout="wide")

# Luego el estilo que acabas de actualizar
aplicar_estilo_oscuro() 

from utils import (
    cargar_datos,
    guardar_datos,
    ahora_iso
)


# --- Utilidades locales ---
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

def agregar_registro(df, tipo_tarea, lote, operador, herramientas, inicio_iso, fin_iso, nota=""):
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

    return df._append(nuevo, ignore_index=True)

# --- Estado inicial ---
if "tipos_tarea" not in st.session_state:
    st.session_state.tipos_tarea = [
        "Siembra", "Riego", "Trasplante",
        "Cosecha", "Inspección", "Embalaje"
    ]

if "tareas_df" not in st.session_state:
    st.session_state.tareas_df = cargar_datos()

if "cronometros" not in st.session_state:
    st.session_state.cronometros = {}

# --- UI ---
st.title("Registro de Tiempos de Tareas")

tipo = st.selectbox(
    "Tipo de tarea",
    options=st.session_state.tipos_tarea
)

lote = st.text_input("Lote (opcional)")
operador = st.text_input("Operador *")
herramientas = st.text_input("Herramientas (opcional)")
nota = st.text_area("Notas (opcional)", height=80)

if not operador.strip():
    st.warning("El campo **Operador** es obligatorio.")
    st.stop()

# --- Cronómetros ---
st.subheader("Cronómetros activos")

if st.session_state.cronometros:
    cron_seleccionado = st.selectbox(
        "Selecciona un cronómetro",
        options=list(st.session_state.cronometros.keys()),
        format_func=lambda k: (
            f"{st.session_state.cronometros[k]['tipo']} – "
            f"{st.session_state.cronometros[k]['operador']}"
        )
    )
else:
    cron_seleccionado = None
    st.info("No hay cronómetros activos.")

col1, col2 = st.columns(2)

with col1:
    if st.button("Iniciar cronómetro"):
        cron_id = str(uuid.uuid4())
        st.session_state.cronometros[cron_id] = {
            "inicio": ahora_iso(),
            "tipo": tipo,
            "lote": lote,
            "operador": operador,
            "herramientas": herramientas,
            "nota": nota
        }
        st.success("Cronómetro iniciado.")

with col2:
    if st.button("Detener y guardar"):
        if not cron_seleccionado:
            st.error("No hay cronómetro seleccionado.")
        else:
            data = st.session_state.cronometros.pop(cron_seleccionado)
            fin_iso = ahora_iso()

            try:
                st.session_state.tareas_df = agregar_registro(
                    st.session_state.tareas_df,
                    data["tipo"],
                    data["lote"],
                    data["operador"],
                    data["herramientas"],
                    data["inicio"],
                    fin_iso,
                    data["nota"]
                )
                guardar_datos(st.session_state.tareas_df)
                st.success("Tarea guardada correctamente.")
            except ValueError as e:
                st.error(str(e))

# --- Entrada manual ---
st.markdown("---")
st.subheader("Entrada manual")

inicio_manual = st.text_input("Inicio (YYYY-MM-DD HH:MM:SS)")
fin_manual = st.text_input("Fin (YYYY-MM-DD HH:MM:SS)")

if st.button("Guardar entrada manual"):
    try:
        inicio_dt = datetime.fromisoformat(inicio_manual)
        fin_dt = datetime.fromisoformat(fin_manual)

        if fin_dt <= inicio_dt:
            st.error("La hora de fin debe ser posterior a la de inicio.")
            st.stop()

        st.session_state.tareas_df = agregar_registro(
            st.session_state.tareas_df,
            tipo,
            lote,
            operador,
            herramientas,
            inicio_manual,
            fin_manual,
            nota
        )
        guardar_datos(st.session_state.tareas_df)
        st.success("Registro manual guardado.")
    except Exception:
        st.error("Formato de fecha inválido o campos incompletos.")
