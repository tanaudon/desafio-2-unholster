"""
Validación: para cada documento, mostrar los 5 temas más mencionados
y verificar que tienen sentido sustantivo.
"""

import pandas as pd

df = pd.read_csv('data/derived/vectores_tematicos.csv')

# Columnas de menciones por mil palabras
cols_por_mil = [c for c in df.columns if c.startswith('por_mil_')]

print("="*80)
print("TOP 5 TEMAS POR DOCUMENTO (menciones por mil palabras)")
print("="*80)

# Programas primero
print("\n--- PROGRAMAS DE GOBIERNO ---")
programas = df[df['tipo'] == 'programa'].sort_values('año')

for _, fila in programas.iterrows():
    print(f"\n{fila['año']} {fila['presidente'].upper()} ({fila['n_palabras_total']:,} palabras)")
    # Top 5 temas
    temas = fila[cols_por_mil].sort_values(ascending=False).head(5)
    for col, valor in temas.items():
        tema = col.replace('por_mil_', '')
        print(f"  {tema:20s} {valor:6.2f}")

# Después cuentas, agrupadas por presidente para ver evolución
print("\n\n--- CUENTAS PÚBLICAS (top 3 por documento) ---")
cuentas = df[df['tipo'] == 'cuenta'].sort_values(['año'])

for _, fila in cuentas.iterrows():
    temas = fila[cols_por_mil].sort_values(ascending=False).head(3)
    top3 = ", ".join([f"{c.replace('por_mil_', '')}({v:.1f})" for c, v in temas.items()])
    print(f"{fila['año']} {fila['presidente']:10s}: {top3}")