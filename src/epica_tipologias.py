"""
Clasifica protagonistas y antagonistas de los 36 análisis épicos en
tipologías mayores. La clasificación es interpretativa, basada en
lectura de las etiquetas y descripciones generadas por Unholster.

Cada caso lleva una nota interpretativa que documenta el sentido
específico de la categoría para ese discurso.
"""

import pandas as pd
from pathlib import Path

# ============================================
# TIPOLOGÍAS
# ============================================

PROTAGONISTAS = {
    'pueblo_ciudadania': 'Pueblo / ciudadanía como sujeto histórico',
    'nacion_chile': 'Nación / Chile como entidad colectiva',
    'estado_gobierno': 'Estado / gobierno como gestor',
    'grupos_sociales': 'Grupos sociales específicos',
    'familias_individuos': 'Familias / individuos concretos',
    'otro': 'Otro / mixto',
}

ANTAGONISTAS = {
    'pasado_autoritario': 'El pasado autoritario / la dictadura',
    'condiciones_estructurales': 'Condiciones estructurales (pobreza, desigualdad, subdesarrollo)',
    'elites_conservadoras': 'Élites / fuerzas conservadoras',
    'amenazas_externas': 'Amenazas externas o globales',
    'crimen_violencia': 'Crimen organizado / delincuencia / violencia',
    'crisis_social': 'Crisis social / ruptura del pacto social',
    'corrupcion_institucional': 'Corrupción institucional',
    'sin_antagonista': 'Sin antagonista claro / abstracto',
}


# ============================================
# CLASIFICACIÓN MANUAL DE LOS 36 CASOS
# ============================================
# Formato: (id, protagonista_tipo, antagonista_tipo, nota_interpretativa)

