import streamlit as st
import os
from datetime import datetime
from utils import cargar_datos, guardar_datos, DATA_DIR
from Interfaz import aplicar_estilo_oscuro

# Siempre primero la configuración
st.set_page_config(page_title="Estimador", layout="wide")

# Luego el estilo que acabas de actualizar
aplicar_estilo_oscuro()

def lista_tareas():
    st.title("Lista de Tareas Guardadas")

    df = cargar_datos()

    if df.empty:
        st.info("No hay registros.")
        return

    df = df.sort_values("id", ascending=False)

    # --- Tabla principal ---
    st.dataframe(
        df[["id", "tipo_tarea", "lote", "operador", "inicio", "fin", "duracion_hhmmss", "nota"]],
        use_container_width=True,
        hide_index=True
    )

    # --- SECCIÓN DESCARGAR CSV (Limpia, sin líneas ni subheaders) ---
    st.write("") # Espacio sutil
    
    # Usamos columnas para centrar el botón y que se vea bien ubicado
    col_desc_1, col_desc_btn, col_desc_2 = st.columns([1, 1, 1])

    with col_desc_btn:
        if st.button("Descargar CSV"):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nombre_archivo = f"tareas_exportadas_{timestamp}.csv"
            ruta_salida = os.path.join(DATA_DIR, nombre_archivo)

            df.to_csv(ruta_salida, index=False)
            st.success(f"Guardado: {nombre_archivo}")

    # --- SECCIÓN ELIMINAR (También organizada sin subheaders agresivos) ---
    st.write("") 
    st.write("") 
    
    # Usamos un contenedor o columnas para que el selector no pegue con el botón de arriba
    col_sel_1, col_sel_2 = st.columns([2, 1])
    
    with col_sel_1:
        id_a_eliminar = st.selectbox(
            "Selecciona ID para eliminar", # Texto corto y limpio
            options=df["id"].tolist(),
            format_func=lambda x: (
                f"ID {x} | "
                f"{df.loc[df['id'] == x, 'tipo_tarea'].values[0]} - "
                f"{df.loc[df['id'] == x, 'operador'].values[0]}"
            )
        )

    # Botón eliminar centrado en su sección
    col_elim_1, col_elim_btn, col_elim_text = st.columns([0.5, 1, 2])

    with col_elim_btn:
        if st.button("Eliminar"):
            df = df[df["id"] != id_a_eliminar]
            guardar_datos(df)
            st.success(f"ID {id_a_eliminar} eliminado.")
            st.rerun()
            
    with col_elim_text:
        st.caption("Acción permanente.")


lista_tareas()
# --- SECCIÓN DESCARGAR CSV (Corregida para usuarios externos) ---
st.write("") 

# Convertimos el DataFrame a CSV en memoria (formato bytes)
csv_data = df.to_csv(index=False).encode('utf-8')

col_desc_1, col_desc_btn, col_desc_2 = st.columns([1, 1, 1])

with col_desc_btn:
    # Este es el componente correcto para que el navegador del usuario reciba el archivo
    st.download_button(
        label="Descargar CSV en mi equipo",
        data=csv_data,
        file_name=f"tareas_exportadas_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv",
    )
