# Vista de la ventana de las tendencias trimestrales del negocio
import streamlit as st
import sys
from pathlib import Path

archivo_actual = Path(__file__).resolve()
base = archivo_actual.parent.parent.parent

if str(base) not in sys.path:
    sys.path.append(str(base))

try:
    from src import precios, graficas_trimestrales
except ImportError as e:
    print(f"Hubo un error: {e}")


def tendencias_trimestrales():
    st.title("Tendencias trimestrales de FEMSA")
    precios.precio_historico()
    st.plotly_chart(
        graficas_trimestrales.ultimo_estado_de_resultados_trimestral())
    st.plotly_chart(graficas_trimestrales.estados_resultados_20trim())
    st.plotly_chart(graficas_trimestrales.tendencia_trimestral_ingresos())
    st.plotly_chart(graficas_trimestrales.tendencia_trimestral_ebit())
    st.plotly_chart(
        graficas_trimestrales.tendencia_trimestral_margen_operativo())
    st.plotly_chart(graficas_trimestrales.ultimo_balance_general_trimestral())
    st.plotly_chart(
        graficas_trimestrales.ultima_figura_tiendas_y_spin_trimestral())
    st.plotly_chart(
        graficas_trimestrales.ultimas_metricas_no_financieras_trimestral())
    st.plotly_chart(
        graficas_trimestrales.tendencia_trimestral_venta_por_tienda())
    st.plotly_chart(graficas_trimestrales.tendencia_trimestral_spin())
    st.plotly_chart(graficas_trimestrales.balance_general_20trim())
    st.plotly_chart(
        graficas_trimestrales.liquidez_deuda_corto_plazo_trimestral())
