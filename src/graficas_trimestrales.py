from pathlib import Path
from PIL import Image
from datos import umbrales
from plotly.subplots import make_subplots
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
femsa_trim = RUTA_DATOS/'femsa_trimestral.csv'


def cargar_datos(df):
    df_cargado = pd.read_csv(df)
    return df_cargado.tail(20)


df_trim = cargar_datos(femsa_trim)
df_lista_trim = [metricas.crecimiento_operativo_df(df_trim), metricas.rentabilidad_operativa_df(df_trim),
                 metricas.eficiencia_control_costos_df(df_trim),
                 metricas.solidez_financiera_corto_plazo_df(df_trim),
                 metricas.momentum_financiero_df(df_trim),
                 metricas.performance_por_unidad_negocio_df(df_trim)]


# Gráfica de calificación trimestral


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


def gauge_calificacion(calificacion, titulo="Última calificación trimestral"):
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
            "text": "Última calificación trimestral",
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


def calificometro_trim():
    return gauge_calificacion(reglas.ultima_calificacion_trimestral(df_lista_trim, umbrales.umbrales_trimestrales))

# Estado de resultados trimestral más reciente


def crecimiento_bruto_trim(df):
    df = df.copy()
    df["crecimiento_ben_bruto"] = (
        df["beneficio_bruto"] - df["beneficio_bruto"].shift(1)
    ) / df["beneficio_bruto"].shift(1).replace(0, np.nan)
    return df


def crecimiento_ticket_trim(df):
    df = df.copy()
    df["crecimiento_ticket_promedio"] = (
        df["ticket_promedio"] - df["ticket_promedio"].shift(1)
    ) / df["ticket_promedio"].shift(1).replace(0, np.nan)
    return df


def crecimiento_trafico_trim(df):
    df = df.copy()
    df["crecimiento_trafico"] = (
        df["trafico_transacciones"] - df["trafico_transacciones"].shift(1)
    ) / df["trafico_transacciones"].shift(1).replace(0, np.nan)
    return df


def crecimiento_ingresos_trim(df):
    df = df.copy()
    df["crecimiento_ingresos"] = (
        df["ingresos"] - df["ingresos"].shift(1)
    ) / df["ingresos"].shift(1).replace(0, np.nan)
    return df


def crecimiento_ebit_trim(df):
    df = df.copy()
    df["crecimiento_ebit"] = (
        df["ebit"] - df["ebit"].shift(1)
    ) / df["ebit"].shift(1).replace(0, np.nan)
    return df


