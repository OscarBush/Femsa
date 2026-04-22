# Vista de la ventana de las tendencias anuales del negocio
import streamlit as st
import sys
from pathlib import Path

archivo_actual = Path(__file__).resolve()
base = archivo_actual.parent.parent.parent

if str(base) not in sys.path:
    sys.path.append(str(base))

try:
    from src import precios, graficas_anuales
except ImportError as e:
    print(f"Hubo un error: {e}")


def tendencias_anuales():
    st.title("Tendencias anuales de FEMSA")
    precios.precio_historico()
    st.plotly_chart(graficas_anuales.ultimo_estado_de_resultados_anual())
    st.plotly_chart(graficas_anuales.estados_resultados_10a())
    st.plotly_chart(graficas_anuales.ultimo_balance_general_anual())
    st.plotly_chart(graficas_anuales.balance_general_10a())
    st.plotly_chart(graficas_anuales.ultimo_fcf_anual())
    st.plotly_chart(graficas_anuales.fcf_10a())
    st.plotly_chart(graficas_anuales.roic_menos_wacc())
    st.plotly_chart(graficas_anuales.val_econ_agregado())
