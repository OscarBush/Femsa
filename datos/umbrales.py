umbrales_anuales = {

    # 1. CALIDAD ANUAL
    "roic - wacc": {"sentido": "mayor_mejor", "min": 0.00, "max": 0.05},
    "margen_fcf": {"sentido": "mayor_mejor", "min": 0.02, "max": 0.05},
    "margen_bruto": {"sentido": "mayor_mejor", "min": 0.34, "max": 0.39},
    "margen_operativo": {"sentido": "mayor_mejor", "min": 0.08, "max": 0.10},

    # 2. CRECIMIENTO ANUAL
    "crecimiento_sostenible": {"sentido": "mayor_mejor", "min": 0.02, "max": 0.06},
    "flujo_operativo_capex": {"sentido": "mayor_mejor", "min": 1.30, "max": 2.00},
    "crecimiento_ingresos": {"sentido": "mayor_mejor", "min": 0.03, "max": 0.08},
    "crecimiento_ebit": {"sentido": "mayor_mejor", "min": 0.04, "max": 0.10},
    "crecimiento_utilidad": {"sentido": "mayor_mejor", "min": 0.03, "max": 0.10},

    # 3. SOLIDEZ ANUAL
    "Altman_z_score": {"sentido": "mayor_mejor", "min": 2.0, "max": 3.2},
    "deuda_neta_ebitda": {"sentido": "menor_mejor", "min": 1.5, "max": 3.0},
    "cobertura_intereses": {"sentido": "mayor_mejor", "min": 3.0, "max": 6.0},
    "quick_ratio": {"sentido": "mayor_mejor", "min": 0.60, "max": 1.00},

    # 4. ESTRUCTURA ANUAL
    "deuda_neta":  {"sentido": "menor_mejor", "min": -0.1, "max": 0},
    "deuda_neta_patrimonio": {"sentido": "menor_mejor", "min": 0.35, "max": 0.70},

    # 5. DIVIDENDO ANUAL
    "flujo_operativo_dividendos": {"sentido": "mayor_mejor", "min": 1.50, "max": 3.00},
    "payout_ratio": {"sentido": "menor_mejor", "min": 0.50, "max": 0.80},
    "roe": {"sentido": "mayor_mejor", "min": 0.08, "max": 0.14}
}


umbrales_trimestrales = {

    # 1. CRECIMIENTO OPERATIVO
    "crecimiento_ingresos_yoy": {"sentido": "mayor_mejor", "min": 0.02, "max": 0.07},
    "crecimiento_ingresos_qoq": {"sentido": "mayor_mejor", "min": -0.03, "max": 0.03},
    "crecimiento_ticket_promedio_yoy": {"sentido": "mayor_mejor", "min": 0.01, "max": 0.05},

    # 2. RENTABILIDAD OPERATIVA
    "margen_bruto": {"sentido": "mayor_mejor", "min": 0.35, "max": 0.45},
    "margen_operativo": {"sentido": "mayor_mejor", "min": 0.08, "max": 0.12},
    "margen_neto": {"sentido": "mayor_mejor", "min": 0.03, "max": 0.06},
    "variacion_margen_operativo": {"sentido": "mayor_mejor", "min": -0.01, "max": 0.015},

    # 3. EFICIENCIA
    "ratio_coste_ingresos": {"sentido": "menor_mejor", "min": 0.55, "max": 0.65},
    "ratio_gastos_operativos": {"sentido": "menor_mejor", "min": 0.20, "max": 0.30},
    "ratio_gastos_totales": {"sentido": "menor_mejor", "min": 0.75, "max": 0.90},
    "variacion_coste_ingresos": {"sentido": "menor_mejor", "min": -0.02, "max": 0.02},

    # 4. SOLIDEZ FINANCIERA
    "deuda_neta":  {"sentido": "menor_mejor", "min": -0.1, "max": 0},
    "cobertura_intereses": {"sentido": "mayor_mejor", "min": 3.0, "max": 6.0},
    "ratio_liquidez": {"sentido": "mayor_mejor", "min": 1, "max": 1.5},

    # 5. MOMENTUM
    "tendencia_ingresos": {"sentido": "mayor_mejor", "min": 0, "max": 0.01},
    "tendencia_ebit": {"sentido": "mayor_mejor", "min": 0, "max": 0.01},
    "consistencia_crecimiento": {"sentido": "mayor_mejor", "min": 1, "max": 4},
    "aceleracion_crecimiento": {"sentido": "mayor_mejor", "min": -0.02, "max": 0.02},

    # 6. UNIDADES DE NEGOCIO
    "crecimiento_oxxo_yoy": {"sentido": "mayor_mejor", "min": 0.02, "max": 0.06},
    "crecimiento_salud_yoy": {"sentido": "mayor_mejor", "min": 0.01, "max": 0.05},
    "crecimiento_usuarios_spin_yoy": {"sentido": "mayor_mejor", "min": 0.10, "max": 0.25},
    "crecimiento_combustibles_yoy": {"sentido": "mayor_mejor", "min": -0.03, "max": 0.03},
    "calidad_retail": {"sentido": "mayor_mejor", "min": -0.02, "max": 0.02}
}
