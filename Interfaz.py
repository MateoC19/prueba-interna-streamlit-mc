import streamlit as st
import base64

def aplicar_estilo_oscuro():
    # 1. Función para cargar la imagen de fondo
    def get_base64_bin_file(bin_file):
        try:
            with open(bin_file, 'rb') as f:
                data = f.read()
            return base64.b64encode(data).decode()
        except FileNotFoundError:
            return None

    # Cargar fondo.jpg (Asegúrate de que el archivo esté en la misma carpeta)
    bin_str = get_base64_bin_file('fondo.jpg')
    
    if bin_str:
        bg_img_style = f"""
            background-image: url("data:image/jpg;base64,{bin_str}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        """
    else:
        bg_img_style = "background-color: #0e1117;"

    st.markdown(f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');

        /* --- 1. FONDO TOTAL (Incluye área de Deploy y Menú) --- */
        .stApp {{
            {bg_img_style}
            font-family: 'Inter', sans-serif;
        }}

        /* CAPA PARA ELIMINAR RUIDO Y DAR OSCURIDAD */
        .stApp::before {{
            content: "";
            position: absolute;
            top: 0; left: 0; width: 100%; height: 100%;
            background-color: rgba(0, 0, 0, 0.7); /* Oscurece la imagen */
            backdrop-filter: blur(10px); /* Elimina el granulado/ruido */
            z-index: -1;
        }}

        /* --- 2. BARRA SUPERIOR (Deploy y tres puntos) --- */
        header[data-testid="stHeader"] {{
            background-color: rgba(0,0,0,0) !important; /* Transparente */
            backdrop-filter: blur(0px) !important;
        }}
        
        /* Color de los iconos de la barra superior */
        header[data-testid="stHeader"] svg {{
            fill: white !important;
        }}

        /* --- 3. TÍTULOS (Aura plata/blanca, no roja) --- */
        h1, h2, h3 {{
            color: #ffffff !important;
            font-weight: 800 !important;
            text-shadow: 0 0 15px rgba(255, 255, 255, 0.15) !important;
            border-bottom: 2px solid rgba(255, 255, 255, 0.1) !important; /* Línea sutil plata */
            padding-bottom: 10px;
            margin-bottom: 20px;
        }}

        /* --- 4. INPUTS Y SELECTORES (Estilo Cristal) --- */
        .stTextInput > div > div > input, 
        .stSelectbox > div > div, 
        .stNumberInput > div > div > input {{
            background-color: rgba(255, 255, 255, 0.05) !important;
            color: white !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 12px !important;
        }}

        /* --- 5. BOTONES (Glow Rojo) --- */
        div.stButton > button {{
            background: linear-gradient(90deg, #ff4b2b, #ff416c) !important;
            color: white !important;
            border-radius: 25px !important;
            border: none !important;
            padding: 10px 30px !important;
            font-weight: bold !important;
            box-shadow: 0 4px 15px rgba(255, 75, 75, 0.3) !important;
            transition: all 0.3s ease;
        }}

        div.stButton > button:hover {{
            transform: scale(1.05);
            box-shadow: 0 0 25px rgba(255, 75, 75, 0.6) !important;
        }}

        /* --- 6. SIDEBAR OSCURA --- */
        [data-testid="stSidebar"] {{
            background-color: rgba(10, 10, 15, 0.9) !important;
            border-right: 1px solid rgba(255, 255, 255, 0.05);
        }}
        </style>
    """, unsafe_allow_html=True)