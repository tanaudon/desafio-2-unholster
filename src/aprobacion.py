"""
Extrae datos de aprobación presidencial de la base consolidada CEP
y los agrega por año (promedio de las encuestas dentro del año).

Variable usada: eval_gob_1
"Independiente de su posición política, usted ¿aprueba o desaprueba 
la forma como está conduciendo el PRESIDENTE el gobierno?"
- 1 = Aprueba
- 2 = Desaprueba  
- 3 = No aprueba ni desaprueba
- -8 = No sabe (excluido)
- -9 = No responde (excluido)

Métrica: % aprobación = aprueba / (aprueba + desaprueba + ni una ni otra),
ponderada con 'pond'.
"""

import pandas as pd
from pathlib import Path

RUTA_CEP = 'data/external/base_consolidada_1994_2025_03112025.csv'

VARS = ['encuesta', 'encuesta_a', 'encuesta_m', 'pond', 'eval_gob_1']

print("Cargando base CEP...")
df = pd.read_csv(RUTA_CEP, usecols=VARS, encoding='utf-8')
print(f"  {len(df):,} filas cargadas")

# Filtrar solo respuestas válidas (1, 2, 3)
df_validas = df[df['eval_gob_1'].isin([1, 2, 3])].copy()
print(f"  {len(df_validas):,} filas con respuesta válida")

# Calcular % aprobación por encuesta (no por año aún, para preservar grano)
print("\nCalculando aprobación por encuesta...")
aprob_por_encuesta = []
for (encuesta, año, mes), grupo in df_validas.groupby(['encuesta', 'encuesta_a', 'encuesta_m']):
    total_pond = grupo['pond'].sum()
    aprueba_pond = grupo[grupo['eval_gob_1'] == 1]['pond'].sum()
    desaprueba_pond = grupo[grupo['eval_gob_1'] == 2]['pond'].sum()
    
    pct_aprueba = (aprueba_pond / total_pond) * 100 if total_pond > 0 else 0
    pct_desaprueba = (desaprueba_pond / total_pond) * 100 if total_pond > 0 else 0
    
    aprob_por_encuesta.append({
        'encuesta': encuesta,
        'año': año,
        'mes': mes,
        'n_respuestas': len(grupo),
        'pct_aprueba': round(pct_aprueba, 2),
        'pct_desaprueba': round(pct_desaprueba, 2),
        'pct_neutro': round(100 - pct_aprueba - pct_desaprueba, 2),
    })

df_encuesta = pd.DataFrame(aprob_por_encuesta).sort_values(['año', 'mes']).reset_index(drop=True)

# Agregar por año (promedio simple de encuestas dentro del año)
print("Agregando por año...")
df_año = df_encuesta.groupby('año').agg({
    'pct_aprueba': 'mean',
    'pct_desaprueba': 'mean',
    'pct_neutro': 'mean',
    'n_respuestas': 'sum',
    'encuesta': 'count',
}).reset_index()
df_año.columns = ['año', 'pct_aprueba', 'pct_desaprueba', 'pct_neutro', 'n_total_respuestas', 'n_encuestas_año']
df_año = df_año.round(2)

# Guardar
Path('data/derived').mkdir(exist_ok=True)
df_encuesta.to_csv('data/derived/aprobacion_por_encuesta.csv', index=False)
df_año.to_csv('data/derived/aprobacion_por_año.csv', index=False)

print("\n" + "="*70)
print("APROBACIÓN PRESIDENCIAL POR AÑO")
print("="*70)
print(df_año.to_string(index=False))

print(f"\n\nGuardado:")
print(f"  data/derived/aprobacion_por_encuesta.csv")
print(f"  data/derived/aprobacion_por_año.csv")