# Crea dataframes con métricas por cada segmento a evaluar de la empresa

import numpy as np


def calidad_anual(df):
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
    df["margen_fcf"] = ((df["flujo_de_efectivo_operativo"] -
                        df["capex"])) / df["ingresos_totales"].replace(0, np.nan)
    df["margen_bruto"] = df["beneficio_bruto"] / \
        df["ingresos_totales"].replace(0, np.nan)
    df["margen_operativo"] = df["EBIT"] / \
        df["ingresos_totales"].replace(0, np.nan)
    return df.loc[:, ["periodo_anual", "roic - wacc", "margen_fcf", "margen_bruto", "margen_operativo"]]


def crecimiento_anual(df):
    df = df.copy()
    df["roe"] = df["beneficio_neto"] / df["patrimonio_neto"].replace(0, np.nan)
    df["payout_ratio"] = df["dividendos_pagados"] / \
        df["beneficio_neto"].replace(0, np.nan)
    df["crecimiento_sostenible"] = df["roe"] * (1 - df["payout_ratio"])
    df["flujo_operativo_capex"] = df["flujo_de_efectivo_operativo"] / \
        df["capex"].replace(0, np.nan)
    df["crecimiento_ingresos"] = (
        df["ingresos_totales"] - df["ingresos_totales"].shift(1)) / df["ingresos_totales"].shift(1).replace(0, np.nan)
    df["crecimiento_ebit"] = (
        df["EBIT"] - df["EBIT"].shift(1)) / df["EBIT"].shift(1).replace(0, np.nan)
    df["crecimiento_utilidad"] = (
        df["beneficio_neto"] - df["beneficio_neto"].shift(1)) / df["beneficio_neto"].shift(1).replace(0, np.nan)
    return df.loc[:, ["periodo_anual", "crecimiento_sostenible", "flujo_operativo_capex",
                      "crecimiento_ingresos", "crecimiento_ebit", "crecimiento_utilidad"]]


def solidez_anual(df):
    df = df.copy()
    df["capital_trabajo"] = df["activos_corrientes"] - df["pasivos_corrientes"]
    df["X1"] = df["capital_trabajo"] / df["activos_totales"].replace(0, np.nan)
    df["X2"] = df["utilidades_retenidas"] / \
        df["activos_totales"].replace(0, np.nan)
    df["X3"] = df["EBIT"] / df["activos_totales"].replace(0, np.nan)
    df["X4"] = df["patrimonio_neto"] / df["pasivos_totales"].replace(0, np.nan)
    df["Altman_z_score"] = (6.56 * df["X1"]) + (3.26 *
                                                df["X2"]) + (6.72 * df["X3"]) + (1.05 * df["X4"])
    df["deuda_neta"] = df["deuda_total"] - df["efectivo"]
    df["deuda_neta_ebitda"] = df["deuda_neta"] / \
        (df["EBIT"] + df["depreciacion_y_amortizacion"]).replace(0, np.nan)
    df["cobertura_intereses"] = df["EBIT"] / \
        df["intereses_pagados"].replace(0, np.nan)
    df["quick_ratio"] = (df["activos_corrientes"] -
                         df["inventario"]) / df["pasivos_corrientes"].replace(0, np.nan)
    return df.loc[:, ["periodo_anual", "Altman_z_score",
                      "deuda_neta_ebitda", "cobertura_intereses", "quick_ratio"]]


def estructura_anual(df):
    df = df.copy()
    df["deuda_neta"] = df["deuda_total"] - df["efectivo"]
    df["deuda_neta_patrimonio"] = df["deuda_neta"] / \
        df["patrimonio_neto"].replace(0, np.nan)
    return df.loc[:, ["periodo_anual", "deuda_neta",
                      "deuda_neta_patrimonio"]]


def dividendo_anual(df):
    df = df.copy()
    df["roe"] = df["beneficio_neto"] / df["patrimonio_neto"].replace(0, np.nan)
    df["payout_ratio"] = df["dividendos_pagados"] / \
        df["beneficio_neto"].replace(0, np.nan)
    df["flujo_operativo_dividendos"] = df["flujo_de_efectivo_operativo"] / \
        df["dividendos_pagados"].replace(0, np.nan)
    return df.loc[:, ["periodo_anual", "flujo_operativo_dividendos",
                      "payout_ratio", "roe"]]


def crecimiento_operativo_df(df):
    df = df.copy()
    df["crecimiento_ingresos_yoy"] = (
        df["ingresos"] - df["ingresos"].shift(4)) / df["ingresos"].shift(4).replace(0, np.nan)
    df["crecimiento_ingresos_qoq"] = (
        df["ingresos"] - df["ingresos"].shift(1)) / df["ingresos"].shift(1).replace(0, np.nan)
    df["crecimiento_ticket_promedio_yoy"] = (
        df["ticket_promedio"] - df["ticket_promedio"].shift(4)) / df["ticket_promedio"].shift(4).replace(0, np.nan)
    parametros = ["crecimiento_ingresos_yoy", "crecimiento_ingresos_qoq",
                  "crecimiento_ticket_promedio_yoy"]
    return df.loc[:, parametros]


