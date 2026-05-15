"""
Cruza la aprobación presidencial anual con el alineamiento entre
discurso presidencial y agenda ciudadana, calculado en alignment.py.

Pregunta: ¿hay correlación entre cuán alineado está el discurso 
presidencial con la agenda ciudadana, y la aprobación de ese mismo año?

IMPORTANTE: esto es análisis correlativo descriptivo, no causal.
La aprobación es endógena a múltiples factores no controlados aquí.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from scipy.stats import pearsonr, spearmanr

# Cargar datos
aprobacion = pd.read_csv('data/derived/aprobacion_por_año.csv')
alineamiento = pd.read_csv('data/derived/alineamiento_global.csv')

# Merge por año
df = alineamiento.merge(aprobacion[['año', 'pct_aprueba', 'pct_desaprueba']], 
                         on='año', how='inner')

print(f"Años con datos en ambas fuentes: {len(df)}")
print(f"Rango: {df['año'].min()} - {df['año'].max()}\n")

# Correlación Pearson (asume linealidad)
r_pearson, p_pearson = pearsonr(df['alineamiento_global'], df['pct_aprueba'])

# Correlación Spearman (no paramétrica, basada en rangos)
r_spearman, p_spearman = spearmanr(df['alineamiento_global'], df['pct_aprueba'])

print("="*70)
print("CORRELACIÓN: ALINEAMIENTO DISCURSIVO vs APROBACIÓN PRESIDENCIAL")
print("="*70)
print(f"\nPearson:   r = {r_pearson:+.4f}, p = {p_pearson:.4f}")
print(f"Spearman:  r = {r_spearman:+.4f}, p = {p_spearman:.4f}")

print("\nInterpretación de la magnitud (Cohen):")
print("  |r| < 0.1     : sin relación")
print("  0.1 ≤ |r| < 0.3: relación débil")
print("  0.3 ≤ |r| < 0.5: relación moderada")
print("  |r| ≥ 0.5     : relación fuerte")

# Mostrar tabla con datos crudos para inspección
print("\n" + "="*70)
print("DATOS POR AÑO (ordenados por alineamiento)")
print("="*70)
df_show = df[['año', 'presidente', 'alineamiento_global', 'pct_aprueba']].copy()
df_show = df_show.sort_values('alineamiento_global', ascending=False)
print(df_show.to_string(index=False))

# Análisis adicional: top 5 años más alineados vs top 5 menos alineados
print("\n" + "="*70)
print("COMPARACIÓN DE EXTREMOS")
print("="*70)

top5_align = df.nlargest(5, 'alineamiento_global')
bot5_align = df.nsmallest(5, 'alineamiento_global')

print(f"\nAprobación promedio en años MÁS alineados (top 5): {top5_align['pct_aprueba'].mean():.1f}%")
print(f"Aprobación promedio en años MENOS alineados (bot 5): {bot5_align['pct_aprueba'].mean():.1f}%")
print(f"\nTop 5 años más alineados:")
print(top5_align[['año', 'presidente', 'alineamiento_global', 'pct_aprueba']].to_string(index=False))
print(f"\nBot 5 años menos alineados:")
print(bot5_align[['año', 'presidente', 'alineamiento_global', 'pct_aprueba']].to_string(index=False))

# Guardar dataset combinado
df.to_csv('data/derived/aprobacion_vs_alineamiento.csv', index=False)
print(f"\n\nGuardado: data/derived/aprobacion_vs_alineamiento.csv")