def crear_figura_estado_resultados_trim(df_trim):
    df_ingresos = crecimiento_ingresos_trim(df_trim)
    df_bruto = crecimiento_bruto_trim(df_trim)
    df_ebit = crecimiento_ebit_trim(df_trim)
    df_ticket = crecimiento_ticket_trim(df_trim)
    df_trafico = crecimiento_trafico_trim(df_trim)

    columnas_crecimiento = [
        "crecimiento_ingresos",
        "crecimiento_ben_bruto",
        "crecimiento_ebit",
        "crecimiento_ticket_promedio",
        "crecimiento_trafico"
    ]

    df_crec = pd.DataFrame({
        "crecimiento_ingresos": df_ingresos["crecimiento_ingresos"],
        "crecimiento_ben_bruto": df_bruto["crecimiento_ben_bruto"],
        "crecimiento_ebit": df_ebit["crecimiento_ebit"],
        "crecimiento_ticket_promedio": df_ticket["crecimiento_ticket_promedio"],
        "crecimiento_trafico": df_trafico["crecimiento_trafico"]
    })

    lista_crecimiento = df_crec[columnas_crecimiento].to_numpy().tolist()[-1]
    trimestre_previo = df_trim["trimestre"].to_list()[-2]

    texto_crecimiento = (
        f"Crecimiento respecto a {trimestre_previo}<br>"
        f"Ingresos: {lista_crecimiento[0]*100:.2f}%<br>"
        f"Beneficio Bruto: {lista_crecimiento[1]*100:.2f}%<br>"
        f"EBIT: {lista_crecimiento[2]*100:.2f}%<br>"
        f"Ticket promedio: {lista_crecimiento[3]*100:.2f}%<br>"
        f"Tráfico: {lista_crecimiento[4]*100:.2f}%"
    )

    df_est_resultados_trim = df_trim[[
        "ingresos",
        "coste_ventas",
        "beneficio_bruto",
        "gastos_operativos",
        "ebit",
        "gastos_financieros",
        "otros_gastos",
        "beneficios_antes_de_impuestos",
        "impuestos_sobre_beneficios",
        "beneficio_neto"
    ]].copy()

    fila = df_est_resultados_trim.iloc[-1]

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
                "Coste de ventas",
                "Beneficio bruto",
                "Gastos operativos",
                "EBIT",
                "Gastos financieros",
                "Otros gastos",
                "Antes de impuestos",
                "Impuestos",
                "Beneficio neto"
            ],
            y=[
                fila["ingresos"],
                -fila["coste_ventas"],
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
            increasing={"marker": {"color": "#16a34a"}},
            decreasing={"marker": {"color": "#dc2626"}},
            totals={"marker": {"color": "#1e55a2"}},
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
            text=f"Estado de resultados del trimestre - {df_trim['trimestre'].to_list()[-1]}",
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


def ultimo_estado_de_resultados_trimestral():
    return crear_figura_estado_resultados_trim(df_trim)

# Balance general trimestral más reciente


def crear_figura_bal_gral_trim(df):
    df = df.copy()
    df_nuevo = df.loc[:, [
        'trimestre',
        'activos_corrientes',
        'activos_no_corrientes',
        'pasivos_corrientes',
        'pasivos_no_corrientes',
        'activos_totales',
        'pasivos_totales',
        'patrimonio_neto'
    ]]

    df_bal_gral = df_nuevo.iloc[-1]

    act_corr = df_bal_gral['activos_corrientes']
    act_no_corr = df_bal_gral['activos_no_corrientes']
    pas_corr = df_bal_gral['pasivos_corrientes']
    pas_no_corr = df_bal_gral['pasivos_no_corrientes']
    patrimonio = df_bal_gral['patrimonio_neto']
    periodo = df_bal_gral['trimestre']

    crec_activos = 100 * (
        (df_nuevo['activos_totales'] - df_nuevo['activos_totales'].shift(4)) /
        df_nuevo['activos_totales'].shift(4).replace(0, np.nan)
    ).iloc[-1]

    crec_pasivos = 100 * (
        (df_nuevo['pasivos_totales'] - df_nuevo['pasivos_totales'].shift(4)) /
        df_nuevo['pasivos_totales'].shift(4).replace(0, np.nan)
    ).iloc[-1]

    crec_patrimonio = 100 * (
        (df_nuevo['patrimonio_neto'] - df_nuevo['patrimonio_neto'].shift(4)) /
        df_nuevo['patrimonio_neto'].shift(4).replace(0, np.nan)
    ).iloc[-1]

    def fmt(x):
        return f"${x:,.0f}"

    def fmt_pct(x):
        if pd.isna(x):
            return "N/D"
        return f"{x:+.2f}%"

    texto_cuadro = (
        f"Crecimiento vs {df['trimestre'].to_list()[-5]}<br>"
        f"Activos totales: {fmt_pct(crec_activos)}<br>"
        f"Pasivos totales: {fmt_pct(crec_pasivos)}<br>"
        f"Patrimonio neto: {fmt_pct(crec_patrimonio)}"
    )

    fig = go.Figure()

    fig.add_bar(
        x=["Activos"],
        y=[act_corr],
        name="Activos Corrientes",
        text=[fmt(act_corr)],
        textposition="inside"
    )

    fig.add_bar(
        x=["Activos"],
        y=[act_no_corr],
        name="Activos No Corrientes",
        text=[fmt(act_no_corr)],
        textposition="inside"
    )

    fig.add_bar(
        x=["Pasivos + Patrimonio"],
        y=[pas_corr],
        name="Pasivos Corrientes",
        text=[fmt(pas_corr)],
        textposition="inside"
    )

    fig.add_bar(
        x=["Pasivos + Patrimonio"],
        y=[pas_no_corr],
        name="Pasivos No Corrientes",
        text=[fmt(pas_no_corr)],
        textposition="inside"
    )

    fig.add_bar(
        x=["Pasivos + Patrimonio"],
        y=[patrimonio],
        name="Patrimonio Neto",
        text=[fmt(patrimonio)],
        textposition="inside"
    )

    fig.update_layout(
        barmode="stack",
        title=f"Balance general del trimestre - {periodo}",
        yaxis_title="Monto en MXN",
        xaxis_title="",
        template="plotly_white",
        margin=dict(r=220)
    )

    fig.add_annotation(
        x=1.05,
        y=0.35,
        xref="paper",
        yref="paper",
        text=texto_cuadro,
        showarrow=False,
        align="left",
        xanchor="left",
        yanchor="top",
        bordercolor="black",
        borderwidth=1,
        borderpad=8,
        bgcolor="black",
        font=dict(size=14)
    )

    return fig


def ultimo_balance_general_trimestral():
    return crear_figura_bal_gral_trim(df_trim)

# Tiendas totales y usuarios Spin del último trimestre


def crear_figura_tiendas_y_spin_trim(df):
    df = df.copy()
    fila_actual = df.iloc[-1]
    fila_previa_yoy = df.iloc[-5]
    categorias_principales = ["OXXO", "Combustible", "Salud"]
    valores_previos_principales = [
        fila_previa_yoy["oxxo_totales"],
        fila_previa_yoy["combustibles_totales"],
        fila_previa_yoy["salud_totales"]
    ]
    valores_actuales_principales = [
        fila_actual["oxxo_totales"],
        fila_actual["combustibles_totales"],
        fila_actual["salud_totales"]
    ]
    categoria_spin = ["Spin"]
    valor_previo_spin = [fila_previa_yoy["usuarios_spin_totales"]]
    valor_actual_spin = [fila_actual["usuarios_spin_totales"]]
    crecimientos = {
        "OXXO": ((fila_actual["oxxo_totales"] - fila_previa_yoy["oxxo_totales"]) /
                 fila_previa_yoy["oxxo_totales"].replace(0, np.nan) if hasattr(fila_previa_yoy["oxxo_totales"], "replace")
                 else (fila_actual["oxxo_totales"] - fila_previa_yoy["oxxo_totales"]) / fila_previa_yoy["oxxo_totales"]),
        "Combustible": ((fila_actual["combustibles_totales"] - fila_previa_yoy["combustibles_totales"]) /
                        fila_previa_yoy["combustibles_totales"]),
        "Salud": ((fila_actual["salud_totales"] - fila_previa_yoy["salud_totales"]) /
                  fila_previa_yoy["salud_totales"]),
        "Spin": ((fila_actual["usuarios_spin_totales"] - fila_previa_yoy["usuarios_spin_totales"]) /
                 fila_previa_yoy["usuarios_spin_totales"])
    }

    def fmt_pct(x):
        if pd.isna(x):
            return "N/D"
        signo = "+" if x >= 0 else ""
        return f"{signo}{x*100:.2f}%"

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_bar(
        x=categorias_principales,
        y=valores_previos_principales,
        name=f"{fila_previa_yoy['trimestre']}",
        marker_color="#64748b",
        offsetgroup=0,
        text=[f"{v:,.0f}" for v in valores_previos_principales],
        textposition="outside",
        hovertemplate="%{x}<br>Previo: %{y:,.0f}<extra></extra>",
        secondary_y=False
    )

    fig.add_bar(
        x=categorias_principales,
        y=valores_actuales_principales,
        name=f"{fila_actual['trimestre']}",
        marker_color="#2563eb",
        offsetgroup=1,
        text=[f"{v:,.0f}" for v in valores_actuales_principales],
        textposition="outside",
        hovertemplate="%{x}<br>Actual: %{y:,.0f}<extra></extra>",
        secondary_y=False
    )

    fig.add_bar(
        x=categoria_spin,
        y=valor_previo_spin,
        name=f"Spin {fila_previa_yoy['trimestre']}",
        marker_color="#94a3b8",
        offsetgroup=0,
        text=[f"{v:,.1f}" for v in valor_previo_spin],
        textposition="outside",
        hovertemplate="%{x}<br>Previo: %{y:,.1f} M<extra></extra>",
        secondary_y=True,
        showlegend=False
    )

    fig.add_bar(
        x=categoria_spin,
        y=valor_actual_spin,
        name=f"Spin {fila_actual['trimestre']}",
        marker_color="#22c55e",
        offsetgroup=1,
        text=[f"{v:,.1f}" for v in valor_actual_spin],
        textposition="outside",
        hovertemplate="%{x}<br>Actual: %{y:,.1f} M<extra></extra>",
        secondary_y=True,
        showlegend=False
    )
    for idx, (cat, y) in enumerate(zip(categorias_principales, valores_actuales_principales)):
        y_base = max(valores_previos_principales[idx], y)
        if y_base > 10000:
            y_pos = y_base * 1.08
        elif y_base > 1000:
            y_pos = y_base * 1.12
        else:
            y_pos = y_base * 1.25
        fig.add_annotation(
            x=cat,
            y=y_pos,
            text=fmt_pct(crecimientos[cat]),
            showarrow=False,
            font=dict(size=13, color="#e5e7eb"),
            bgcolor="rgba(15,23,42,0.85)",
            bordercolor="white",
            borderwidth=1,
            borderpad=4,
            yref="y"
        )
    fig.add_annotation(
        x="Spin",
        y=max(valor_previo_spin[0], valor_actual_spin[0]) * 1.20,
        text=fmt_pct(crecimientos["Spin"]),
        showarrow=False,
        font=dict(size=13, color="#e5e7eb"),
        bgcolor="rgba(15,23,42,0.85)",
        bordercolor="white",
        borderwidth=1,
        borderpad=4,
        yref="y2"
    )

    fig.update_layout(
        title=dict(
            text=f"Tipos de tiendas y Spin del trimestre - {fila_actual['trimestre']}",
            font=dict(size=26, color="#f1f5f9")
        ),
        barmode="group",
        paper_bgcolor="#0B0F20",
        plot_bgcolor="#0B0F20",
        font=dict(color="#e5e7eb"),
        margin=dict(l=40, r=40, t=80, b=40),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=0
        )
    )

    fig.update_xaxes(
        showgrid=False,
        tickfont=dict(size=12, color="#e5e7eb")
    )

    fig.update_yaxes(
        title_text="Unidades / tiendas",
        showgrid=True,
        gridcolor="rgba(148,163,184,0.18)",
        zeroline=False,
        tickfont=dict(size=12, color="#cbd5e1"),
        secondary_y=False
    )

    fig.update_yaxes(
        title_text="Usuarios Spin (millones)",
        showgrid=False,
        zeroline=False,
        tickfont=dict(size=12, color="#cbd5e1"),
        secondary_y=True
    )

    return fig


