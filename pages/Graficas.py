import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from utils import cargar_datos
from pathlib import Path
from Interfaz import aplicar_estilo_oscuro

# 1. Configuración de página (SIEMPRE LA PRIMERA LÍNEA)
st.set_page_config(page_title="Gráficas", layout="wide")

# 2. Aplicar el estilo global (Fondo de polígonos, fuentes y botones glow)
aplicar_estilo_oscuro()

def pagina_graficas():
    st.title("Análisis de Tareas")

    df = cargar_datos()

    if df.empty:
        st.info("No hay datos para analizar.")
        return
    
    # Preparación de datos
    df["duracion_minutos"] = df["duracion_segundos"] / 60

    # ---------- SECCIÓN DE FILTROS ----------
    # Sin subheaders agresivos para mantener la limpieza
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        tipos = ["Todos"] + sorted(df["tipo_tarea"].unique().tolist())
        tipo_sel = st.selectbox("Filtrar por Tarea", tipos)
    with col_f2:
        operadores = ["Todos"] + sorted(df["operador"].unique().tolist())
        operador_sel = st.selectbox("Filtrar por Operador", operadores)

    if tipo_sel != "Todos":
        df = df[df["tipo_tarea"] == tipo_sel]
    if operador_sel != "Todos":
        df = df[df["operador"] == operador_sel]

    if df.empty:
        st.warning("No hay datos con los filtros seleccionados.")
        return

    # ---------- CONFIGURACIÓN DE GRÁFICA ----------
    st.write("") # Espacio para separar de los filtros
    tipo_grafica = st.selectbox(
        "Selecciona Visualización",
        [
            "Tiempo total por tipo de tarea",
            "Tiempo total por operador",
            "Número de tareas por tipo",
            "Duración promedio por tipo"
        ]
    )

    # Estilo de la gráfica para que combine con el fondo oscuro
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(10, 5))
    
    # Hacer que los fondos del gráfico sean transparentes para ver tus polígonos
    fig.patch.set_facecolor('none') 
    ax.set_facecolor('none')

    # Color Azul Cielo Claro solicitado
    color_barras = '#87CEFA' 

    if tipo_grafica == "Tiempo total por tipo de tarea":
        datos = df.groupby("tipo_tarea")["duracion_minutos"].sum().sort_values(ascending=False)
        ax.bar(datos.index, datos.values, color=color_barras)
        ax.set_ylabel("Minutos")

    elif tipo_grafica == "Tiempo total por operador":
        datos = df.groupby("operador")["duracion_minutos"].sum().sort_values(ascending=False)
        ax.bar(datos.index, datos.values, color=color_barras)
        ax.set_ylabel("Minutos")

    elif tipo_grafica == "Número de tareas por tipo":
        datos = df["tipo_tarea"].value_counts()
        ax.bar(datos.index, datos.values, color=color_barras)
        ax.set_ylabel("Cantidad")

    elif tipo_grafica == "Duración promedio por tipo":
        datos = df.groupby("tipo_tarea")["duracion_minutos"].mean().sort_values(ascending=False)
        ax.bar(datos.index, datos.values, color=color_barras)
        ax.set_ylabel("Minutos")

    # Personalización estética del gráfico
    ax.set_title(f"{tipo_grafica}", color='white', fontsize=14, pad=20)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(axis='y', linestyle='--', alpha=0.2) # Cuadrícula muy sutil
    plt.xticks(rotation=45)
    
    st.pyplot(fig)

    # ---------- BOTÓN EXPORTAR (Solito y centrado) ----------
    st.write("") 
    st.write("") 
    
    # Tres columnas para centrar el botón en la pantalla
    col_1, col_centro, col_2 = st.columns([1, 1, 1])

    with col_centro:
        if st.button("Guardar Gráfica"):
            carpeta = Path("datos")
            carpeta.mkdir(exist_ok=True)

            # Limpiar nombre del archivo de tildes y espacios
            nombre_limpio = (
                tipo_grafica.lower()
                .replace(" ", "_")
                .translate(str.maketrans("áéíóú", "aeiou"))
            )

            ruta = carpeta / f"{nombre_limpio}.png"
            
            # Guardamos la imagen con un color de fondo sólido para que se vea bien fuera de la app
            fig.savefig(ruta, bbox_inches="tight", facecolor='#0e1117')
            st.success("Gráfica guardada en la carpeta datos")

pagina_graficas()