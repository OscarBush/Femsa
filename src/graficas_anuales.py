# Genera las gráficas anuales de FEMSA

from pathlib import Path
from PIL import Image
from datos import umbrales
from src import alertas_anuales as alertas
from src import metricas
from src import reglas
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st


DIRECTORIO_BASE = Path(__file__).resolve().parent.parent
RUTA_DATOS = DIRECTORIO_BASE/'datos'
femsa_anual = RUTA_DATOS/'femsa_anual.csv'


def cargar_datos(df):
    df_cargado = pd.read_csv(df)
    return df_cargado.tail(10)


df_anual = cargar_datos(femsa_anual)
df_lista = [metricas.calidad_anual(df_anual), metricas.crecimiento_anual(df_anual), metricas.solidez_anual(
    df_anual), metricas.estructura_anual(df_anual), metricas.dividendo_anual(df_anual)]

# GRÁFICAS PARA GENERALIDADES

# Gráfica de calificación anual


def color_calificacion(calificacion):
    if calificacion < 4.0:
        return "#ea7f7f", "Débil"
    elif calificacion < 6.0:
        return "#e39960", "Recuperable"
    elif calificacion < 7.5:
        return "#f2f229", "Aceptable"
    elif calificacion < 9.0:
        return "#5FBA82", "Muy buena"
    else:
        return "#6b9ccd", "Excelente"


def gauge_calificacion(calificacion, titulo="Última calificación anual"):
    color, etiqueta = color_calificacion(calificacion)
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=calificacion,
        number={
            "font": {"size": 70, "color": color},
            "suffix": ""
        },
        title={
            "text": f"""
        <span style='font-size:24px;color:#cbd5e1'>{etiqueta}</span>
        """,
            "font": {"size": 32}
        },
        gauge={
            "axis": {
                "range": [0, 10],
                "tickwidth": 1,
                "tickcolor": "#94a3b8",
                "tickfont": {"color": "#cbd5e1", "size": 14}
            },
            "bar": {"color": color, "thickness": 0.45},
            "bgcolor": "rgba(0,0,0,0)",
            "borderwidth": 0,
            "steps": [
                {"range": [0, 4.0], "color": "#ed2424"},
                {"range": [4.0, 6.0], "color": "#ec761c"},
                {"range": [6.0, 7.5], "color": "#eaea55"},
                {"range": [7.5, 9.0], "color": "#28AF5C"},
                {"range": [9.0, 10], "color": "#4888c8"},
            ],
            "threshold": {
                "line": {"color": "white", "width": 5},
                "thickness": 0.8,
                "value": calificacion
            }
        }
    ))
    fig.update_layout(
        title={
            "text": "Última calificación anual",
            "y": 0.99,
            "x": 0.5,
            "xanchor": "center",
            "yanchor": "top",
            "font": {"size": 28}
        },
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"color": "white", "family": "Roboto"},
        margin=dict(l=20, r=20, t=70, b=20),
        height=320
    )
    return fig


def calificometro():
    return gauge_calificacion(reglas.ultima_calificacion_anual(df_lista, umbrales.umbrales_anuales))

# Estado de resultados más reciente


def crecimiento_bruto(df):
    df = df.copy()
    df["crecimiento_ben_bruto"] = (
        df["beneficio_bruto"] - df["beneficio_bruto"].shift(1)) / df["beneficio_bruto"].shift(1).replace(0, np.nan)
    return df


