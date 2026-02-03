import streamlit as st
from Interfaz import aplicar_estilo_oscuro

# Siempre primero la configuración
st.set_page_config(page_title="Estimador", layout="wide")

# Luego el estilo que acabas de actualizar
aplicar_estilo_oscuro()

st.title("Gestionar tipos de tarea")

# Inicializar tipos de tarea si no existen
if "tipos_tarea" not in st.session_state:
    st.session_state.tipos_tarea = [
        "Siembra",
        "Riego",
        "Trasplante",
        "Cosecha",
        "Inspección",
        "Embalaje"
    ]

# Mostrar tipos actuales
st.subheader("Tipos de tarea existentes")
for i, tipo in enumerate(st.session_state.tipos_tarea, start=1):
    st.write(f"{i}. {tipo}")

st.markdown("---")

# Agregar nuevo tipo
st.subheader("Agregar nuevo tipo de tarea")

nuevo_tipo = st.text_input("Nombre del nuevo tipo")

if st.button("Agregar tipo"):
    nuevo_tipo = nuevo_tipo.strip()

    if not nuevo_tipo:
        st.error("El nombre no puede estar vacío.")
    elif nuevo_tipo in st.session_state.tipos_tarea:
        st.warning("Ese tipo ya existe.")
    else:
        st.session_state.tipos_tarea.append(nuevo_tipo)
        st.success("Tipo agregado correctamente.")
        st.rerun()

st.markdown("---")

# Eliminar tipo
st.subheader("Eliminar tipo de tarea")

tipo_a_eliminar = st.selectbox(
    "Selecciona un tipo",
    options=st.session_state.tipos_tarea
)

if st.button("Eliminar tipo"):
    st.session_state.tipos_tarea.remove(tipo_a_eliminar)
    st.success("Tipo eliminado correctamente.")
    st.rerun()
