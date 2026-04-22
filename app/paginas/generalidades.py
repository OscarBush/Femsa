# Vista de la ventana de generalidades del negocio

import streamlit as st
import sys
from pathlib import Path

archivo_actual = Path(__file__).resolve()
base = archivo_actual.parent.parent.parent

if str(base) not in sys.path:
    sys.path.append(str(base))

try:
    from src import alertas_anuales, alertas_trimestrales, precios, graficas_anuales, graficas_trimestrales
except ImportError as e:
    print(f"Hubo un error: {e}")


def generalidades():
    st.title("Generalidades de FEMSA")
    precios.precio_historico()

    def alertas_estructurales(alertas):
        alertas_validas = [a for a in alertas if a]
        if alertas_validas:
            texto = "\n".join([f"- {a}" for a in alertas_validas])
            st.error(f"Alertas estructurales:\n\n{texto}")
        else:
            st.success("No hay alertas estructurales")

    alertas_estructurales(alertas_anuales.alertas_anuales())
    alertas_estructurales(alertas_trimestrales.alertas_trimestrales())
    st.plotly_chart(graficas_trimestrales.calificometro_trim())
    st.plotly_chart(graficas_trimestrales.radar_trimestral())
    st.plotly_chart(graficas_anuales.calificometro())
    st.plotly_chart(graficas_anuales.radar())
    st.plotly_chart(graficas_anuales.calificaciones_anuales())
    st.plotly_chart(graficas_trimestrales.calificaciones_trimestrales())