def ultima_figura_tiendas_y_spin_trimestral():
    return crear_figura_tiendas_y_spin_trim(df_trim)


def crear_figura_metricas_no_financieras_trim(df):
    df = df.copy()
    fila_actual = df.iloc[-1]
    fila_previa = df.iloc[-5]
    categorias_principales = ["Tráfico", "Ticket promedio"]
    valores_previos_principales = [
        fila_previa["trafico_transacciones"],
        fila_previa["ticket_promedio"]
    ]
    valores_actuales_principales = [
        fila_actual["trafico_transacciones"],
        fila_actual["ticket_promedio"]
    ]
    categoria_secundaria = ["Venta por tienda"]
    valor_previo_secundaria = [fila_previa["venta_por_tienda"]]
    valor_actual_secundaria = [fila_actual["venta_por_tienda"]]
    crecimientos = {
        "Tráfico": ((fila_actual["trafico_transacciones"] - fila_previa["trafico_transacciones"]) /
                    fila_previa["trafico_transacciones"]),
        "Ticket promedio": ((fila_actual["ticket_promedio"] - fila_previa["ticket_promedio"]) /
                            fila_previa["ticket_promedio"]),
        "Venta por tienda": ((fila_actual["venta_por_tienda"] - fila_previa["venta_por_tienda"]) /
                             fila_previa["venta_por_tienda"])
    }

    def fmt_pct(x):
        if pd.isna(x):
            return "N/D"
        signo = "+" if x >= 0 else ""
        return f"{signo}{x*100:.2f}%"
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_bar(
        x=categorias_principales,
        y=valores_previos_principales,
        name=f"{fila_previa['trimestre']}",
        marker_color="#64748b",
        offsetgroup=0,
        text=[f"{v:,.1f}" for v in valores_previos_principales],
        textposition="outside",
        hovertemplate="%{x}<br>Previo: %{y:,.1f}<extra></extra>",
        secondary_y=False
    )
    fig.add_bar(
        x=categorias_principales,
        y=valores_actuales_principales,
        name=f"{fila_actual['trimestre']}",
        marker_color="#f59e0b",
        offsetgroup=1,
        text=[f"{v:,.1f}" for v in valores_actuales_principales],
        textposition="outside",
        hovertemplate="%{x}<br>Actual: %{y:,.1f}<extra></extra>",
        secondary_y=False
    )
    fig.add_bar(
        x=categoria_secundaria,
        y=valor_previo_secundaria,
        name=f"Venta/tienda {fila_previa['trimestre']}",
        marker_color="#94a3b8",
        offsetgroup=0,
        text=[f"{v:,.1f}" for v in valor_previo_secundaria],
        textposition="outside",
        hovertemplate="%{x}<br>Previo: %{y:,.1f}<extra></extra>",
        secondary_y=True,
        showlegend=False
    )
    fig.add_bar(
        x=categoria_secundaria,
        y=valor_actual_secundaria,
        name=f"Venta/tienda {fila_actual['trimestre']}",
        marker_color="#22c55e",
        offsetgroup=1,
        text=[f"{v:,.1f}" for v in valor_actual_secundaria],
        textposition="outside",
        hovertemplate="%{x}<br>Actual: %{y:,.1f}<extra></extra>",
        secondary_y=True,
        showlegend=False
    )
    for cat, y in zip(categorias_principales, valores_actuales_principales):
        fig.add_annotation(
            x=cat,
            y=max(
                valores_previos_principales[categorias_principales.index(cat)], y) * 1.15,
            text=fmt_pct(crecimientos[cat]),
            showarrow=False,
            font=dict(size=13, color="#e5e7eb"),
            bgcolor="rgba(15,23,42,0.85)",
            bordercolor="white",
            borderwidth=1,
            borderpad=4,
            yref="y"
        )
    fig.add_annotation(
        x="Venta por tienda",
        y=max(valor_previo_secundaria[0], valor_actual_secundaria[0]) * 1.08,
        text=fmt_pct(crecimientos["Venta por tienda"]),
        showarrow=False,
        font=dict(size=13, color="#e5e7eb"),
        bgcolor="rgba(15,23,42,0.85)",
        bordercolor="white",
        borderwidth=1,
        borderpad=4,
        yref="y2"
    )
    fig.update_layout(
        title=dict(
            text=f"Otras métricas no financieras del trimestre - {fila_actual['trimestre']}",
            font=dict(size=26, color="#f1f5f9")
        ),
        barmode="group",
        paper_bgcolor="#0B0F20",
        plot_bgcolor="#0B0F20",
        font=dict(color="#e5e7eb"),
        margin=dict(l=40, r=40, t=80, b=40),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=0
        )
    )
    fig.update_xaxes(
        showgrid=False,
        tickfont=dict(size=12, color="#e5e7eb")
    )
    fig.update_yaxes(
        title_text="Tráfico / ticket",
        showgrid=True,
        gridcolor="rgba(148,163,184,0.18)",
        zeroline=False,
        tickfont=dict(size=12, color="#cbd5e1"),
        secondary_y=False
    )
    fig.update_yaxes(
        title_text="Venta por tienda",
        showgrid=False,
        zeroline=False,
        tickfont=dict(size=12, color="#cbd5e1"),
        secondary_y=True
    )
    return fig


