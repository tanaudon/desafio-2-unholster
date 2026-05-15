"""
Alineamiento entre agenda presidencial (cuentas públicas) y agenda
ciudadana (encuestas CEP). Para cada año con datos en ambas:
- Normaliza ambas agendas a porcentajes sobre temas comparables.
- Calcula brecha por tema (presidencial - ciudadana).
- Calcula índice global de alineamiento (similar a Jensen-Shannon
  pero sobre las dos distribuciones).
"""

import pandas as pd
import numpy as np
from scipy.spatial.distance import jensenshannon

# ============================================
# TEMAS COMPARABLES (los que están en ambas fuentes)
# ============================================
# Excluimos los temas presidenciales sin equivalente en CEP:
# Araucanía/Mapuche, Género/Mujer, Niños/Infancia, Regiones, Tecnología.
# Para la comparación solo usamos temas mapeables.

TEMAS_COMPARABLES = [
    'Constitución',
    'Corrupción',
    'Derechos humanos',
    'Desigualdad',
    'Economía',
    'Educación',
    'Medio ambiente',
    'Migración',
    'Pensiones',
    'Pobreza',
    'Salud',
    'Seguridad',
    'Trabajo/Empleo',
    'Vivienda',
]

# ============================================
# CARGA DE DATOS
# ============================================

vectores = pd.read_csv('data/derived/vectores_tematicos.csv')
agenda = pd.read_csv('data/derived/agenda_ciudadana.csv')

# Filtrar solo cuentas públicas (no programas) para alineamiento
cuentas = vectores[vectores['tipo'] == 'cuenta'].copy()


def normalizar_a_porcentaje(valores_dict):
    """
    Toma un dict {tema: valor} y devuelve {tema: porcentaje} donde
    los porcentajes suman 100 sobre los temas comparables.
    """
    total = sum(valores_dict.values())
    if total == 0:
        return {t: 0 for t in valores_dict}
    return {t: (v / total) * 100 for t, v in valores_dict.items()}


def calcular_alineamiento(año, presidente):
    """
    Para un año específico, calcula brechas tema a tema y un índice global.
    Devuelve dict con métricas.
    """
    # Buscar cuenta presidencial del año
    cuenta = cuentas[(cuentas['año'] == año) & (cuentas['presidente'] == presidente)]
    if cuenta.empty:
        return None
    
    # Extraer valores presidenciales solo para temas comparables
    valores_presidente = {}
    for tema in TEMAS_COMPARABLES:
        col = f'por_mil_{tema}'
        if col in cuenta.columns:
            valores_presidente[tema] = float(cuenta.iloc[0][col])
        else:
            valores_presidente[tema] = 0
    
    # Buscar agenda ciudadana del año
    agenda_año = agenda[agenda['año'] == año]
    if agenda_año.empty:
        return None
    
    valores_ciudadania = {}
    for tema in TEMAS_COMPARABLES:
        if tema in agenda_año.columns:
            valores_ciudadania[tema] = float(agenda_año.iloc[0][tema])
        else:
            valores_ciudadania[tema] = 0
    
    # Normalizar ambas a porcentajes
    pres_pct = normalizar_a_porcentaje(valores_presidente)
    ciu_pct = normalizar_a_porcentaje(valores_ciudadania)
    
    # Calcular brechas por tema (positivo = presidente sobre-enfatiza)
    brechas = {tema: pres_pct[tema] - ciu_pct[tema] for tema in TEMAS_COMPARABLES}
    
    # Índice global: 1 - divergencia Jensen-Shannon
    vec_pres = np.array([pres_pct[t] for t in TEMAS_COMPARABLES])
    vec_ciu = np.array([ciu_pct[t] for t in TEMAS_COMPARABLES])
    
    # Normalizar a distribuciones de probabilidad
    if vec_pres.sum() > 0:
        vec_pres_norm = vec_pres / vec_pres.sum()
    else:
        vec_pres_norm = np.ones_like(vec_pres) / len(vec_pres)
    if vec_ciu.sum() > 0:
        vec_ciu_norm = vec_ciu / vec_ciu.sum()
    else:
        vec_ciu_norm = np.ones_like(vec_ciu) / len(vec_ciu)
    
    distancia_js = jensenshannon(vec_pres_norm, vec_ciu_norm, base=2)
    divergencia = distancia_js ** 2
    alineamiento_global = 1 - divergencia
    
    return {
        'año': año,
        'presidente': presidente,
        'alineamiento_global': round(alineamiento_global, 4),
        'brechas': brechas,
        'presidencial': pres_pct,
        'ciudadana': ciu_pct,
    }


