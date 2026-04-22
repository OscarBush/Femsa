# Proyecto FEMSA versión 0.1

## Objetivo del proyecto  
Construir un sistema en un dashboard que permita evaluar a FEMSA de forma estructurada mediante datos históricos anuales y trimestrales para apoyar decisiones de inclusión en watchlist, compra, mantenimiento o venta, así como detectar deterioro estructural que justifique su exclusión del portafolio de inversión. El sistema debe lograr visualizar claramente datos y métricas, y ser reproducible.

## Alcance  
El sistema usará información financiera de al menos 10 años y reportes trimestrales de entre 12 y 20 trimestres, integrando variables financieras y no financieras. El resultado será un dashboard interactivo.

---

## Estructura del proyecto
```
femsa_dashboard/
│
├── datos/
│   ├── femsa_anual.csv
│   ├── femsa_trimestral.csv
│   └── umbrales.py
│
├── src/
│   ├── alertas_anuales.py
│   ├── alertas_trimestrales.py
│   ├── graficas_anuales.py
│   ├── graficas_trimestrales.py
│   ├── metricas.py
│   ├── reglas.py
│   ├── precios.py
│   └── __init__.py
│
├── app/
│   ├── femsa_logo.png
│   └── dashboard.py
│   └── paginas/
│       ├── generalidades.py
│       ├── tendencias_anuales.py
│       └── tendencias_trimestrales.py
├── main.py
├── requirements.txt
└── README.md
```
La carpeta datos contiene los archivos de entrada del proyecto. Su función es almacenar los datos crudos con los que se va a trabajar. Aquí se colocan femsa_anual.csv y femsa_trimestral.csv. El archivo umbrales.py contiene diccionarios agrupados por métricas en las que se establecen los rangos para determinar el desempeño de cada una según su categoría (anual o trimestral). La idea es que estos archivos sean la base del sistema y se mantengan como fuente original de información. 

La carpeta src contiene la lógica central del proyecto. Aquí es donde vive el procesamiento de datos. La razón de separar esta carpeta es evitar que todo quede mezclado dentro del dashboard o del archivo principal para corregir errores, ampliar el proyecto o entender actividades esenciales de forma separada.

El archivo metricas.py tiene la función de calcular las métricas financieras y operativas a partir de los datos crudos. La lógica es que este archivo transforme columnas base en indicadores más útiles para el análisis.

El archivo reglas.py tiene la función de interpretar las métricas. Aquí se procesan los datos en un proceso de semaforización, los scores y las alertas. Por ejemplo, si margen_operativo es mayor a cierto valor, se asigna una calificación de "2" (verde); si deuda_neta/patrimonio es muy alta, se asigna "0" (rojo). 

El archivo alertas_anuales y alertas_trimestrales ejecutan reglas “si ingresos caen tres trimestres consecutivos, activar alerta”. La lógica es separar el cálculo del juicio. 

El archivo graficas_anuales.py y graficas_trimestrales.py tienen la función de generar visualizaciones. Las gráficas forman parte de una capa que no calculan métricas ni definen reglas, solo presentan resultados de forma visual. 

La carpeta app contiene la interfaz visual del proyecto. Su función es reunir resultados ya procesados y mostrarlos al usuario. 

El archivo dashboard.py tiene la función de construir la ventana interactiva del dashboard, expresa cómo se organiza la información en pantalla: gráfica de precio, scores, menús laterales, tablas y secciones de ratios o tendencias. Este archivo usa lo que ya se preparó en los demás módulos.

El archivo main.py tiene la función de ser el punto de entrada del proyecto. 

---

## Proceso de desarrollo

1. Creación de un dataset básico con datos anuales y trimestrales.  
2. Carga de datos usando pandas con validaciones básicas.  
3. Cálculo de métricas financieras y operativas.  
4. Implementación del sistema de semáforos.  
5. Construcción de un score simple basado en suma de métricas.  
6. Definición de alertas estructurales básicas.  
7. Generación de salida en consola con métricas y alertas.  
8. Creación de visualización básica con plotly y matplotlib.  
9. Validación manual de métricas clave.  
10. Control de calidad antes de avanzar a etapas más complejas.

---

## Criterios de finalización versión 0.1

El proyecto se considera terminado cuando:

- Se cargan los datos sin errores  
- Se calculan correctamente las métricas definidas  
- Se obtiene un score coherente  
- Se detectan alertas básicas  
- Se visualiza al menos una gráfica simple  
- Se puede explicar de forma clara el estado del negocio con base en los resultados  

---