def ultimas_metricas_no_financieras_trimestral():
    return crear_figura_metricas_no_financieras_trim(df_trim)

# Gráfica de radar de desempeño trimestral


def creador_radar(df, umbral):
    valores = []
    for i in df:
        valores.append(reglas.creador_dataframes(
            i, umbral).loc[-2:, "Calificacion_normalizada"].to_list()[-1])
    claves = ["Crecimiento operativo", "Rentabilidad operativa", "Eficiencia de costes",
              "Solidez a corto plazo", "Momentum financiero", "Desempeño por unidad de negocio"]
    fig = go.Figure()
    categorias_cerradas = claves + [claves[0]]
    valores_cerrados = valores + [valores[0]]
    fig.add_trace(go.Scatterpolar(r=valores_cerrados, theta=categorias_cerradas, fill="toself",
                                  line=dict(color="#3B82F6", width=3), fillcolor="rgba(59, 130, 246, 0.35)",
                                  marker=dict(size=7, color="#3B82F6")))
    fig.update_layout(title=dict(text=f"Desempeño del trimestre {df_trim['trimestre'].iloc[-1]}",
                                 x=0.5, xanchor="center", font=dict(size=22)),
                      polar=dict(radialaxis=dict(visible=True, range=[0, 10], tickvals=[2, 4, 6, 8, 10],
                                                 tickfont=dict(size=11, color="black"),                                                  gridcolor="rgba(0,0,0,0.15)",
                                                 linecolor="rgba(0,0,0,0.25)"),
                                 angularaxis=dict(tickfont=dict(size=15, color="white"), linecolor="rgba(0,0,0,0.25)",
                                                  gridcolor="rgba(0,0,0,0.10)")), showlegend=False)
    return fig