def crear_figura_estado_resultados(df_anual):
    df_crec = metricas.crecimiento_anual(df_anual)
    df_bruto = crecimiento_bruto(df_anual)
    df_crec["crecimiento_ben_bruto"] = df_bruto["crecimiento_ben_bruto"]
    columnas_crecimiento = [
        "crecimiento_ingresos",
        "crecimiento_ben_bruto",
        "crecimiento_ebit",
        "crecimiento_utilidad"
    ]
    lista_crecimiento = df_crec[columnas_crecimiento].to_numpy().tolist()[-1]
    periodo_previo = df_anual["periodo_anual"].to_list()[-2]

    def fmt_pct(x):
        color = "#22c55e" if x >= 0 else "#ef4444"
        signo = "+" if x >= 0 else ""
        return f"<span style='color:{color}'>{signo}{x*100:.2f}%</span>"
    texto_crecimiento = (
        f"Crecimiento respecto al {periodo_previo}<br>"
        f"Ingresos totales: {lista_crecimiento[0]*100:.2f}%<br>"
        f"Beneficio Bruto: {lista_crecimiento[1]*100:.2f}%<br>"
        f"Beneficio Operativo: {lista_crecimiento[2]*100:.2f}%<br>"
        f"Beneficio Neto: {lista_crecimiento[3]*100:.2f}%"
    )
    df_est_resultados = df_anual[[
        "ingresos_totales",
        "coste_de_bienes_vendidos",
        "beneficio_bruto",
        "gastos_operativos",
        "EBIT",
        "gastos_financieros",
        "otros_gastos",
        "beneficios_antes_de_impuestos",
        "impuestos_sobre_beneficios",
        "beneficio_neto"
    ]].copy()
    fila = df_est_resultados.iloc[-1]
    fig = go.Figure(
        go.Waterfall(
            orientation="v",
            measure=[
                "relative",
                "relative",
                "total",
                "relative",
                "total",
                "relative",
                "relative",
                "total",
                "relative",
                "total"
            ],
            x=[
                "Ingresos",
                "Coste de bienes",
                "Beneficio bruto",
                "Gastos G&A",
                "EBIT",
                "Gastos financieros",
                "Otros gastos",
                "Antes de impuestos",
                "Impuestos",
                "Beneficio neto"
            ],
            y=[
                fila["ingresos_totales"],
                -fila["coste_de_bienes_vendidos"],
                0,
                -fila["gastos_operativos"],
                0,
                -fila["gastos_financieros"],
                -fila["otros_gastos"],
                0,
                -fila["impuestos_sobre_beneficios"],
                0
            ],
            connector={"line": {"color": "#cbd5e1", "width": 1.5}},
            increasing={"marker": {"color": "#16a34a"}},   # verde serio
            decreasing={"marker": {"color": "#dc2626"}},   # rojo serio
            totals={"marker": {"color": "#1e55a2"}},       # gris institucional
            textposition="outside"
        )
    )

    fig.add_annotation(
        text=texto_crecimiento,
        x=1,
        y=1,
        xref="paper",
        yref="paper",
        xanchor="right",
        yanchor="top",
        showarrow=False,
        align="left",
        bordercolor="white",
        borderwidth=1,
        borderpad=8,
        bgcolor="rgba(15,23,42,0.92)",
        font=dict(size=14, color="#e5e7eb")
    )
    fig.update_layout(
        title=dict(
            text=f"Estado de resultados - {df_anual['periodo_anual'].to_list()[-1]}",
            font=dict(size=30, color="#f1f5f9")
        ),
        yaxis_title="Millones de MXN",
        showlegend=False,
        paper_bgcolor="#0B0F20",
        plot_bgcolor="#0B0F20",
        font=dict(color="#e5e7eb"),
        margin=dict(l=40, r=40, t=70, b=40)
    )
    fig.update_xaxes(
        showgrid=False,
        tickfont=dict(size=12, color="#e5e7eb")
    )
    fig.update_yaxes(
        showgrid=True,
        gridcolor="rgba(148,163,184,0.18)",
        zeroline=False,
        tickfont=dict(size=12, color="#cbd5e1"),
        title_font=dict(size=14, color="#e5e7eb")
    )
    return fig


def ultimo_estado_de_resultados_anual():
    return crear_figura_estado_resultados(df_anual)
# Balance general más reciente


