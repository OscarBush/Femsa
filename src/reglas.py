# Crea dataframes con las métricas, sus calificaciones y calificaciones normalizadas

import pandas as pd


def diccionarioinador(df):
    nombres_cols = list(df.columns)[1:]
    dicc = {}
    for i in nombres_cols:
        dicc.update({i: df[i].to_list()})
    return dicc


def calificador(j, umbral, metrica):
    lista = []
    if umbral[metrica]["sentido"] == "mayor_mejor":
        for i in j:
            if i < umbral[metrica]["min"]:
                lista.append(0)
            elif i > umbral[metrica]["max"]:
                lista.append(2)
            else:
                lista.append(1)
    elif umbral[metrica]["sentido"] == "menor_mejor":
        for i in j:
            if i < umbral[metrica]["min"]:
                lista.append(2)
            elif i > umbral[metrica]["max"]:
                lista.append(0)
            else:
                lista.append(1)
    return lista


def creador_dataframes(metrica, umbral):
    resultado = {}
    for i, j in metrica.items():
        if i in umbral:
            resultado[i] = calificador(j, umbral, i)
    df = pd.DataFrame(resultado)
    n = len(list(df.columns))
    cols = list(df.columns)
    df["Calificacion"] = df[cols].sum(axis=1)
    df["Calificacion_normalizada"] = round(
        (((df[cols].sum(axis=1))/(n*2))*10), 2)
    return df


# ultima_calificacion_anual(df_lista, umbrales.umbral)
def ultima_calificacion_anual(data_lista, umbral):
    b = []
    for i in data_lista:
        b.append(creador_dataframes(
            i, umbral).loc[-2:, "Calificacion_normalizada"].to_list()[-1])
    c = 0
    c += (b[0]*0.3)
    c += (b[1]*0.2)
    c += (b[2]*0.25)
    c += (b[3]*0.15)
    c += (b[4]*0.1)
    return c


def ultima_calificacion_trimestral(data_lista, umbral):
    b = []
    for i in data_lista:
        b.append(creador_dataframes(
            i, umbral).loc[-2:, "Calificacion_normalizada"].to_list()[-1])
    c = 0
    c += (b[0]*0.15)
    c += (b[1]*0.25)
    c += (b[2]*0.15)
    c += (b[3]*0.2)
    c += (b[4]*0.1)
    c += (b[5]*0.15)
    return c