def radar_trimestral():
    return creador_radar(df_lista_trim, umbrales.umbrales_trimestrales)

# Ahora si, van las tendencias trimestrales
# Grafica de estados de resultados de los últimos 20 trimestres

# Gráfica de estado de resultados trimestral histórico


def grafica_estados_resultados_20trim(df):
    df = df.copy()
    columnas = ["trimestre", "ingresos",
                "beneficio_bruto", "ebit", "beneficio_neto"]
    df = df[columnas].dropna(subset=["trimestre"]).copy()
    df = df.reset_index(drop=True)

    def calcular_cagr(serie):
        serie = serie.dropna()
        if len(serie) < 2:
            return np.nan
        valor_inicial = serie.iloc[0]
        valor_final = serie.iloc[-1]
        n_periodos = len(serie) - 1
        if valor_inicial <= 0 or valor_final <= 0 or n_periodos <= 0:
            return np.nan
        return (valor_final / valor_inicial) ** (4 / n_periodos) - 1
    cagr_ingresos = calcular_cagr(df["ingresos"])
    cagr_bruto = calcular_cagr(df["beneficio_bruto"])
    cagr_ebit = calcular_cagr(df["ebit"])
    cagr_neto = calcular_cagr(df["beneficio_neto"])

    def fmt_cagr(x):
        return "N/D" if pd.isna(x) else f"{x*100:.2f}%"
    texto_cagr = (
        "CAGR del periodo disponible<br>"
        f"Ingresos: {fmt_cagr(cagr_ingresos)}<br>"
        f"Beneficio bruto: {fmt_cagr(cagr_bruto)}<br>"
        f"Beneficio operativo: {fmt_cagr(cagr_ebit)}<br>"
        f"Beneficio neto: {fmt_cagr(cagr_neto)}"
    )
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=df["trimestre"],
            y=df["ingresos"],
            name="Ingresos",
            yaxis="y"
        )
    )
    fig.add_trace(
        go.Scatter(
            x=df["trimestre"],
            y=df["beneficio_bruto"],
            mode="lines+markers",
            name="Beneficio bruto",
            yaxis="y"
        )
    )
    fig.add_trace(
        go.Scatter(
            x=df["trimestre"],
            y=df["ebit"],
            mode="lines+markers",
            name="EBIT",
            yaxis="y"
        )
    )
    fig.add_trace(
        go.Scatter(
            x=df["trimestre"],
            y=df["beneficio_neto"],
            mode="lines+markers",
            name="Beneficio neto",
            yaxis="y"
        )
    )
    fig.update_layout(
        title="Ingresos trimestrales vs beneficios y rentabilidad operativa",
        xaxis_title="Trimestre",
        yaxis_title="Pesos mexicanos",
        barmode="overlay",
        template="plotly_white",
        width=1200,
        height=650,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=0
        ),
        margin=dict(l=80, r=260, t=100, b=70),
        annotations=[
            dict(
                x=1.45,
                y=1.07,
                xref="paper",
                yref="paper",
                text=texto_cagr,
                showarrow=False,
                align="left",
                bordercolor="white",
                borderwidth=1,
                borderpad=8,
                bgcolor="black",
                font=dict(size=12)
            )
        ]
    )
    fig.update_yaxes(tickformat=",.0f")
    return fig


