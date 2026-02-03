import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io
from utils import cargar_datos
from Interfaz import aplicar_estilo_oscuro

# 1. Configuración de página
st.set_page_config(page_title="Análisis Gráfico", layout="wide")

# 2. Estilo
aplicar_estilo_oscuro()

def pagina_graficas():
    st.title("Análisis de Tareas")

    df = cargar_datos()

    if df.empty:
        st.info("No hay datos para analizar.")
        return
    
    df["duracion_minutos"] = df["duracion_segundos"] / 60

    # Filtros
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        tipos = ["Todos"] + sorted(df["tipo_tarea"].unique().tolist())
        tipo_sel = st.selectbox("Filtrar por Tarea", tipos)
    with col_f2:
        tipo_grafica = st.selectbox("Tipo de Gráfico", ["Total horas por tipo", "Duración promedio por tipo"])

    # Lógica de filtrado
    df_plot = df.copy()
    if tipo_sel != "Todos":
        df_plot = df_plot[df_plot["tipo_tarea"] == tipo_sel]

    # Crear la figura
    fig, ax = plt.subplots(figsize=(10, 5))
    fig.patch.set_facecolor('#0e1117') # Fondo oscuro para el gráfico
    ax.set_facecolor('#0e1117')
    
    color_barras = '#ff4b2b'

    if tipo_grafica == "Total horas por tipo":
        datos = df_plot.groupby("tipo_tarea")["duracion_minutos"].sum() / 60
        ax.bar(datos.index, datos.values, color=color_barras)
        ax.set_ylabel("Horas Totales", color='white')
    else:
        datos = df_plot.groupby("tipo_tarea")["duracion_minutos"].mean()
        ax.bar(datos.index, datos.values, color=color_barras)
        ax.set_ylabel("Promedio Minutos", color='white')

    # Estética
    ax.tick_params(colors='white')
    ax.spines['bottom'].set_color('white')
    ax.spines['left'].set_color('white')
    plt.xticks(rotation=45)
    st.pyplot(fig)

    # --- BOTÓN DESCARGAR GRÁFICA (CORREGIDO) ---
    st.write("")
    
    # Guardar en buffer de memoria
    buf = io.BytesIO()
    plt.savefig(buf, format="png", bbox_inches='tight')
    buf.seek(0)

    col_1, col_centro, col_2 = st.columns([1, 1, 1])
    with col_centro:
        st.download_button(
            label="Descargar Gráfica (PNG)",
            data=buf,
            file_name=f"grafica_{datetime.now().strftime('%Y%m%d')}.png",
            mime="image/png"
        )

if __name__ == "__main__":
    pagina_graficas()
