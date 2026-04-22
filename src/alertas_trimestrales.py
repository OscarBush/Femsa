# Alertas solo arroja una lista de alertas estructurales cuando están presentes

import pandas as pd
from pathlib import Path
import numpy as np

DIRECTORIO_BASE = Path(__file__).resolve().parent.parent
RUTA_DATOS = DIRECTORIO_BASE/'datos'
femsa_trim = RUTA_DATOS/'femsa_trimestral.csv'


def cargar_datos(df):
    df_cargado = pd.read_csv(df)
    return df_cargado.tail(20)


df_trim = cargar_datos(femsa_trim)


def caida(a):
    a = [x for x in a if pd.notna(x)]
    if len(a) < 3:
        return False
    return a[-1] < a[-2] and a[-2] < a[-3]


def subida(a):
    a = [x for x in a if pd.notna(x)]
    if len(a) < 3:
        return False
    return a[-1] > a[-2] and a[-2] > a[-3]


def crecimiento_bajo_trimestral(a, umbral=0.02):
    a = [x for x in a if pd.notna(x)]
    if len(a) < 3:
        return False
    b = []
    for i in a[-3:]:
        if i > umbral:
            b.append(i)
    return len(b) < 2


def alertas_estructurales_trimestrales(df_trim):
    df = df_trim.copy()
    ingresos = df["ingresos"].to_list()
    margen_operativo = (
        df["ebit"] / df["ingresos"].replace(0, np.nan)
    ).to_list()
    ebit = df["ebit"].to_list()
    beneficio_neto = df["beneficio_neto"].to_list()
    deuda_neta = (df["deuda_total"] - df["efectivo"]).to_list()
    crecimiento_ingresos = (
        (df["ingresos"] - df["ingresos"].shift(1)) /
        df["ingresos"].shift(1).replace(0, np.nan)
    ).to_list()
    venta_por_tienda = df["venta_por_tienda"].to_list()
    trafico = df["trafico_transacciones"].to_list()
    claves = [
        "Ingresos",
        "Margen operativo",
        "EBIT",
        "Beneficio neto",
        "Venta por tienda",
        "Tráfico"]
    valores = [
        ingresos,
        margen_operativo,
        ebit,
        beneficio_neto,
        venta_por_tienda,
        trafico]
    diccionario = dict(zip(claves, valores))
    alertas = []
    for clave, serie in diccionario.items():
        if caida(serie):
            alertas.append(f"Alerta estructural: caída consecutiva en {clave}")
    deuda_mal_usada = subida(deuda_neta) and crecimiento_bajo_trimestral(
        crecimiento_ingresos, umbral=0.02)
    if deuda_mal_usada:
        alertas.append(
            "Alerta estructural: la deuda aumenta sin crecimiento suficiente de ingresos")
    if not alertas:
        alertas.append("Sin alertas estructurales trimestrales")
    return alertas


def alertas_trimestrales():
    return alertas_estructurales_trimestrales(df_trim)
