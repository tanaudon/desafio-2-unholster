"""
Sección 4: triangulación electoral.

Para cada caso de derrota electoral intermedia identificado, compara:
- La cuenta pública ANTERIOR al evento electoral.
- La cuenta pública POSTERIOR al evento.

Métricas calculadas:
1. Alineamiento de cada cuenta con la agenda ciudadana CEP del año.
2. Cambio en alineamiento (posterior - anterior).
3. Cambios temáticos específicos: qué temas suben/bajan tras la derrota.
"""

import pandas as pd
import numpy as np
from scipy.spatial.distance import jensenshannon

# ============================================
# CASOS
# ============================================

CASOS = [
    {
        'id': 'bachelet2_2016',
        'descripcion': 'Bachelet II tras municipales 2016',
        'evento': 'Municipales 2016 (Nueva Mayoría pierde votación)',
        'fecha_evento': '2016-10-23',
        'presidente': 'bachelet',
        'cuenta_anterior_año': 2016,  # cuenta de mayo 2016 (anterior a octubre)
        'cuenta_posterior_año': 2017,  # cuenta de junio 2017 (posterior)
    },
    {
        'id': 'pinera2_2020',
        'descripcion': 'Piñera II tras plebiscito de entrada 2020',
        'evento': 'Plebiscito 2020 (Apruebo gana 78%)',
        'fecha_evento': '2020-10-25',
        'presidente': 'pinera',
        'cuenta_anterior_año': 2019,  # junio 2019 (CEP 2020 no existe por pandemia)
        'cuenta_posterior_año': 2021,  # junio 2021
        'nota_metodologica': 'CEP no realizó encuestas en 2020. Se usa 2019 como anterior. El gap mayor abarca también el estallido y la pandemia.'
    },
    {
        'id': 'boric_2022',
        'descripcion': 'Boric tras Rechazo plebiscitario 2022',
        'evento': 'Plebiscito de salida (Rechazo gana 62%)',
        'fecha_evento': '2022-09-04',
        'presidente': 'boric',
        'cuenta_anterior_año': 2022,  # junio 2022
        'cuenta_posterior_año': 2023,  # junio 2023
    },
]

# Temas que comparamos (los mismos del alineamiento)
TEMAS_COMPARABLES = [
    'Constitución', 'Corrupción', 'Derechos humanos', 'Desigualdad',
    'Economía', 'Educación', 'Medio ambiente', 'Migración',
    'Pensiones', 'Pobreza', 'Salud', 'Seguridad',
    'Trabajo/Empleo', 'Vivienda',
]


# ============================================
# CARGA
# ============================================

vectores = pd.read_csv('data/derived/vectores_tematicos.csv')
agenda = pd.read_csv('data/derived/agenda_ciudadana.csv')
alineamiento = pd.read_csv('data/derived/alineamiento_global.csv')


def normalizar(valores):
    total = sum(valores.values())
    if total == 0:
        return {k: 0 for k in valores}
    return {k: (v / total) * 100 for k, v in valores.items()}


def jensen_shannon(vec_a, vec_b):
    """Devuelve 1 - distancia^2 (alineamiento entre 0 y 1)."""
    a = np.array(vec_a)
    b = np.array(vec_b)
    if a.sum() > 0:
        a = a / a.sum()
    else:
        a = np.ones_like(a) / len(a)
    if b.sum() > 0:
        b = b / b.sum()
    else:
        b = np.ones_like(b) / len(b)
    dist = jensenshannon(a, b, base=2)
    return 1 - (dist ** 2)