def crear_figura_bal_gral(df):
    df = df.copy()
    df_nuevo = df.loc[:, ['periodo_anual', 'activos_corrientes', 'activos_no_corrientes', 'pasivos_corrientes',
                          'pasivos_no_corrientes', 'activos_totales', 'pasivos_totales', 'patrimonio_neto']]
    df_bal_gral = df_nuevo.iloc[-1]
    act_corr = df_bal_gral['activos_corrientes']
    act_no_corr = df_bal_gral['activos_no_corrientes']
    pas_corr = df_bal_gral['pasivos_corrientes']
    pas_no_corr = df_bal_gral['pasivos_no_corrientes']
    patrimonio = df_bal_gral['patrimonio_neto']
    periodo = df_bal_gral['periodo_anual']
    crec_activos = 100 * ((df_nuevo['activos_totales']-df_nuevo['activos_totales'].shift(1)
                           )/df_nuevo['activos_totales'].shift(1).replace(0, np.nan)).iloc[-1]
    crec_pasivos = 100 * ((df_nuevo['pasivos_totales']-df_nuevo['pasivos_totales'].shift(1)
                           )/df_nuevo['pasivos_totales'].shift(1).replace(0, np.nan)).iloc[-1]
    crec_patrimonio = 100 * ((df_nuevo['patrimonio_neto']-df_nuevo['patrimonio_neto'].shift(1)
                              )/df_nuevo['patrimonio_neto'].shift(1).replace(0, np.nan)).iloc[-1]

    def fmt(x):
        return f"${x:,.0f}"

    def fmt_pct(x):
        if pd.isna(x):
            return "N/D"
        return f"{x:+.2f}%"
    texto_cuadro = (
        f"Crecimiento vs {df["periodo_anual"].to_list()[-2]}<br>"
        f"Activos totales: {fmt_pct(crec_activos)}<br>"
        f"Pasivos totales: {fmt_pct(crec_pasivos)}<br>"
        f"Patrimonio neto: {fmt_pct(crec_patrimonio)}"
    )
    fig = go.Figure()
    fig.add_bar(x=["Activos"], y=[act_corr], name="Activos Corrientes", text=[
                fmt(act_corr)], textposition="inside")
    fig.add_bar(x=["Activos"], y=[act_no_corr], name="Activos No Corrientes", text=[
                fmt(act_no_corr)], textposition="inside")
    fig.add_bar(x=["Pasivos + Patrimonio"],
                y=[pas_corr], name="Pasivos Corrientes", text=[fmt(pas_corr)],
                textposition="inside")
    fig.add_bar(x=["Pasivos + Patrimonio"], y=[pas_no_corr],
                name="Pasivos No Corrientes", text=[fmt(pas_no_corr)],
                textposition="inside")
    fig.add_bar(x=["Pasivos + Patrimonio"],
                y=[patrimonio], name="Patrimonio Neto", text=[fmt(patrimonio)],
                textposition="inside")
    fig.update_layout(barmode="stack", title=f"Balance general - {periodo}",
                      yaxis_title="Monto en MXN", xaxis_title="", template="plotly_white", margin=dict(r=220)
                      )
    fig.add_annotation(x=1.05, y=0.35, xref="paper", yref="paper", text=texto_cuadro, showarrow=False, align="left",
                       xanchor="left", yanchor="top", bordercolor="black", borderwidth=1, borderpad=8, bgcolor="black",
                       font=dict(size=14))
    return fig


def ultimo_balance_general_anual():
    return crear_figura_bal_gral(df_anual)
# Flujo de efectivo más reciente


