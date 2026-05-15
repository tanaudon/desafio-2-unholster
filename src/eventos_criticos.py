"""
Registro de los 15 eventos críticos del período 1990-2025 que se
superponen al timeline épico para contextualizar cambios discursivos.

Cada evento tiene fecha, nombre corto, tipo, y nota interpretativa
que conecta con cambios observados en marcos épicos, protagonistas
o antagonistas.
"""

import pandas as pd
from pathlib import Path

# ============================================
# EVENTOS CRÍTICOS
# ============================================

EVENTOS = [
    {
        'fecha': '1991-02-09',
        'año': 1991,
        'evento': 'Informe Rettig',
        'tipo': 'DDHH',
        'nota': 'Reconocimiento oficial de violaciones a DDHH. Refuerza antagonista "pasado autoritario" en Aylwin 1991-1992.'
    },
    {
        'fecha': '1997-07-01',
        'año': 1997,
        'evento': 'Crisis asiática',
        'tipo': 'Económico',
        'nota': 'Golpe externo al modelo. Antecede antagonista amenazas externas en Frei 1999.'
    },
    {
        'fecha': '1998-10-16',
        'año': 1998,
        'evento': 'Detención de Pinochet en Londres',
        'tipo': 'DDHH',
        'nota': 'Punto de inflexión en justicia transicional. Reactiva tematización del pasado autoritario en Frei 1999.'
    },
    {
        'fecha': '2003-04-01',
        'año': 2003,
        'evento': 'Caso MOP-Gate',
        'tipo': 'Corrupción',
        'nota': 'Escándalo de corrupción del propio gobierno. Aparece como antagonista en Lagos 2003 (único caso de corrupción institucional como adversario explícito).'
    },
    {
        'fecha': '2006-05-30',
        'año': 2006,
        'evento': 'Revolución Pingüina',
        'tipo': 'Social',
        'nota': 'Primer ciclo de movilización estudiantil postdictadura. Antecede el lenguaje de derechos sociales y "grupos excluidos" en Bachelet I.'
    },
    {
        'fecha': '2008-09-15',
        'año': 2008,
        'evento': 'Crisis financiera global',
        'tipo': 'Económico',
        'nota': 'Crisis externa que impacta al país. Conecta con antagonista amenazas externas en Bachelet 2009.'
    },
    {
        'fecha': '2010-02-27',
        'año': 2010,
        'evento': 'Terremoto y tsunami 27F',
        'tipo': 'Natural',
        'nota': 'Catástrofe que reconfigura agenda. Explica antagonista amenazas externas y aparición de Salud en Piñera 2010.'
    },
    {
        'fecha': '2011-08-04',
        'año': 2011,
        'evento': 'Movilización estudiantil universitaria',
        'tipo': 'Social',
        'nota': 'Masificación demanda por educación gratuita. Antecede el lenguaje de derechos ciudadanos que articula Bachelet II.'
    },
    {
        'fecha': '2015-03-01',
        'año': 2015,
        'evento': 'Casos Penta, SQM, Caval',
        'tipo': 'Corrupción',
        'nota': 'Crisis de confianza en política, empresa y financiamiento electoral. Coincide con período Bachelet II que tematiza "élites conservadoras" como antagonista.'
    },
    {
        'fecha': '2019-10-18',
        'año': 2019,
        'evento': 'Estallido social',
        'tipo': 'Crisis',
        'nota': 'Mayor crisis política-social desde 1990. Genera el quiebre narrativo más fuerte de la serie: transición de antagonista subdesarrollo a antagonista crisis social en Piñera 2020-2021.'
    },
    {
        'fecha': '2020-03-03',
        'año': 2020,
        'evento': 'Pandemia COVID-19 llega a Chile',
        'tipo': 'Sanitaria',
        'nota': 'Primer caso. Suma a la crisis del estallido. Convierte Salud en tema dominante de Piñera 2020-2021 (Salud sube de 7.94 a 18.05 por mil palabras).'
    },
    {
        'fecha': '2020-10-25',
        'año': 2020,
        'evento': 'Plebiscito de entrada (Apruebo)',
        'tipo': 'Institucional',
        'nota': 'Apertura del proceso constituyente. Hace de Constitución tema relevante en Piñera 2021 (sube de 1.40 a 4.30 por mil).'
    },
    {
        'fecha': '2022-09-04',
        'año': 2022,
        'evento': 'Rechazo plebiscito constitucional',
        'tipo': 'Institucional',
        'nota': 'Fracasa el primer proceso constituyente. Antecede el reacomodo discursivo de Boric 2023 (única cuenta con fidelidad top-3 = 1/3, la más baja de su serie).'
    },
    {
        'fecha': '2023-12-17',
        'año': 2023,
        'evento': 'Segundo rechazo constitucional',
        'tipo': 'Institucional',
        'nota': 'Cierra el ciclo constituyente 2019-2023 sin nueva Constitución.'
    },
    {
        'fecha': '2024-09-01',
        'año': 2024,
        'evento': 'Caso Audios / Hermosilla',
        'tipo': 'Corrupción',
        'nota': 'Crisis de confianza en justicia, élites y lobby. Coincide con discurso de Boric 2024 que cambia antagonista hacia crimen organizado.'
    },
]


# ============================================
# REGISTRO DE CAMBIOS DE GOBIERNO
# ============================================
# Para uso como bandas de fondo en la visualización

CAMBIOS_GOBIERNO = [
    {'año_inicio': 1990, 'año_fin': 1993, 'presidente': 'aylwin',   'coalicion': 'Concertación'},
    {'año_inicio': 1994, 'año_fin': 1999, 'presidente': 'frei',     'coalicion': 'Concertación'},
    {'año_inicio': 2000, 'año_fin': 2005, 'presidente': 'lagos',    'coalicion': 'Concertación'},
    {'año_inicio': 2006, 'año_fin': 2009, 'presidente': 'bachelet', 'coalicion': 'Concertación / Nueva Mayoría'},
    {'año_inicio': 2010, 'año_fin': 2013, 'presidente': 'pinera',   'coalicion': 'Coalición por el Cambio'},
    {'año_inicio': 2014, 'año_fin': 2017, 'presidente': 'bachelet', 'coalicion': 'Nueva Mayoría'},
    {'año_inicio': 2018, 'año_fin': 2021, 'presidente': 'pinera',   'coalicion': 'Chile Vamos'},
    {'año_inicio': 2022, 'año_fin': 2025, 'presidente': 'boric',    'coalicion': 'Apruebo Dignidad / Frente Amplio'},
]


def guardar():
    df_eventos = pd.DataFrame(EVENTOS)
    df_gobiernos = pd.DataFrame(CAMBIOS_GOBIERNO)
    
    Path('data/derived').mkdir(exist_ok=True)
    df_eventos.to_csv('data/derived/eventos_criticos.csv', index=False)
    df_gobiernos.to_csv('data/derived/gobiernos.csv', index=False)
    
    print(f"Eventos críticos: {len(df_eventos)}")
    print(df_eventos[['año', 'evento', 'tipo']].to_string(index=False))
    print(f"\nGobiernos: {len(df_gobiernos)}")
    print(df_gobiernos.to_string(index=False))
    print(f"\nGuardado:")
    print(f"  data/derived/eventos_criticos.csv")
    print(f"  data/derived/gobiernos.csv")


if __name__ == "__main__":
    guardar()