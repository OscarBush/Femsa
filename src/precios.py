# Se crea la gráfica de precios por periodo de tiempo

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import yfinance as yf


def _descargar_datos(ticker, periodo):
    df = yf.download(ticker, period=periodo, auto_adjust=False)
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    return df


def crear_figura(df, ticker, height=500):
    df = df.copy().reset_index()

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=df["Date"],
            y=df["Close"],
            mode="lines",
            name="Cierre",
            line=dict(color="green", width=2),
        )
    )

    fig.update_layout(
        title=f"Precio histórico de {ticker}",
        xaxis_title="Fecha",
        yaxis_title="Precio",
        template="plotly_dark",
        height=height
    )
    return fig


def grafica_precio(ticker, periodo, height=500):
    df = _descargar_datos(ticker, periodo)
    if df.empty:
        return None
    return crear_figura(df, ticker, height)


def precio_historico():
    st.header("Precio histórico")
    ticker = st.text_input("Ticker", value="FEMSAUBD.MX")
    periodo = st.selectbox(
        "Periodo",
        ["1mo", "3mo", "6mo", "1y", "2y", "5y", "max"],
        index=1,
    )

    fig = grafica_precio(ticker, periodo)

    if fig is not None:
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.error("No se pudieron descargar datos.")
