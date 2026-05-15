"""
Procesa la base consolidada CEP y construye la agenda ciudadana anual:
para cada año, el porcentaje de menciones a cada tema (mapeado a nuestra
taxonomía de 19 temas presidenciales + 'Otros').

Usa las tres menciones con igual peso y aplica el ponderador 'pond'.
"""

import pandas as pd
from pathlib import Path

# ============================================
# CONFIGURACIÓN
# ============================================

RUTA_CEP = 'data/external/base_consolidada_1994_2025_03112025.csv'

VARS_INTERES = [
    'encuesta', 'encuesta_a', 'encuesta_m', 'pond',
    'percepcion_1_a', 'percepcion_1_b', 'percepcion_1_c',
]

# Diccionario código → etiqueta (de las alternativas que vimos en el diccionario CEP)
CODIGO_A_CATEGORIA_CEP = {
    1: 'Pensiones',
    2: 'Corrupción',
    3: 'Delincuencia, asaltos y robos',
    4: 'Derechos humanos',
    5: 'Educación',
    6: 'Empleo',
    7: 'Pobreza',
    8: 'Protección del medio ambiente',
    9: 'Narcotráfico',
    10: 'Salud',
    11: 'Sueldos',
    12: 'Transporte público',
    13: 'Vivienda',
    14: 'Inmigración',
    15: 'Reformas constitucionales',
    16: 'Desigualdad',
    17: 'Alzas de precios, inflación',
    18: 'Protestas y desórdenes callejeros',
    19: 'Terrorismo',
    20: 'Infraestructura',
    21: 'Sistema judicial',
    22: 'Sistema electoral binominal',
    23: 'Energía',
    24: 'Violencia con fines políticos',
    25: 'Pandemia por Covid-19',
    26: 'Violencia',
    27: 'La Constitución',
}

# Mapeo de categorías CEP a nuestros temas presidenciales
# (basado en la decisión que tomamos: 19 temas + ampliación con Corrupción/Pobreza/Desigualdad)
CEP_A_TEMA_PRESIDENCIAL = {
    'Pensiones': 'Pensiones',
    'Corrupción': 'Corrupción',
    'Delincuencia, asaltos y robos': 'Seguridad',
    'Derechos humanos': 'Derechos humanos',
    'Educación': 'Educación',
    'Empleo': 'Trabajo/Empleo',
    'Pobreza': 'Pobreza',
    'Protección del medio ambiente': 'Medio ambiente',
    'Narcotráfico': 'Seguridad',
    'Salud': 'Salud',
    'Sueldos': 'Trabajo/Empleo',
    'Transporte público': 'Otros',
    'Vivienda': 'Vivienda',
    'Inmigración': 'Migración',
    'Reformas constitucionales': 'Constitución',
    'Desigualdad': 'Desigualdad',
    'Alzas de precios, inflación': 'Economía',
    'Protestas y desórdenes callejeros': 'Seguridad',
    'Terrorismo': 'Seguridad',
    'Infraestructura': 'Otros',
    'Sistema judicial': 'Otros',
    'Sistema electoral binominal': 'Otros',
    'Energía': 'Otros',
    'Violencia con fines políticos': 'Seguridad',
    'Pandemia por Covid-19': 'Salud',
    'Violencia': 'Seguridad',
    'La Constitución': 'Constitución',
}

# ============================================
# CARGA Y LIMPIEZA
# ============================================

print("Cargando base CEP...")
df = pd.read_csv(RUTA_CEP, usecols=VARS_INTERES, encoding='utf-8')
print(f"  {len(df):,} filas cargadas")

# Convertir las tres menciones de wide a long
# Cada fila se convierte en hasta 3 filas (una por mención)
print("\nReformateando de wide a long (3 menciones por persona)...")
df_long = df.melt(
    id_vars=['encuesta', 'encuesta_a', 'encuesta_m', 'pond'],
    value_vars=['percepcion_1_a', 'percepcion_1_b', 'percepcion_1_c'],
    var_name='orden_mencion',
    value_name='codigo_problema'
)

# Filtrar respuestas válidas (excluir no sabe / no contesta / NaN)
df_long = df_long[df_long['codigo_problema'].isin(CODIGO_A_CATEGORIA_CEP.keys())]
print(f"  {len(df_long):,} menciones válidas tras filtrar")

# Mapear código a categoría CEP, luego a tema presidencial
df_long['categoria_cep'] = df_long['codigo_problema'].map(CODIGO_A_CATEGORIA_CEP)
df_long['tema_presidencial'] = df_long['categoria_cep'].map(CEP_A_TEMA_PRESIDENCIAL)

# ============================================
# AGREGACIÓN POR AÑO Y TEMA
# ============================================

print("\nCalculando agenda ciudadana anual...")

# Para cada año, sumar el ponderador por cada tema
# Luego dividir por el total ponderado del año para tener porcentajes
agenda_por_año = df_long.groupby(['encuesta_a', 'tema_presidencial'])['pond'].sum().reset_index()
agenda_por_año.columns = ['año', 'tema', 'menciones_ponderadas']

# Calcular total ponderado por año
total_por_año = agenda_por_año.groupby('año')['menciones_ponderadas'].sum().reset_index()
total_por_año.columns = ['año', 'total_año']

# Merge y calcular porcentaje
agenda_por_año = agenda_por_año.merge(total_por_año, on='año')
agenda_por_año['porcentaje'] = (agenda_por_año['menciones_ponderadas'] / agenda_por_año['total_año']) * 100
agenda_por_año['porcentaje'] = agenda_por_año['porcentaje'].round(2)

# Pivot para tener una fila por año y una columna por tema
agenda_pivot = agenda_por_año.pivot(index='año', columns='tema', values='porcentaje').fillna(0).round(2)
agenda_pivot = agenda_pivot.reset_index()

# Guardar
Path('data/derived').mkdir(exist_ok=True)
agenda_pivot.to_csv('data/derived/agenda_ciudadana.csv', index=False)

# ============================================
# RESUMEN
# ============================================

print("\n" + "="*70)
print("AGENDA CIUDADANA - TOP 3 TEMAS POR AÑO")
print("="*70)

cols_temas = [c for c in agenda_pivot.columns if c != 'año']

for _, fila in agenda_pivot.iterrows():
    año = int(fila['año'])
    temas_valores = [(c, fila[c]) for c in cols_temas]
    temas_valores.sort(key=lambda x: x[1], reverse=True)
    top3 = temas_valores[:3]
    top3_str = ", ".join([f"{t}({v:.1f}%)" for t, v in top3])
    print(f"{año}: {top3_str}")

print(f"\n\nGuardado: data/derived/agenda_ciudadana.csv")
print(f"Cobertura: {agenda_pivot['año'].min()} a {agenda_pivot['año'].max()}")