def crear_flujo_efect_anual(df):
    df = df.copy()
    df_fcf = df.loc[:, ['periodo_anual', 'depreciacion_y_amortizacion', 'flujo_de_efectivo_operativo',
                        'flujo_de_efectivo_inversion', 'capex', 'flujo_de_efectivo_financiamiento',
                        'dividendos_pagados', 'dividendo_emitido', 'pagos_de_deuda',
                        'flujo_de_efectivo']]
    ultimo_periodo = df_fcf['periodo_anual'].iloc[-1]
    conceptos = ['flujo_de_efectivo_operativo', 'depreciacion_y_amortizacion',
                 'flujo_de_efectivo_inversion', 'capex', 'flujo_de_efectivo_financiamiento',
                 'dividendos_pagados', 'pagos_de_deuda', 'flujo_de_efectivo']
    valores = df_fcf[conceptos].iloc[-1].to_numpy().tolist()
    etiquetas_mapeo = {
        'flujo_de_efectivo_operativo': 'Flujo operativo',
        'depreciacion_y_amortizacion': 'D&A',
        'flujo_de_efectivo_inversion': 'Flujo por inversión',
        'capex': 'CapEx',
        'flujo_de_efectivo_financiamiento': 'Flujo por financiamiento',
        'dividendos_pagados': 'Dividendos',
        'pagos_de_deuda': 'Deuda',
        'flujo_de_efectivo': 'Flujo Neto'
    }
    etiquetas = [etiquetas_mapeo[c] for c in conceptos]
    colores = ['green' if v > 0 else 'red' for v in valores]
    fig = go.Figure()
    fig.add_trace(go.Bar(x=etiquetas, y=valores, marker_color=colores, text=valores,
                         hovertext=conceptos, hovertemplate='%{hovertext}<br>%{y}'))
    fig.update_layout(title=f'Flujo de Efectivo {ultimo_periodo}', yaxis_title='Monto en Mxn',
                      template='plotly_white', xaxis_tickangle=30)
    return fig


def ultimo_fcf_anual():
    return crear_flujo_efect_anual(df_anual)
# Gráfica de radar de desempeño


def creador_radar(df, umbral):
    valores = []
    for i in df:
        valores.append(reglas.creador_dataframes(
            i, umbral).loc[-2:, "Calificacion_normalizada"].to_list()[-1])
    claves = ["Calidad del negocio", "Crecimiento", "Solidez",
              "Estructura de deuda", "Pago sostenible de dividendo"]
    fig = go.Figure()
    categorias_cerradas = claves + [claves[0]]
    valores_cerrados = valores + [valores[0]]
    fig.add_trace(go.Scatterpolar(r=valores_cerrados, theta=categorias_cerradas, fill="toself",
                                  line=dict(color="#3B82F6", width=3), fillcolor="rgba(59, 130, 246, 0.35)",
                                  marker=dict(size=7, color="#3B82F6")))
    fig.update_layout(title=dict(text=f"Desempeño anual del {df_anual['periodo_anual'].iloc[-1]}",
                                 x=0.5, xanchor="center", font=dict(size=22)),
                      polar=dict(radialaxis=dict(visible=True, range=[0, 10], tickvals=[2, 4, 6, 8, 10],
                                                 tickfont=dict(size=11, color="black"),                                                  gridcolor="rgba(0,0,0,0.15)",
                                                 linecolor="rgba(0,0,0,0.25)"),
                                 angularaxis=dict(tickfont=dict(size=15, color="white"), linecolor="rgba(0,0,0,0.25)",
                                                  gridcolor="rgba(0,0,0,0.10)")), showlegend=False)
    return fig


def radar():
    return creador_radar(df_lista, umbrales.umbrales_anuales)

# Ahora si, van las tendencias anuales
# Grafica de estados de resultados de los últimos 10 años