def rentabilidad_operativa_df(df):
    df = df.copy()
    df["margen_bruto"] = df["beneficio_bruto"] / \
        df["ingresos"].replace(0, np.nan)
    df["margen_operativo"] = df["ebit"]/df["ingresos"].replace(0, np.nan)
    df["margen_neto"] = df["beneficio_neto"]/df["ingresos"].replace(0, np.nan)
    df["variacion_margen_operativo"] = (
        df["margen_operativo"]-df["margen_operativo"].shift(4))
    parametros = ["margen_bruto", "margen_operativo", "margen_neto",
                  "variacion_margen_operativo"]
    return df.loc[:, parametros]


def eficiencia_control_costos_df(df):
    df = df.copy()
    df["ratio_coste_ingresos"] = df["coste_ventas"] / \
        df["ingresos"].replace(0, np.nan)
    df["ratio_gastos_operativos"] = df["gastos_operativos"] / \
        df["ingresos"].replace(0, np.nan)
    df["ratio_gastos_totales"] = (
        df["coste_ventas"] + df["gastos_operativos"])/df["ingresos"].replace(0, np.nan)
    df["variacion_coste_ingresos"] = df["ratio_gastos_totales"] - \
        df["ratio_gastos_totales"].shift(4)
    parametros = ["ratio_coste_ingresos", "ratio_gastos_operativos",
                  "ratio_gastos_totales", "variacion_coste_ingresos"]
    return df.loc[:, parametros]


def solidez_financiera_corto_plazo_df(df):
    df = df.copy()
    df["deuda_neta"] = df["deuda_total"] - df["efectivo"]
    df["cobertura_intereses"] = df["ebit"] / \
        df["gastos_financieros"].replace(0, np.nan)
    df["ratio_liquidez"] = df["activos_corrientes"] / df["pasivos_corrientes"]
    parametros = ["deuda_neta", "cobertura_intereses", "ratio_liquidez"]
    return df.loc[:, parametros]


def momentum_financiero_df(df):
    df = df.copy()
    df["tendencia_ingresos"] = (df["ingresos"] - df["ingresos"].shift(3))/3
    df["tendencia_ebit"] = (df["ebit"] - df["ebit"].shift(3))/3
    df["crecimiento_qoq_t"] = (
        df["ingresos"] - df["ingresos"].shift(1))/df["ingresos"].shift(1)
    df["consistencia_crecimiento"] = df["crecimiento_qoq_t"]+df["crecimiento_qoq_t"].shift(
        1)+df["crecimiento_qoq_t"].shift(2)+df["crecimiento_qoq_t"].shift(3)
    df["crecimiento_yoy_t"] = (
        df["ingresos"] - df["ingresos"].shift(4))/df["ingresos"].shift(4)
    df["crecimiento_yoy_t-1"] = (df["ingresos"].shift(1) -
                                 df["ingresos"].shift(5))/df["ingresos"].shift(5)
    df["aceleracion_crecimiento"] = df["crecimiento_yoy_t"] - \
        df["crecimiento_yoy_t-1"]
    parametros = ["tendencia_ingresos", "tendencia_ebit",
                  "consistencia_crecimiento", "aceleracion_crecimiento"]
    return df.loc[:, parametros]


def performance_por_unidad_negocio_df(df):
    df = df.copy()
    df["crecimiento_oxxo_yoy"] = (
        df["oxxo_totales"] - df["oxxo_totales"].shift(4)) / df["oxxo_totales"].shift(4)
    df["crecimiento_salud_yoy"] = (
        df["salud_totales"] - df["salud_totales"].shift(4))/df["salud_totales"].shift(4)
    df["crecimiento_usuarios_spin_yoy"] = (
        df["usuarios_spin_totales"] - df["usuarios_spin_totales"].shift(4))/df["usuarios_spin_totales"].shift(4)
    df["crecimiento_combustibles_yoy"] = (
        df["combustibles_totales"] - df["combustibles_totales"].shift(4))/df["combustibles_totales"].shift(4)
    df["calidad_retail"] = df["trafico_transacciones"] * df["ticket_promedio"]
    parametros = ["crecimiento_oxxo_yoy", "crecimiento_salud_yoy",
                  "crecimiento_usuarios_spin_yoy", "crecimiento_combustibles_yoy",
                  "calidad_retail"]
    return df.loc[:, parametros]
