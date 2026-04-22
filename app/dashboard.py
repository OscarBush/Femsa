# Se crea el dashboard con la pestaña de navegación

import streamlit as st
import sys
from PIL import Image
from pathlib import Path

base = Path(__file__).resolve().parent.parent
if str(base) not in sys.path:
    sys.path.append(str(base))

try:
    from app.paginas import generalidades, tendencias_anuales, tendencias_trimestrales
except ImportError as e:
    print(f"Hubo un error: {e}")

imagen_femsa = base/"app"/"femsa_logo.png"


def dashboard():
    menu = ["Generalidades", "Tendencias anuales",
            "Tendencias trimestrales"]
    imagen = Image.open(imagen_femsa)
    st.sidebar.image(imagen)
    opciones = st.sidebar.selectbox("Menu", menu, key="dashboard")
    if opciones == "Generalidades":
        generalidades.generalidades()
    elif opciones == "Tendencias anuales":
        tendencias_anuales.tendencias_anuales()
    elif opciones == "Tendencias trimestrales":
        tendencias_trimestrales.tendencias_trimestrales()
