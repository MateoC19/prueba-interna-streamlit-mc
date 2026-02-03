import streamlit as st
from Interfaz import aplicar_estilo_oscuro

# 1. Configuración de página (SIEMPRE PRIMERO)
st.set_page_config(page_title="Página Principal", layout="wide")

# 2. Aplicar el estilo global (Fondo fluido, barra transparente, etc.)
aplicar_estilo_oscuro()

# ---------- CSS PARA CENTRADO ABSOLUTO ----------
st.markdown("""
<style>
/* Forzamos que el contenedor de Streamlit permita centrado */
[data-testid="stVerticalBlock"] > div:has(div.main-content) {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
}

.main-content {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    /* Ajustamos la altura restando la barra superior para un centrado real */
    height: 75vh; 
    width: 100%;
}

/* Quitamos la línea de los títulos para este mensaje de bienvenida */
.main-content h1 {
    border: none !important;
    font-size: 3.5rem !important;
    margin-bottom: 0px !important;
    text-shadow: 0 0 20px rgba(255,255,255,0.2) !important;
}

.main-content h2 {
    border: none !important;
    font-weight: 400 !important;
    color: rgba(255,255,255,0.7) !important;
    margin-top: 10px !important;
}

.author-footer {
    margin-top: 50px;
    font-size: 1rem;
    letter-spacing: 2px;
    color: rgba(255,255,255,0.4);
    text-transform: uppercase;
}
</style>
""", unsafe_allow_html=True)

# ---------- CONTENIDO CENTRADO ----------
st.markdown("""
<div class="main-content">
    <h1>BIENVENIDO</h1>
    <h2>Usa el menú lateral para explorar las secciones</h2>
    <div class="author-footer">Matteo Cortés - 2026</div>
</div>
""", unsafe_allow_html=True)