# ============================================
# CALCULAR PARA TODOS LOS AÑOS
# ============================================

resultados_globales = []
resultados_brechas = []

años_agenda = set(agenda['año'].unique())
años_cuentas = set(cuentas['año'].unique())
años_comunes = sorted(años_agenda & años_cuentas)

print(f"Años con datos en ambas fuentes: {len(años_comunes)}")
print(f"Rango: {min(años_comunes)} - {max(años_comunes)}")
print(f"Años faltantes en CEP: {sorted(años_cuentas - años_agenda)}")
print()

for año in años_comunes:
    # Buscar presidente del año
    fila = cuentas[cuentas['año'] == año].iloc[0]
    presidente = fila['presidente']
    
    resultado = calcular_alineamiento(año, presidente)
    if resultado is None:
        continue
    
    resultados_globales.append({
        'año': resultado['año'],
        'presidente': resultado['presidente'],
        'alineamiento_global': resultado['alineamiento_global'],
    })
    
    for tema, brecha in resultado['brechas'].items():
        resultados_brechas.append({
            'año': resultado['año'],
            'presidente': resultado['presidente'],
            'tema': tema,
            'pct_presidencial': round(resultado['presidencial'][tema], 2),
            'pct_ciudadana': round(resultado['ciudadana'][tema], 2),
            'brecha': round(brecha, 2),
        })


df_globales = pd.DataFrame(resultados_globales)
df_brechas = pd.DataFrame(resultados_brechas)

df_globales.to_csv('data/derived/alineamiento_global.csv', index=False)
df_brechas.to_csv('data/derived/alineamiento_brechas.csv', index=False)


# ============================================
# RESÚMENES
# ============================================

print("="*70)
print("ALINEAMIENTO GLOBAL POR AÑO")
print("="*70)
print(f"\n{'Año':6} {'Presidente':12} {'Alineamiento':>14}")
print("-" * 35)
for _, r in df_globales.iterrows():
    print(f"{int(r['año']):<6} {r['presidente']:12} {r['alineamiento_global']:>14.4f}")


print("\n\n" + "="*70)
print("TEMAS MÁS SOBRE-ENFATIZADOS POR EL PRESIDENTE (brecha más positiva)")
print("="*70)
top_sobre = df_brechas.nlargest(15, 'brecha')
for _, r in top_sobre.iterrows():
    print(f"  {int(r['año'])} {r['presidente']:10s} {r['tema']:20s} "
          f"pres={r['pct_presidencial']:5.1f}% vs ciu={r['pct_ciudadana']:5.1f}% "
          f"(+{r['brecha']:.2f})")


print("\n\n" + "="*70)
print("TEMAS MÁS DESATENDIDOS POR EL PRESIDENTE (brecha más negativa)")
print("="*70)
top_desat = df_brechas.nsmallest(15, 'brecha')
for _, r in top_desat.iterrows():
    print(f"  {int(r['año'])} {r['presidente']:10s} {r['tema']:20s} "
          f"pres={r['pct_presidencial']:5.1f}% vs ciu={r['pct_ciudadana']:5.1f}% "
          f"({r['brecha']:.2f})")


print("\n\nGuardado:")
print("  data/derived/alineamiento_global.csv")
print("  data/derived/alineamiento_brechas.csv")