def grafica_estados_resultados_10a(df):
    df = df.copy()
    columnas = ["periodo_anual", "ingresos_totales",
                "beneficio_bruto", "EBIT", "beneficio_neto"]
    df = df[columnas].dropna(subset=["periodo_anual"]).copy()
    df = df.sort_values("periodo_anual").reset_index(drop=True)
    if len(df) > 10:
        df_10 = df.copy()
    else:
        df_10 = df.copy()
    df_10["periodo_anual"] = df_10["periodo_anual"].astype(str)

    def calcular_cagr(serie):
        serie = serie.dropna()
        if len(serie) < 2:
            return np.nan
        valor_inicial = serie.iloc[0]
        valor_final = serie.iloc[-1]
        n_periodos = len(serie) - 1
        if valor_inicial <= 0 or valor_final <= 0 or n_periodos <= 0:
            return np.nan
        return (valor_final / valor_inicial) ** (1 / n_periodos) - 1
    cagr_ingresos = calcular_cagr(df_10["ingresos_totales"])
    cagr_bruto = calcular_cagr(df_10["beneficio_bruto"])
    cagr_ebit = calcular_cagr(df_10["EBIT"])
    cagr_neto = calcular_cagr(df_10["beneficio_neto"])

    def fmt_cagr(x):
        return "N/D" if pd.isna(x) else f"{x*100:.2f}%"
    texto_cagr = (
        "CAGR últimos 10 años<br>"
        f"Ingresos: {fmt_cagr(cagr_ingresos)}<br>"
        f"Beneficio bruto: {fmt_cagr(cagr_bruto)}<br>"
        f"Beneficio operativo: {fmt_cagr(cagr_ebit)}<br>"
        f"Beneficio neto: {fmt_cagr(cagr_neto)}")
    fig = go.Figure()
    fig.add_trace(go.Bar(x=df_10["periodo_anual"], y=df_10["ingresos_totales"], name="Ingresos totales",
                         yaxis="y"))
    fig.add_trace(go.Scatter(x=df_10["periodo_anual"], y=df_10["beneficio_bruto"], mode="lines+markers",
                             name="Beneficio bruto", yaxis="y"))
    fig.add_trace(go.Scatter(x=df_10["periodo_anual"], y=df_10["EBIT"], mode="lines+markers",
                             name="Beneficio operativo", yaxis="y"))
    fig.add_trace(go.Scatter(x=df_10["periodo_anual"], y=df_10["beneficio_neto"], mode="lines+markers",
                             name="Beneficio neto", yaxis="y"))
    fig.update_layout(title="Ingresos totales vs beneficios y rentabilidad operativa de los últimos 10 años",
                      xaxis_title="Año",
                      yaxis_title="Pesos mexicanos", barmode="overlay", template="plotly_white",
                      width=1200, height=650, legend=dict(orientation="h", yanchor="bottom",
                                                          y=1.02, xanchor="left", x=0),
                      margin=dict(l=80, r=260, t=100, b=70), annotations=[dict(x=0.02, y=1.0, xref="paper",
                                                                               yref="paper", text=texto_cagr,
                                                                               showarrow=False, align="left",
                                                                               bordercolor="white",
                                                                               borderwidth=1,
                                                                               borderpad=8, bgcolor="black",
                                                                               font=dict(size=12))])
    fig.update_yaxes(tickformat=",.0f")
    return fig


def estados_resultados_10a():
    return grafica_estados_resultados_10a(df_anual)

# Grafica de balance general de los últimos 10 años


