import streamlit as st
import pandas as pd
from utils import cargar_datos
from Interfaz import aplicar_estilo_oscuro

# 1. Configuración de página (SIEMPRE PRIMERO)
st.set_page_config(page_title="Estimador de tiempo", layout="wide")

# 2. Aplicar estilo global
aplicar_estilo_oscuro()

def pagina_estimador():
    st.title("Calculadora de Tiempo Estimado")

    df = cargar_datos()

    if df.empty:
        st.info("No hay datos para estimar tiempos.")
        return
    else:
        df["duracion_minutos"] = df["duracion_segundos"] / 60

    # ---------- FILTROS ----------
    st.write("") # Espacio sutil
    col1, col2, col3 = st.columns(3)

    with col1:
        tipos = ["Todos"] + sorted(df["tipo_tarea"].unique().tolist())
        tipo_sel = st.selectbox("Tipo de Tarea", tipos)

    with col2:
        operadores = ["Todos"] + sorted(df["operador"].unique().tolist())
        operador_sel = st.selectbox("Operador", operadores)

    with col3:
        cantidad_unidades = st.number_input(
            "Cantidad de Unidades", min_value=1, step=1, value=1
        )

    # Filtrado
    df_filtrado = df.copy()
    if tipo_sel != "Todos":
        df_filtrado = df_filtrado[df_filtrado["tipo_tarea"] == tipo_sel]
    if operador_sel != "Todos":
        df_filtrado = df_filtrado[df_filtrado["operador"] == operador_sel]

    if df_filtrado.empty:
        st.warning("No hay datos suficientes para realizar el cálculo.")
        return

    # ---------- CÁLCULO ----------
    
    tiempo_promedio = df_filtrado["duracion_minutos"].mean()
    tiempo_estimado = tiempo_promedio * cantidad_unidades
    tiempo_estimado_rounded = round(tiempo_estimado)

    # ---------- RESULTADOS ESTILO DASHBOARD ----------
    st.write("") 
    st.write("") 
    
    # Título sin línea decorativa para la zona de resultados
    st.markdown("<h3 style='border:none; margin-bottom:0px;'>Análisis de Resultado</h3>", unsafe_allow_html=True)
    
    # Creamos un contenedor visual usando columnas y Markdown con CSS inyectado
    m1, m2 = st.columns(2)

    with m1:
        st.markdown(f"""
            <div style="
                background: rgba(255, 255, 255, 0.05);
                padding: 25px;
                border-radius: 15px;
                border-left: 5px solid #87CEFA;
                backdrop-filter: blur(10px);
                ">
                <p style="color: #87CEFA; font-size: 0.9rem; font-weight: bold; text-transform: uppercase; margin:0;">Tiempo Promedio / Unidad</p>
                <h2 style="color: white; border: none; margin: 0; padding: 0;">{tiempo_promedio:.2f} <span style="font-size: 1.2rem; color: #87CEFA;">min</span></h2>
            </div>
        """, unsafe_allow_html=True)

    with m2:
        st.markdown(f"""
            <div style="
                background: rgba(255, 255, 255, 0.05);
                padding: 25px;
                border-radius: 15px;
                border-left: 5px solid #ff4b2b;
                backdrop-filter: blur(10px);
                box-shadow: 0 4px 15px rgba(255, 75, 43, 0.1);
                ">
                <p style="color: #ff4b2b; font-size: 0.9rem; font-weight: bold; text-transform: uppercase; margin:0;">Tiempo Estimado Total</p>
                <h2 style="color: white; border: none; margin: 0; padding: 0;">{tiempo_estimado_rounded} <span style="font-size: 1.2rem; color: #ff4b2b;">min</span></h2>
            </div>
        """, unsafe_allow_html=True)

pagina_estimador()