def estados_resultados_20trim():
    return grafica_estados_resultados_20trim(df_trim)

# Tendencia de ingresos trimestrales
# Gráfica de tendencias y su banda de variabilidad


def grafica_con_banda(df, columna, nombre, es_porcentaje=False):
    df = df.copy()
    df = df[["trimestre", columna]].dropna().reset_index(drop=True)
    # tendencia (media móvil 4T)
    df["tendencia"] = df[columna].rolling(window=4, min_periods=1).mean()
    # residuo
    df["residuo"] = df[columna] - df["tendencia"]
    # desviación
    df["desviacion"] = df["residuo"].rolling(window=4, min_periods=1).std()
    df["desviacion"] = df["desviacion"].fillna(0)
    # bandas
    df["banda_superior"] = df["tendencia"] + df["desviacion"]
    df["banda_inferior"] = df["tendencia"] - df["desviacion"]
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["trimestre"],
        y=df["banda_superior"],
        mode="lines",
        line=dict(width=0),
        showlegend=False,
        hoverinfo="skip"
    ))
    fig.add_trace(go.Scatter(
        x=df["trimestre"],
        y=df["banda_inferior"],
        mode="lines",
        line=dict(width=0),
        fill="tonexty",
        fillcolor="rgba(59,130,246,0.15)",
        name="Banda de variabilidad",
        hoverinfo="skip"
    ))
    fig.add_trace(go.Scatter(
        x=df["trimestre"],
        y=df["tendencia"],
        mode="lines",
        name="Tendencia",
        line=dict(width=3, dash="dash")
    ))
    fig.add_trace(go.Scatter(
        x=df["trimestre"],
        y=df[columna],
        mode="lines+markers",
        name=nombre,
        line=dict(width=3)
    ))
    fig.update_layout(
        title=f"{nombre} - tendencia y variabilidad",
        xaxis_title="Trimestre",
        yaxis_title=nombre,
        template="plotly_white",
        width=1100,
        height=550,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=0
        ),
        margin=dict(l=60, r=60, t=80, b=60))
    if es_porcentaje:
        fig.update_yaxes(tickformat=".2%")
    else:
        fig.update_yaxes(tickformat=",.0f")
    return fig