def grafica_balance_general_10a(df):
    df = df.copy()
    columnas = ["periodo_anual", "activos_totales",
                "pasivos_totales", "patrimonio_neto"]
    df = df[columnas].dropna().sort_values("periodo_anual")
    if len(df) > 10:
        df_10 = df.tail(10).copy()
    else:
        df_10 = df.copy()
    df_10["periodo_anual"] = df_10["periodo_anual"].astype(str)

    def calcular_cagr(serie):
        serie = serie.dropna()
        if len(serie) < 2:
            return np.nan
        vi = serie.iloc[0]
        vf = serie.iloc[-1]
        n = len(serie) - 1
        if vi <= 0 or vf <= 0:
            return np.nan
        return (vf / vi) ** (1/n) - 1
    cagr_activos = calcular_cagr(df_10["activos_totales"])
    cagr_pasivos = calcular_cagr(df_10["pasivos_totales"])
    cagr_patrimonio = calcular_cagr(df_10["patrimonio_neto"])

    def fmt(x):
        return "N/D" if pd.isna(x) else f"{x*100:.2f}%"
    texto = (
        "CAGR últimos 10 años<br>"
        f"Activos: {fmt(cagr_activos)}<br>"
        f"Pasivos: {fmt(cagr_pasivos)}<br>"
        f"Patrimonio: {fmt(cagr_patrimonio)}")
    fig = go.Figure()
    fig.add_trace(go.Bar(x=df_10["periodo_anual"],
                  y=df_10["pasivos_totales"], name="Pasivos"))
    fig.add_trace(go.Bar(x=df_10["periodo_anual"],
                  y=df_10["patrimonio_neto"], name="Patrimonio"))
    fig.add_trace(go.Scatter(x=df_10["periodo_anual"], y=df_10["activos_totales"], mode="lines+markers",
                             name="Activos totales"))
    fig.update_layout(title="Balance general: crecimiento y estructura de los últimos 10 años", xaxis_title="Año",
                      yaxis_title="Pesos mexicanos", barmode="stack", template="plotly_white",
                      width=1200, height=650, margin=dict(l=80, r=260, t=100, b=70),
                      annotations=[dict(x=0.02, y=1.02, xref="paper", yref="paper", text=texto, showarrow=False,
                                        align="left", bordercolor="white", borderwidth=1, borderpad=8,
                                        bgcolor="black")])
    fig.update_yaxes(tickformat=",.0f")
    return fig


def balance_general_10a():
    return grafica_balance_general_10a(df_anual)


# Gráfica flujo de efectivo de los últimos 10 años

def flujo_efectivo_10a(df):
    df = df.copy()
    columnas = ["periodo_anual", "flujo_de_efectivo_operativo", "capex", "flujo_de_efectivo",
                "beneficio_neto", "dividendos_pagados", "ingresos_totales"]
    df = df[columnas].dropna(subset=["periodo_anual"]
                             ).sort_values("periodo_anual")
    if len(df) > 10:
        df = df.tail(10).copy()
    df["periodo_anual"] = df["periodo_anual"].astype(str)

    def calcular_cagr(serie):
        serie = serie.dropna()
        if len(serie) < 2:
            return np.nan
        vi = serie.iloc[0]
        vf = serie.iloc[-1]
        n = len(serie) - 1
        if vi <= 0 or vf <= 0:
            return np.nan
        return (vf / vi) ** (1 / n) - 1
    cagr_cfo = calcular_cagr(df["flujo_de_efectivo_operativo"])
    cagr_fcf = calcular_cagr(df["flujo_de_efectivo"]
                             [df["flujo_de_efectivo"] > 0])

    def fmt_pct(x):
        return "N/D" if pd.isna(x) else f"{x*100:.2f}%"

    def fmt_ratio(x):
        return "N/D" if pd.isna(x) else f"{x:.2f}x"
    texto = (
        "Resumen 10 años<br>"
        f"CAGR flujo operativo: {fmt_pct(cagr_cfo)}<br>"
        f"CAGR flujo neto: {fmt_pct(cagr_fcf)}<br>")
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df["periodo_anual"], y=df["flujo_de_efectivo_operativo"], name="Flujo operativo"))
    fig.add_trace(go.Bar(x=df["periodo_anual"], y=-
                  df["capex"].abs(), name="CAPEX"))
    fig.add_trace(go.Scatter(x=df["periodo_anual"], y=df["flujo_de_efectivo"], mode="lines+markers",
                             name="Flujo neto de efectivo"))
    fig.update_layout(title=dict(text="Flujo de efectivo: tendencias clave de los últimos 10 años",
                                 y=0.95, x=0.02, xanchor="left"),
                      template="plotly_white", width=1450, height=700, barmode="group", margin=dict(l=80, r=160, t=140, b=110),
                      legend=dict(orientation="h", yanchor="top",
                                  y=1.02, xanchor="left", x=0),
                      annotations=[dict(x=0.05, y=0.95, xref="paper", yref="paper", text=texto, showarrow=False,
                                        align="left", bordercolor="white", borderwidth=1, borderpad=8,
                                        bgcolor="black", font=dict(size=12))])
    fig.update_yaxes(title_text="Pesos mexicanos", tickformat=",.0f")
    return fig


