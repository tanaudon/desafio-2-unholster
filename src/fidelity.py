"""
Cálculo de fidelidad programática:
- Divergencia Jensen-Shannon entre programa y cada cuenta pública anual.
- Divergencia entre cada cuenta y la del año anterior (continuidad inter-anual).
- Identificación de temas emergentes (en cuentas pero no programados).
- Identificación de temas abandonados (en programa pero no en cuentas).
"""

import pandas as pd
import numpy as np
from scipy.spatial.distance import jensenshannon
from pathlib import Path

# ============================================
# CARGA DE DATOS
# ============================================

df = pd.read_csv('data/derived/vectores_tematicos.csv')

# Columnas de menciones por mil palabras (uso estas para las distribuciones)
cols_por_mil = sorted([c for c in df.columns if c.startswith('por_mil_')])

# Mapeo de presidentes a sus mandatos (para vincular cuenta → programa)
# Cada tupla: (presidente, año_programa, rango_cuentas)
MANDATOS = [
    ('aylwin',   1990, range(1990, 1994)),
    ('frei',     1994, range(1994, 2000)),
    ('lagos',    2000, range(2000, 2006)),
    ('bachelet', 2006, range(2006, 2010)),  # Bachelet I
    ('pinera',   2010, range(2010, 2014)),  # Piñera I
    ('bachelet', 2014, range(2014, 2018)),  # Bachelet II
    ('pinera',   2018, range(2018, 2022)),  # Piñera II
    ('boric',    2022, range(2022, 2026)),
]

# ============================================
# FUNCIONES
# ============================================

def vector_temático(fila):
    """Extrae el vector temático (16 valores) de una fila del DataFrame."""
    return fila[cols_por_mil].values.astype(float)


def distribución(vector):
    """
    Convierte el vector a distribución de probabilidad (suma = 1).
    Si todos los valores son 0, devuelve uniforme.
    """
    total = vector.sum()
    if total == 0:
        return np.ones_like(vector) / len(vector)
    return vector / total


def fidelidad_js(vec_a, vec_b):
    """
    Calcula fidelidad como 1 - divergencia Jensen-Shannon.
    Resultado entre 0 (muy distintos) y 1 (idénticos).
    """
    dist_a = distribución(vec_a)
    dist_b = distribución(vec_b)
    # scipy.spatial.distance.jensenshannon devuelve la "distancia"
    # (raíz cuadrada de la divergencia). La elevamos al cuadrado para
    # tener divergencia entre 0 y 1, después invertimos.
    distancia = jensenshannon(dist_a, dist_b, base=2)
    divergencia = distancia ** 2
    return 1 - divergencia


# ============================================
# CÁLCULO 1: FIDELIDAD CUENTA vs PROGRAMA
# ============================================

resultados_vs_programa = []

for presidente, año_programa, rango_cuentas in MANDATOS:
    # Buscar el programa correspondiente
    programa = df[(df['tipo'] == 'programa') & 
                  (df['año'] == año_programa) & 
                  (df['presidente'] == presidente)]
    
    if programa.empty:
        print(f"ADVERTENCIA: no se encontró programa {presidente} {año_programa}")
        continue
    
    vec_programa = vector_temático(programa.iloc[0])
    
    # Buscar las cuentas de ese mandato
    for año in rango_cuentas:
        cuenta = df[(df['tipo'] == 'cuenta') & 
                    (df['año'] == año) & 
                    (df['presidente'] == presidente)]
        
        if cuenta.empty:
            continue
        
        vec_cuenta = vector_temático(cuenta.iloc[0])
        fidelidad = fidelidad_js(vec_programa, vec_cuenta)
        
        resultados_vs_programa.append({
            'presidente': presidente,
            'año_programa': año_programa,
            'año_cuenta': año,
            'año_de_mandato': año - año_programa + 1,
            'fidelidad': round(fidelidad, 4)
        })

df_vs_programa = pd.DataFrame(resultados_vs_programa)
df_vs_programa.to_csv('data/derived/fidelidad_vs_programa.csv', index=False)


# ============================================
# CÁLCULO 2: FIDELIDAD CUENTA vs CUENTA ANTERIOR
# ============================================

resultados_inter_anual = []

cuentas = df[df['tipo'] == 'cuenta'].sort_values(['presidente', 'año']).reset_index(drop=True)

# Construir mapeo (presidente, año) → vector
mapa_cuentas = {}
for _, fila in cuentas.iterrows():
    mapa_cuentas[(fila['presidente'], fila['año'])] = vector_temático(fila)

for presidente, año_programa, rango_cuentas in MANDATOS:
    años_lista = sorted([a for a in rango_cuentas if (presidente, a) in mapa_cuentas])
    
    for i in range(1, len(años_lista)):
        año_actual = años_lista[i]
        año_anterior = años_lista[i-1]
        
        vec_actual = mapa_cuentas[(presidente, año_actual)]
        vec_anterior = mapa_cuentas[(presidente, año_anterior)]
        
        fidelidad = fidelidad_js(vec_actual, vec_anterior)
        
        resultados_inter_anual.append({
            'presidente': presidente,
            'año_programa': año_programa,
            'año_cuenta': año_actual,
            'año_anterior': año_anterior,
            'continuidad_inter_anual': round(fidelidad, 4)
        })

df_inter_anual = pd.DataFrame(resultados_inter_anual)
df_inter_anual.to_csv('data/derived/continuidad_inter_anual.csv', index=False)


# ============================================
# CÁLCULO 3: TEMAS EMERGENTES Y ABANDONADOS
# ============================================

# Para cada cuenta pública: ¿qué temas se enfatizan mucho más que en el programa?
# ¿Qué temas se abandonaron?
# Usamos diferencia (cuenta - programa) en menciones por mil palabras.