CLASIFICACION = [
    # AYLWIN (1990-1993)
    ('discurso_1990', 'pueblo_ciudadania', 'pasado_autoritario',
     'Pueblo: la ciudadanía que recupera derechos tras 16 años. Antagonista: dictadura como pasado obstructor del futuro.'),
    ('discurso_1991', 'estado_gobierno', 'pasado_autoritario',
     'Protagonista: la institucionalidad democrática restaurada (no el pueblo, sino el gobierno gestor). Antagonista: pasado autoritario y sus herencias no resueltas.'),
    ('discurso_1992', 'nacion_chile', 'pasado_autoritario',
     'Nación reconciliada como sujeto. Antagonista: régimen autoritario como pasado a superar.'),
    ('discurso_1993', 'nacion_chile', 'pasado_autoritario',
     'Nación en transición. Antagonista: legado autoritario, especialmente enclaves institucionales (binominal, senadores designados).'),

    # FREI (1994-1999)
    ('discurso_1994', 'nacion_chile', 'condiciones_estructurales',
     'Nación con oportunidad histórica. Antagonista: subdesarrollo, pobreza, oportunidades perdidas (no actores).'),
    ('discurso_1995', 'nacion_chile', 'condiciones_estructurales',
     'Nación conducida hacia desarrollo. Antagonista: obstáculos internos (autoritarismo institucional + desigualdad + conductas regresivas).'),
    ('discurso_1996', 'nacion_chile', 'pasado_autoritario',
     'Nación en marcha. Antagonista: aún el pasado autoritario activo (caso Letelier, oposición a reformas).'),
    ('discurso_1997', 'grupos_sociales', 'condiciones_estructurales',
     'Excluidos esperando oportunidad: pobres, jóvenes, mujeres jefas de hogar. Antagonista: inequidad histórica acumulada.'),
    ('discurso_1998', 'pueblo_ciudadania', 'condiciones_estructurales',
     'Ciudadanos como agentes de progreso por esfuerzo propio. Antagonista: desigualdad heredada + rezago institucional.'),
    ('discurso_1999', 'familias_individuos', 'condiciones_estructurales',
     'Familia chilena como unidad de mejora. Antagonista doble: precariedad histórica + crisis asiática como factor externo.'),

    # LAGOS (2000-2005)
    ('discurso_2000', 'nacion_chile', 'condiciones_estructurales',
     'Chile entrando al nuevo siglo. Antagonista: división histórica + conservadurismo + brecha digital.'),
    ('discurso_2001', 'nacion_chile', 'amenazas_externas',
     'Chile unido frente a turbulencia. Antagonista: crisis económica global + pesimismo interno.'),
    ('discurso_2002', 'nacion_chile', 'condiciones_estructurales',
     'Chile productivo integrándose al mundo. Antagonista: condiciones estructurales de desarrollo pendientes.'),
    ('discurso_2003', 'nacion_chile', 'corrupcion_institucional',
     'Chile emprendedor. Antagonista: escándalos de corrupción del propio gobierno (MOP-Gate, MOP-CIADE). Primera vez que corrupción institucional aparece como antagonista discursivo central.'),
    ('discurso_2004', 'nacion_chile', 'amenazas_externas',
     'Chile emprendedor. Antagonista: adversidad económica mundial (recuperación tras crisis global).'),
    ('discurso_2005', 'nacion_chile', 'condiciones_estructurales',
     'Chile maduro hacia el siglo XXI. Antagonista: tareas pendientes de desarrollo, sin enemigo claro (cierre de mandato).'),

    # BACHELET I (2006-2009)
    ('discurso_2006', 'grupos_sociales', 'condiciones_estructurales',
     'Los excluidos que el desarrollo dejó atrás. Antagonista: brechas estructurales de la modernización chilena.'),
    ('discurso_2007', 'pueblo_ciudadania', 'condiciones_estructurales',
     'Ciudadanos con derechos sociales garantizados por el Estado. Antagonista: desigualdad estructural en provisión de derechos.'),
    ('discurso_2008', 'nacion_chile', 'condiciones_estructurales',
     'Chile unido construyendo acuerdos. Antagonista: brechas pendientes hacia el bicentenario.'),
    ('discurso_2009', 'pueblo_ciudadania', 'amenazas_externas',
     'El pueblo chileno protegido por el Estado. Antagonista: crisis financiera internacional 2008-2009.'),

    # PIÑERA I (2010-2013)
    ('discurso_2010', 'nacion_chile', 'amenazas_externas',
     'Nación golpeada que se levanta. Antagonista: terremoto 27F y sus consecuencias (tratado como amenaza externa/catástrofe).'),
    ('discurso_2011', 'nacion_chile', 'condiciones_estructurales',
     'Generación del Bicentenario como comunidad nacional temporal (no grupo sociológico). Antagonista: subdesarrollo como condición a superar.'),
    ('discurso_2012', 'grupos_sociales', 'condiciones_estructurales',
     'Clase media y vulnerable como grupo social específico (no nación entera). Antagonista: condiciones de desarrollo desigual.'),
    ('discurso_2013', 'nacion_chile', 'condiciones_estructurales',
     'Chile en marcha al desarrollo prometido. Antagonista: tareas pendientes (sin enemigo concreto, cierre de mandato).'),

    # BACHELET II (2014-2017)
    ('discurso_2014', 'pueblo_ciudadania', 'elites_conservadoras',
     'Ciudadanía que exige derechos (reformas estructurales: tributaria, educacional, constitucional). Antagonista: élites que bloquean transformaciones.'),
    ('discurso_2015', 'pueblo_ciudadania', 'elites_conservadoras',
     'Ciudadanía que demanda en democracia madura. Antagonista: oposición que resiste reformas.'),
    ('discurso_2016', 'pueblo_ciudadania', 'elites_conservadoras',
     'Ciudadanía exigiendo reformas urgentes. Antagonista: bloqueos al programa reformista.'),
    ('discurso_2017', 'pueblo_ciudadania', 'condiciones_estructurales',
     'Ciudadanía que exige transformaciones postergadas. Antagonista: desigualdad como condición estructural (cierre de mandato).'),

    # PIÑERA II (2018-2021)
    ('discurso_2018', 'nacion_chile', 'condiciones_estructurales',
     'Generación del Bicentenario llamada al desarrollo (similar a 2011, comunidad nacional temporal). Antagonista: subdesarrollo, sin agenda de crimen aún.'),
    ('discurso_2019', 'nacion_chile', 'condiciones_estructurales',
     'Chile en marcha al desarrollo. Antagonista: subdesarrollo. Importante: este discurso es de junio 2019, anterior al estallido de octubre.'),
    ('discurso_2020', 'pueblo_ciudadania', 'crisis_social',
     'El pueblo chileno resiliente ante adversidades acumuladas. Antagonista: crisis múltiple (estallido + pandemia) como ruptura del pacto social y emergencia simultánea.'),
    ('discurso_2021', 'nacion_chile', 'crisis_social',
     'Chile resistiendo cuatro crisis superpuestas. Antagonista: convergencia de crisis sociales, sanitarias y económicas.'),

    # BORIC (2022-2025)
    ('discurso_2022', 'grupos_sociales', 'condiciones_estructurales',
     'Marginados que la transición postergó y el estallido expresó (sujeto plural específico). Antagonista: desigualdad estructural acumulada por décadas.'),
    ('discurso_2023', 'pueblo_ciudadania', 'crisis_social',
     'Ciudadanos golpeados por crisis que el Estado debe alcanzar. Antagonista: crisis social y de confianza post-Rechazo constitucional.'),
    ('discurso_2024', 'grupos_sociales', 'crimen_violencia',
     'Mayoría trabajadora y honesta que merece bienestar. Antagonista: crimen organizado y violencia (giro de agenda explícito).'),
    ('discurso_2025', 'estado_gobierno', 'condiciones_estructurales',
     'El progresismo que gobierna cediendo sin claudicar (sujeto: el gobierno como agente). Antagonista: tareas pendientes, sin enemigo concreto (cierre de mandato).'),
]


# ============================================
# APLICAR CLASIFICACIÓN
# ============================================

def aplicar_clasificacion():
    df = pd.read_csv('data/derived/epica_analyses.csv')
    
    df_clas = pd.DataFrame(CLASIFICACION, columns=[
        'id', 'protagonista_tipo', 'antagonista_tipo', 'nota_interpretativa'
    ])
    
    df_final = df.merge(df_clas, on='id', how='left')
    df_final['protagonista_tipo_label'] = df_final['protagonista_tipo'].map(PROTAGONISTAS)
    df_final['antagonista_tipo_label'] = df_final['antagonista_tipo'].map(ANTAGONISTAS)
    
    ruta = 'data/derived/epica_clasificada.csv'
    df_final.to_csv(ruta, index=False)
    
    print(f"Guardado: {ruta}\n")
    print("="*70)
    print("DISTRIBUCIÓN DE PROTAGONISTAS")
    print("="*70)
    print(df_final['protagonista_tipo_label'].value_counts().to_string())
    
    print("\n" + "="*70)
    print("DISTRIBUCIÓN DE ANTAGONISTAS")
    print("="*70)
    print(df_final['antagonista_tipo_label'].value_counts().to_string())
    
    print("\n" + "="*70)
    print("TRAYECTORIA POR AÑO")
    print("="*70)
    df_ordenado = df_final.sort_values('año')
    for _, r in df_ordenado.iterrows():
        print(f"  {r['año']} {r['presidente']:10s}: "
              f"P={r['protagonista_tipo']:20s} A={r['antagonista_tipo']}")


if __name__ == "__main__":
    aplicar_clasificacion()