def fcf_10a():
    return flujo_efectivo_10a(df_anual)

# Gráfica ROIC - WACC


def df_nuevo(df):
    df = df.copy()
    df["tasa_impositiva"] = df["impuestos_sobre_beneficios"] / \
        df["beneficios_antes_de_impuestos"].replace(0, np.nan)
    df["roic"] = (df["EBIT"] * (1 - df["tasa_impositiva"])) / \
        (df["patrimonio_neto"] - df["deuda_total"]).replace(0, np.nan)
    df["market_cap"] = df["cotizacion"] * df["acciones_totales"]
    df["costo_capital"] = df["tasa_libre_de_riesgo"] + \
        (df["beta_de_la_accion"].replace(0, np.nan)
         * df["prima_de_riesgo"].replace(0, np.nan))
    df["costo_deuda"] = df["intereses_pagados"] / \
        df["deuda_total"].replace(0, np.nan)
    df["wacc01"] = (df["market_cap"]/((df["market_cap"] +
                    df["deuda_total"])).replace(0, np.nan) * df["costo_capital"]).replace(0, np.nan)
    df["wacc02"] = (df["deuda_total"]/(df["market_cap"]+df["deuda_total"]).replace(0, np.nan)
                    ) * df["costo_deuda"] * df["tasa_impositiva"]
    df["wacc"] = df["wacc01"] + df["wacc02"]
    df["roic - wacc"] = df["roic"] - df["wacc"]
    return df


def roic_wacc_creador(df):
    df = df.copy()
    x = df["periodo_anual"]
    roic = df["roic"]
    wacc = df["wacc"]
    spread = df["roic - wacc"]
    colores_spread = np.where(
        spread >= 0, "rgba(46, 204, 113, 0.55)", "rgba(231, 76, 60, 0.55)")
    fig = go.Figure()
    fig.add_trace(go.Bar(x=x, y=spread, name="Spread ROIC - WACC", marker_color=colores_spread,
                         yaxis="y1", hovertemplate=("Periodo: %{x}<br>""Spread: %{y:.2f} pp<br>""<extra></extra>")))
    fig.add_trace(go.Scatter(x=x, y=roic, name="ROIC", mode="lines+markers", line=dict(width=3, color="#3fa7ff"),
                             marker=dict(size=8), yaxis="y2", hovertemplate=("Periodo: %{x}<br>""ROIC: %{y:.2f}%<br>"
                                                                             "<extra></extra>")))
    fig.add_trace(go.Scatter(x=x, y=wacc, name="WACC", mode="lines+markers", line=dict(width=3, dash="dot", color="#bfbfbf"),
                             marker=dict(size=8), yaxis="y2", hovertemplate=("Periodo: %{x}<br>""WACC: %{y:.2f}%<br>"
                                                                             "<extra></extra>")))
    fig.add_hline(y=0, line_width=1.2, line_dash="dash", line_color="gray")
    max_y2 = max(roic.max(), wacc.max())
    min_y2 = min(roic.min(), wacc.min())
    fig.update_layout(title=dict(text="Spread de creación de valor: ROIC vs WACC de los últimos 10 años",
                                 x=0.01, xanchor="left"),
                      template="plotly_dark", barmode="relative", height=500, width=1100, hovermode="x unified",
                      legend=dict(orientation="h", y=1.10, x=0.01), margin=dict(t=90, b=70, l=70, r=70),
                      yaxis=dict(title="Spread (pp)", side="left", zeroline=False), yaxis2=dict(title="ROIC / WACC (%)",
                                                                                                overlaying="y", side="right",
                                                                                                zeroline=False,
                                                                                                range=[min_y2 * 0.8,
                                                                                                       max_y2 * 1.1]))
    fig.add_annotation(x=0.98, y=1.09, xref="paper", yref="paper", text="🔴 < 0%<br>🟡 0% – 5%<br>🟢 > 5%",
                       showarrow=False, align="left", font=dict(size=12), bordercolor="gray", borderwidth=1,
                       borderpad=6, bgcolor="rgba(0,0,0,0.6)")
    return fig


