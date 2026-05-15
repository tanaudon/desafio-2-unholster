"""
Exploración inicial de la base consolidada CEP.
Carga solo las variables necesarias para nuestro análisis.
"""

import pandas as pd

# IMPORTANTE: ajusta la ruta y extensión al nombre real del archivo
RUTA_CEP = 'data/external/base_consolidada_1994_2025_03112025.csv'

# Variables que nos interesan
VARS_INTERES = [
    'encuesta',       # Número de encuesta
    'encuesta_a',     # Año de la encuesta
    'encuesta_m',     # Mes de la encuesta
    'pond',           # Ponderador
    'percepcion_1_a', # Primera mención de problema
    'percepcion_1_b', # Segunda mención
    'percepcion_1_c', # Tercera mención
]

print("Cargando base CEP (solo columnas necesarias)...")
df = pd.read_csv(RUTA_CEP, usecols=VARS_INTERES, encoding='utf-8')

print(f"\nFilas totales: {len(df):,}")
print(f"Columnas: {list(df.columns)}")

print(f"\nRango temporal:")
print(f"  Años: {df['encuesta_a'].min()} a {df['encuesta_a'].max()}")
print(f"  Número de encuestas únicas: {df['encuesta'].nunique()}")

print(f"\nFilas por año:")
print(df.groupby('encuesta_a').size())

print(f"\nValores únicos de percepcion_1_a (primera mención):")
print(sorted(df['percepcion_1_a'].dropna().unique())[:30])