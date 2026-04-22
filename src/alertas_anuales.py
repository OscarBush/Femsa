# Alertas solo arroja una lista de alertas estructurales cuando están presentes

import pandas as pd
from pathlib import Path
import numpy as np
from src import metricas

DIRECTORIO_BASE = Path(__file__).resolve().parent.parent
RUTA_DATOS = DIRECTORIO_BASE/'datos'
femsa_anual = RUTA_DATOS/'femsa_anual.csv'

df_anual = pd.read_csv(femsa_anual).tail(10)


def caida(a):
    if a[-1] < a[-2] and a[-2] < a[-3]:
        return True
    else:
        return False


def subida(a):
    if a[-1] > a[-2] and a[-2] > a[-3]:
        return True
    else:
        return False


def ingresos_bajos(a):
    b = []
    for i in a[-3:]:
        if i > 0.04:
            b.append(i)
    if len(b) < 2:
        return True
    else:
        return False


ingresos = df_anual["ingresos_totales"].to_list()
margen_operativo = (df_anual["EBIT"] /
                    df_anual["ingresos_totales"].replace(0, np.nan)).to_list()
deuda_neta = (df_anual["deuda_total"] - df_anual["efectivo"]).to_list()
crecimiento_ingresos = ((df_anual["ingresos_totales"] - df_anual["ingresos_totales"].shift(1)
                         ) / df_anual["ingresos_totales"].shift(1).replace(0, np.nan)).to_list()
fcf = df_anual["flujo_de_efectivo"].to_list()
roic_wacc = metricas.calidad_anual(
    df_anual)["roic - wacc"].to_list()


claves = ["Ingresos totales", "Margen operativo",
          "Flujo de efectivo", "ROIC - WACC (creación de valor)"]
valores = [ingresos, margen_operativo, fcf, roic_wacc]

diccionario = dict(zip(claves, valores))


def alertas_anuales():
    b = []
    for i, j in diccionario.items():
        if caida(j) == True:
            b.append(f"Alerta estructural: {i}")
        else:
            b.append("")
    deuda_mal_usada = subida(deuda_neta) is True and ingresos_bajos(
        crecimiento_ingresos) is True
    if deuda_mal_usada is True:
        b.append("Alerta estructural: La deuda aumenta sin crecimiento de ingresos")
    else:
        b.append("")
    return b


# print(alertas())