def margen_operativo_tendencia(df):
    df = df.copy()
    df["margen_operativo"] = (
        df["ebit"] / df["ingresos"].replace(0, np.nan)
    )
    return df


def tendencia_trimestral_ingresos():
    return grafica_con_banda(df_trim, "ingresos", "Ingresos")


def tendencia_trimestral_ebit():
    return grafica_con_banda(df_trim, "ebit", "EBIT")


def tendencia_trimestral_margen_operativo():
    return grafica_con_banda(margen_operativo_tendencia(df_trim), "margen_operativo",
                             "Margen operativo", es_porcentaje=True)


def tendencia_trimestral_venta_por_tienda():
    return grafica_con_banda(df_trim, "venta_por_tienda", "Venta por tienda")


def tendencia_trimestral_spin():
    return grafica_con_banda(df_trim, "usuarios_spin_totales", "Usuarios Spin")

# Gráfica de balance general trimestral histórico


def grafica_balance_general_20trim(df):
    df = df.copy()
    columnas = [
        "trimestre",
        "activos_totales",
        "pasivos_totales",
        "patrimonio_neto",
        "activos_corrientes",
        "pasivos_corrientes",
        "deuda_total"]
    df = df[columnas].dropna(subset=["trimestre"]).copy()
    if len(df) > 20:
        df_20 = df.tail(20).copy()
    else:
        df_20 = df.copy()
    df_20["trimestre"] = df_20["trimestre"].astype(str)

    def calcular_crecimiento_anualizado(serie):
        serie = serie.dropna()
        if len(serie) < 2:
            return np.nan
        vi = serie.iloc[0]
        vf = serie.iloc[-1]
        n_trimestres = len(serie) - 1
        años = n_trimestres / 4
        if vi <= 0 or vf <= 0 or años <= 0:
            return np.nan
        return (vf / vi) ** (1 / años) - 1
    crec_activos = calcular_crecimiento_anualizado(df_20["activos_totales"])
    crec_pasivos = calcular_crecimiento_anualizado(df_20["pasivos_totales"])
    crec_patrimonio = calcular_crecimiento_anualizado(df_20["patrimonio_neto"])
    ultimo_ratio_corriente = (
        df_20["activos_corrientes"].iloc[-1] /
        df_20["pasivos_corrientes"].iloc[-1]
        if df_20["pasivos_corrientes"].iloc[-1] != 0 else np.nan)
    ultima_deuda_patrimonio = (
        df_20["deuda_total"].iloc[-1] /
        df_20["patrimonio_neto"].iloc[-1]
        if df_20["patrimonio_neto"].iloc[-1] != 0 else np.nan)

    def fmt_pct(x):
        return "N/D" if pd.isna(x) else f"{x*100:.2f}%"

    def fmt_ratio(x):
        return "N/D" if pd.isna(x) else f"{x:.2f}x"
    texto = (
        f"Crecimiento anual ({df_20['trimestre'].iloc[0]} a {df_20['trimestre'].iloc[-1]})<br>"
        f"Activos: {fmt_pct(crec_activos)}<br>"
        f"Pasivos: {fmt_pct(crec_pasivos)}<br>"
        f"Patrimonio: {fmt_pct(crec_patrimonio)}<br><br>"
        f"Último quick ratio: {fmt_ratio(ultimo_ratio_corriente)}<br>"
        f"Última relación deuda/patrimonio: {fmt_ratio(ultima_deuda_patrimonio)}"
    )
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=df_20["trimestre"],
            y=df_20["pasivos_totales"],
            name="Pasivos"))
    fig.add_trace(
        go.Bar(
            x=df_20["trimestre"],
            y=df_20["patrimonio_neto"],
            name="Patrimonio"))
    fig.add_trace(
        go.Scatter(
            x=df_20["trimestre"],
            y=df_20["activos_totales"],
            mode="lines+markers",
            name="Activos totales"))
    fig.update_layout(
        title="Balance general trimestral: crecimiento y estructura",
        xaxis_title="Trimestre",
        yaxis_title="Pesos mexicanos",
        barmode="stack",
        template="plotly_white",
        width=1200,
        height=650,
        margin=dict(l=80, r=280, t=100, b=70),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=0
        ),
        annotations=[
            dict(
                x=1.65,
                y=1.02,
                xref="paper",
                yref="paper",
                text=texto,
                showarrow=False,
                align="left",
                bordercolor="white",
                borderwidth=1,
                borderpad=8,
                bgcolor="black"
            )
        ]
    )
    fig.update_yaxes(tickformat=",.0f")
    return fig


def balance_general_20trim():
    return grafica_balance_general_20trim(df_trim)

