import streamlit as st
import os
import io
from datetime import datetime
from utils import cargar_datos, guardar_datos, DATA_DIR
from Interfaz import aplicar_estilo_oscuro

# 1. Configuración de página (SIEMPRE PRIMERO)
st.set_page_config(page_title="Lista de Tareas", layout="wide")

# 2. Aplicar estilo
aplicar_estilo_oscuro()

def lista_tareas():
    st.title("Lista de Tareas Guardadas")

    df = cargar_datos()

    if df.empty:
        st.info("No hay registros disponibles.")
        return

    df = df.sort_values("id", ascending=False)

    # --- Tabla principal ---
    st.dataframe(
        df[["id", "tipo_tarea", "lote", "operador", "inicio", "fin", "duracion_hhmmss", "nota"]],
        use_container_width=True,
        hide_index=True
    )

    st.write("") 
    
    # --- SECCIÓN DESCARGAR CSV (Corregida para usuarios externos) ---
    col_desc_1, col_desc_btn, col_desc_2 = st.columns([1, 1, 1])

    with col_desc_btn:
        # Convertimos el DataFrame a CSV en memoria
        csv_buffer = df.to_csv(index=False).encode('utf-8')
        
        st.download_button(
            label="Descargar Reporte CSV",
            data=csv_buffer,
            file_name=f"reporte_tareas_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
        )

    # --- SECCIÓN ELIMINAR ---
    st.markdown("---")
    st.subheader("Eliminar Registro")
    
    col_sel_1, col_sel_2 = st.columns([2, 1])
    
    with col_sel_1:
        id_a_eliminar = st.selectbox(
            "Selecciona ID para eliminar",
            options=df["id"].tolist(),
            format_func=lambda x: f"ID {x} | {df.loc[df['id'] == x, 'tipo_tarea'].values[0]}"
        )

    with col_sel_2:
        st.write(" ") # Espaciador
        if st.button("Eliminar Tarea", use_container_width=True):
            df = df[df["id"] != id_a_eliminar]
            guardar_datos(df)
            st.success(f"Registro {id_a_eliminar} eliminado.")
            st.rerun()

if __name__ == "__main__":
    lista_tareas()