def roic_menos_wacc():
    return roic_wacc_creador(df_nuevo(df_anual))

# Gráfica valor económico agregado EVA


def graf_val_econ_agregado(df):
    x = df["periodo_anual"]
    cap_invertido = (df["patrimonio_neto"] -
                     df["deuda_total"]).replace(0, np.nan)
    roic_wacc = df["roic - wacc"]
    eva = (cap_invertido * roic_wacc).replace(0,
                                              np.nan)  # economic value added
    inflacion = df["inflacion"]
    colores_eva = np.where(
        eva >= 0, "rgba(66, 153, 225, 0.9)", "rgba(237, 125, 49, 0.9)")
    fig = go.Figure()
    fig.add_trace(go.Bar(x=x, y=eva, name="EVA (MXN bn)", marker_color=colores_eva, yaxis="y1",
                         hovertemplate="Periodo: %{x}<br>EVA: %{y:.2f} bn<extra></extra>"))
    fig.add_trace(go.Scatter(x=x, y=inflacion, name="Inflación %", mode="lines+markers",
                             line=dict(color="#ff6b35", width=2.5), marker=dict(size=7),
                             yaxis="y2", hovertemplate="Periodo: %{x}<br>Inflación: %{y:.2f}%<extra></extra>"))
    fig.add_hline(y=0, line_width=1, line_dash="dash", line_color="gray")
    max_inf = inflacion.max()
    min_inf = inflacion.min()
    fig.update_layout(template="plotly_dark", height=550, width=1100, hovermode="x unified",
                      title="Valor económico (EVA) agregado de los últimos 10 años",
                      legend=dict(orientation="h", y=1.1, x=0.01), margin=dict(t=90, b=60, l=70, r=80),
                      xaxis=dict(title="Periodo"),
                      yaxis=dict(title="EVA (MXN bn)",
                                 side="left", zeroline=False),
                      yaxis2=dict(title="Inflación (%)", overlaying="y", side="right",
                                  position=1.0, range=[min_inf * 0.9, max_inf * 1.1]))
    return fig


def val_econ_agregado():
    return graf_val_econ_agregado(df_nuevo(df_anual))

# Gráfica con calificaciones por métricas en los últimos 10 años


def graf_calificaciones_anuales(df, umbral):
    calificaciones = []
    metricas = ["Calidad del negocio", "Crecimiento",
                "Solidez", "Estructura", "Dividendo"]
    for i in df:
        calificaciones.append(reglas.creador_dataframes(
            i, umbral).tail(10).iloc[:, -1].to_numpy().tolist())
    diccionario = dict(zip(metricas, calificaciones))
    periodo = df_anual["periodo_anual"].tail(10)
    fig = go.Figure()
    for i, j in diccionario.items():
        fig.add_trace(go.Scatter(x=periodo, y=j, mode="lines", name=i))
    fig.update_layout(title="Métricas de los últimos 10 años", xaxis_title="Años", yaxis_title="Calificación",
                      template="plotly_white", hovermode="x unified")
    return fig


def calificaciones_anuales():
    return graf_calificaciones_anuales(df_lista, umbrales.umbrales_anuales)