# Gráfica trimestral de liquidez y deuda a corto plazo


def grafica_liquidez_deuda_corto_plazo(df):
    df = df.copy()
    columnas = [
        "trimestre",
        "efectivo",
        "cuentas_por_cobrar",
        "inventario",
        "activos_corrientes",
        "pasivos_corrientes",
        "deuda_a_corto_plazo"]
    df = df[columnas].dropna(subset=["trimestre"]).copy()
    if len(df) > 20:
        df_20 = df.tail(20).copy()
    else:
        df_20 = df.copy()
    df_20["trimestre"] = df_20["trimestre"].astype(str)
    df_20["quick_assets"] = (
        df_20["efectivo"] + df_20["cuentas_por_cobrar"])
    df_20["ratio_corriente"] = (
        df_20["activos_corrientes"] /
        df_20["pasivos_corrientes"].replace(0, np.nan))
    df_20["quick_ratio"] = (
        (df_20["activos_corrientes"] - df_20["inventario"]) /
        df_20["pasivos_corrientes"].replace(0, np.nan))
    df_20["cobertura_efectivo_deuda_cp"] = (
        df_20["efectivo"] /
        df_20["deuda_a_corto_plazo"].replace(0, np.nan))
    ultimo_ratio_corriente = df_20["ratio_corriente"].iloc[-1]
    ultimo_quick_ratio = df_20["quick_ratio"].iloc[-1]
    ultima_cobertura = df_20["cobertura_efectivo_deuda_cp"].iloc[-1]

    def fmt_ratio(x):
        return "N/D" if pd.isna(x) else f"{x:.2f}x"

    texto = (
        f"Líquidez y deuda - {df_20['trimestre'].iloc[-1]}<br>"
        f"Ratio corriente: {fmt_ratio(ultimo_ratio_corriente)}<br>"
        f"Quick ratio: {fmt_ratio(ultimo_quick_ratio)}<br>"
        f"Efectivo / deuda a corto plazo: {fmt_ratio(ultima_cobertura)}")
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=df_20["trimestre"],
            y=df_20["efectivo"],
            name="Efectivo"))
    fig.add_trace(
        go.Bar(
            x=df_20["trimestre"],
            y=df_20["cuentas_por_cobrar"],
            name="Cuentas por cobrar"))
    fig.add_trace(
        go.Scatter(
            x=df_20["trimestre"],
            y=df_20["pasivos_corrientes"],
            mode="lines+markers",
            name="Pasivos corrientes",
            yaxis="y"))
    fig.add_trace(
        go.Scatter(
            x=df_20["trimestre"],
            y=df_20["deuda_a_corto_plazo"],
            mode="lines+markers",
            name="Deuda a corto plazo",
            yaxis="y"))
    fig.update_layout(
        title="Liquidez y deuda a corto plazo",
        xaxis_title="Trimestre",
        yaxis_title="Pesos mexicanos",
        barmode="stack",
        template="plotly_white",
        width=1200,
        height=650,
        margin=dict(l=80, r=280, t=100, b=70),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=0
        ),
        annotations=[
            dict(
                x=0.02,
                y=1.02,
                xref="paper",
                yref="paper",
                text=texto,
                showarrow=False,
                align="left",
                bordercolor="white",
                borderwidth=1,
                borderpad=8,
                bgcolor="black"
            )
        ]
    )
    fig.update_yaxes(tickformat=",.0f")
    return fig


def liquidez_deuda_corto_plazo_trimestral():
    return grafica_liquidez_deuda_corto_plazo(df_trim)

# Gráfica con calificaciones por métricas en los últimos 20 trimestres


def graf_calificaciones_trimestrales(df, umbral):
    calificaciones = []
    metricas = ["Crecimiento operativo", "Rentabilidad operativa", "Eficiencia de costes",
                "Solidez a corto plazo", "Momentum financiero", "Desempeño por unidad de negocio"]
    for i in df:
        calificaciones.append(reglas.creador_dataframes(
            i, umbral).tail(20).iloc[:, -1].to_numpy().tolist())
    diccionario = dict(zip(metricas, calificaciones))
    periodo = df_trim["trimestre"].tail(20)
    fig = go.Figure()
    for i, j in diccionario.items():
        fig.add_trace(go.Scatter(x=periodo, y=j, mode="lines", name=i))
    fig.update_layout(title="Métricas de los últimos trimestres", xaxis_title="Trimestre", yaxis_title="Calificación",
                      template="plotly_white", hovermode="x unified")
    return fig


def calificaciones_trimestrales():
    return graf_calificaciones_trimestrales(df_lista_trim, umbrales.umbrales_trimestrales)