def calcular_caso(caso):
    """Calcula métricas antes/después para un caso."""
    presidente = caso['presidente']
    año_ant = caso['cuenta_anterior_año']
    año_pos = caso['cuenta_posterior_año']
    
    # Cuentas presidenciales
    c_ant = vectores[(vectores['tipo'] == 'cuenta') & 
                     (vectores['año'] == año_ant) & 
                     (vectores['presidente'] == presidente)]
    c_pos = vectores[(vectores['tipo'] == 'cuenta') & 
                     (vectores['año'] == año_pos) & 
                     (vectores['presidente'] == presidente)]
    
    if c_ant.empty or c_pos.empty:
        print(f"  ADVERTENCIA: no encontrada cuenta {año_ant} o {año_pos}")
        return None
    
    # Vectores temáticos sobre temas comparables
    vec_pres_ant = {t: float(c_ant.iloc[0][f'por_mil_{t}']) for t in TEMAS_COMPARABLES}
    vec_pres_pos = {t: float(c_pos.iloc[0][f'por_mil_{t}']) for t in TEMAS_COMPARABLES}
    
    # Agenda ciudadana
    ag_ant = agenda[agenda['año'] == año_ant]
    ag_pos = agenda[agenda['año'] == año_pos]
    
    if ag_ant.empty or ag_pos.empty:
        print(f"  ADVERTENCIA: no encontrada agenda ciudadana {año_ant} o {año_pos}")
        return None
    
    vec_ciu_ant = {t: float(ag_ant.iloc[0][t]) if t in ag_ant.columns else 0 for t in TEMAS_COMPARABLES}
    vec_ciu_pos = {t: float(ag_pos.iloc[0][t]) if t in ag_pos.columns else 0 for t in TEMAS_COMPARABLES}
    
    # Normalizar todo a porcentajes
    pres_ant_pct = normalizar(vec_pres_ant)
    pres_pos_pct = normalizar(vec_pres_pos)
    ciu_ant_pct = normalizar(vec_ciu_ant)
    ciu_pos_pct = normalizar(vec_ciu_pos)
    
    # Alineamientos
    align_ant = jensen_shannon(
        [pres_ant_pct[t] for t in TEMAS_COMPARABLES],
        [ciu_ant_pct[t] for t in TEMAS_COMPARABLES]
    )
    align_pos = jensen_shannon(
        [pres_pos_pct[t] for t in TEMAS_COMPARABLES],
        [ciu_pos_pct[t] for t in TEMAS_COMPARABLES]
    )
    
    cambio_align = align_pos - align_ant
    
    # Cambios temáticos en el discurso presidencial
    cambios_temas = []
    for tema in TEMAS_COMPARABLES:
        delta_pres = pres_pos_pct[tema] - pres_ant_pct[tema]
        delta_ciu = ciu_pos_pct[tema] - ciu_ant_pct[tema]
        cambios_temas.append({
            'tema': tema,
            'pres_antes': round(pres_ant_pct[tema], 2),
            'pres_despues': round(pres_pos_pct[tema], 2),
            'delta_presidente': round(delta_pres, 2),
            'ciu_antes': round(ciu_ant_pct[tema], 2),
            'ciu_despues': round(ciu_pos_pct[tema], 2),
            'delta_ciudadania': round(delta_ciu, 2),
        })
    
    return {
        'caso': caso,
        'align_antes': round(align_ant, 4),
        'align_despues': round(align_pos, 4),
        'cambio_align': round(cambio_align, 4),
        'cambios_temas': cambios_temas,
    }


# ============================================
# EJECUCIÓN
# ============================================

print("="*70)
print("TRIANGULACIÓN ELECTORAL: 3 CASOS PILOTO")
print("="*70)

resultados = []
for caso in CASOS:
    print(f"\n--- {caso['descripcion']} ---")
    print(f"Evento: {caso['evento']}")
    print(f"Cuenta anterior: {caso['cuenta_anterior_año']} | Cuenta posterior: {caso['cuenta_posterior_año']}")
    
    r = calcular_caso(caso)
    if r is None:
        continue
    
    print(f"\nAlineamiento ANTES del evento:    {r['align_antes']:.4f}")
    print(f"Alineamiento DESPUÉS del evento:  {r['align_despues']:.4f}")
    print(f"Cambio: {r['cambio_align']:+.4f} "
          f"({'acercamiento' if r['cambio_align'] > 0 else 'alejamiento'})")
    
    print(f"\nTop 5 temas que MÁS SUBIERON en discurso presidencial:")
    temas_sub = sorted(r['cambios_temas'], key=lambda x: x['delta_presidente'], reverse=True)[:5]
    for t in temas_sub:
        print(f"  {t['tema']:18s}: {t['pres_antes']:5.1f}% → {t['pres_despues']:5.1f}% "
              f"({t['delta_presidente']:+.2f}) | Ciudadanía: {t['ciu_antes']:5.1f}% → {t['ciu_despues']:5.1f}%")
    
    print(f"\nTop 5 temas que MÁS BAJARON en discurso presidencial:")
    temas_baj = sorted(r['cambios_temas'], key=lambda x: x['delta_presidente'])[:5]
    for t in temas_baj:
        print(f"  {t['tema']:18s}: {t['pres_antes']:5.1f}% → {t['pres_despues']:5.1f}% "
              f"({t['delta_presidente']:+.2f}) | Ciudadanía: {t['ciu_antes']:5.1f}% → {t['ciu_despues']:5.1f}%")
    
    resultados.append(r)

# Guardar resumen
df_resumen = pd.DataFrame([{
    'caso_id': r['caso']['id'],
    'descripcion': r['caso']['descripcion'],
    'evento': r['caso']['evento'],
    'cuenta_anterior_año': r['caso']['cuenta_anterior_año'],
    'cuenta_posterior_año': r['caso']['cuenta_posterior_año'],
    'align_antes': r['align_antes'],
    'align_despues': r['align_despues'],
    'cambio_align': r['cambio_align'],
} for r in resultados])

df_resumen.to_csv('data/derived/triangulacion_resumen.csv', index=False)

# Guardar detalle de cambios temáticos
filas_detalle = []
for r in resultados:
    for t in r['cambios_temas']:
        filas_detalle.append({
            'caso_id': r['caso']['id'],
            'descripcion': r['caso']['descripcion'],
            **t
        })
df_detalle = pd.DataFrame(filas_detalle)
df_detalle.to_csv('data/derived/triangulacion_detalle.csv', index=False)

print("\n\n" + "="*70)
print("RESUMEN GENERAL")
print("="*70)
print(df_resumen[['descripcion', 'align_antes', 'align_despues', 'cambio_align']].to_string(index=False))

print("\nGuardado:")
print("  data/derived/triangulacion_resumen.csv")
print("  data/derived/triangulacion_detalle.csv")