resultados_temas = []

for presidente, año_programa, rango_cuentas in MANDATOS:
    programa = df[(df['tipo'] == 'programa') & 
                  (df['año'] == año_programa) & 
                  (df['presidente'] == presidente)]
    
    if programa.empty:
        continue
    
    for año in rango_cuentas:
        cuenta = df[(df['tipo'] == 'cuenta') & 
                    (df['año'] == año) & 
                    (df['presidente'] == presidente)]
        
        if cuenta.empty:
            continue
        
        for col in cols_por_mil:
            tema = col.replace('por_mil_', '')
            valor_programa = float(programa.iloc[0][col])
            valor_cuenta = float(cuenta.iloc[0][col])
            diferencia = valor_cuenta - valor_programa
            
            resultados_temas.append({
                'presidente': presidente,
                'año_programa': año_programa,
                'año_cuenta': año,
                'tema': tema,
                'en_programa': valor_programa,
                'en_cuenta': valor_cuenta,
                'diferencia': round(diferencia, 2)
            })

df_temas = pd.DataFrame(resultados_temas)
df_temas.to_csv('data/derived/desvios_tematicos.csv', index=False)


# ============================================
# RESUMEN
# ============================================

print("="*70)
print("FIDELIDAD CUENTA vs PROGRAMA")
print("="*70)
for presidente in df_vs_programa['presidente'].unique():
    sub = df_vs_programa[df_vs_programa['presidente'] == presidente]
    # Diferenciar mandatos cuando el presidente tiene varios
    for año_prog in sub['año_programa'].unique():
        sub2 = sub[sub['año_programa'] == año_prog]
        trayectoria = ", ".join([f"{r['año_cuenta']}: {r['fidelidad']:.3f}" 
                                  for _, r in sub2.iterrows()])
        print(f"\n{presidente.upper()} (programa {año_prog}):")
        print(f"  {trayectoria}")

print("\n" + "="*70)
print("TEMAS EMERGENTES MÁS FUERTES (diferencia cuenta - programa)")
print("="*70)
# Top 10 mayores diferencias positivas
top_emergentes = df_temas.nlargest(15, 'diferencia')
for _, r in top_emergentes.iterrows():
    print(f"  {r['presidente']:10s} cuenta {r['año_cuenta']}: "
          f"{r['tema']:25s} programa={r['en_programa']:5.2f} → cuenta={r['en_cuenta']:5.2f} "
          f"(+{r['diferencia']:.2f})")

print("\n" + "="*70)
print("TEMAS ABANDONADOS MÁS FUERTES (diferencia más negativa)")
print("="*70)
top_abandonos = df_temas.nsmallest(15, 'diferencia')
for _, r in top_abandonos.iterrows():
    print(f"  {r['presidente']:10s} cuenta {r['año_cuenta']}: "
          f"{r['tema']:25s} programa={r['en_programa']:5.2f} → cuenta={r['en_cuenta']:5.2f} "
          f"({r['diferencia']:.2f})")

# ============================================
# CÁLCULO 4: FIDELIDAD DE TEMAS PRINCIPALES (TOP-3)
# ============================================
# Pregunta: ¿los 3 temas que el programa enfatizó más siguen
# siendo top-3 en cada cuenta pública?

resultados_top3 = []

for presidente, año_programa, rango_cuentas in MANDATOS:
    programa = df[(df['tipo'] == 'programa') & 
                  (df['año'] == año_programa) & 
                  (df['presidente'] == presidente)]
    
    if programa.empty:
        continue
    
    # Top 3 temas del programa
    valores_programa = programa.iloc[0][cols_por_mil].sort_values(ascending=False)
    top3_programa = set([c.replace('por_mil_', '') for c in valores_programa.head(3).index])
    
    for año in rango_cuentas:
        cuenta = df[(df['tipo'] == 'cuenta') & 
                    (df['año'] == año) & 
                    (df['presidente'] == presidente)]
        
        if cuenta.empty:
            continue
        
        # Top 3 temas de la cuenta
        valores_cuenta = cuenta.iloc[0][cols_por_mil].sort_values(ascending=False)
        top3_cuenta = set([c.replace('por_mil_', '') for c in valores_cuenta.head(3).index])
        
        coincidencias = len(top3_programa & top3_cuenta)
        fidelidad_top3 = coincidencias / 3
        
        resultados_top3.append({
            'presidente': presidente,
            'año_programa': año_programa,
            'año_cuenta': año,
            'top3_programa': ', '.join(sorted(top3_programa)),
            'top3_cuenta': ', '.join(sorted(top3_cuenta)),
            'coincidencias': coincidencias,
            'fidelidad_top3': round(fidelidad_top3, 2)
        })

df_top3 = pd.DataFrame(resultados_top3)
df_top3.to_csv('data/derived/fidelidad_top3.csv', index=False)


print("\n" + "="*70)
print("FIDELIDAD TOP-3 TEMAS (¿siguen siendo top-3 en cuentas?)")
print("="*70)
for _, r in df_top3.iterrows():
    coincide_flag = "✓✓✓" if r['fidelidad_top3'] == 1.0 else ("✓✓" if r['fidelidad_top3'] >= 0.67 else "✓")
    print(f"\n{r['presidente'].upper()} {r['año_cuenta']} ({coincide_flag} {r['coincidencias']}/3):")
    print(f"  Programa top3: {r['top3_programa']}")
    print(f"  Cuenta   top3: {r['top3_cuenta']}")

print("\n\nGuardado:")
print("  data/derived/fidelidad_vs_programa.csv")
print("  data/derived/continuidad_inter_anual.csv")
print("  data/derived/desvios_tematicos.csv")