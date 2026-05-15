"""
Verifica hipótesis interpretativas sobre temas emergentes específicos
inspeccionando el contexto textual.
"""

import re
from pathlib import Path


def buscar_contexto(ruta, palabras, max_contextos=5, ventana=80):
    """Busca palabras en el texto y muestra contexto."""
    texto = Path(ruta).read_text(encoding='utf-8').lower()
    texto = re.sub(r'\s+', ' ', texto)
    
    contextos_encontrados = []
    
    for palabra in palabras:
        if ' ' in palabra:
            palabras_split = palabra.lower().split()
            patron = r'\b' + r'\s+'.join(re.escape(p) for p in palabras_split) + r'\b'
        else:
            patron = r'\b' + re.escape(palabra.lower()) + r'[a-záéíóúñü]*\b'
        
        for m in re.finditer(patron, texto):
            start = max(0, m.start() - ventana)
            end = min(len(texto), m.end() + ventana)
            contextos_encontrados.append((palabra, texto[start:end]))
            if len(contextos_encontrados) >= max_contextos:
                return contextos_encontrados
    
    return contextos_encontrados


casos = [
    {
        'titulo': 'PIÑERA 2010 (Salud +5.41): hipótesis terremoto 27F',
        'archivo': 'data/processed/cuentas/2010_pinera.txt',
        'palabras': ['terremoto', 'reconstrucción', 'tsunami', '27 de febrero', 
                     'hospital', 'damnificados']
    },
    {
        'titulo': 'BACHELET 2017 (Vivienda +3.43): contexto',
        'archivo': 'data/processed/cuentas/2017_bachelet.txt',
        'palabras': ['vivienda', 'subsidio habitacional', 'campamento',
                     'incendio', 'valparaíso']
    },
    {
        'titulo': 'AYLWIN 1991 (Seguridad +3.42): hipótesis violencia política residual',
        'archivo': 'data/processed/cuentas/1991_aylwin.txt',
        'palabras': ['terrorismo', 'fpmr', 'lautaro', 'frente patriótico',
                     'violencia política', 'atentado']
    },
]

for caso in casos:
    print(f"\n{'='*70}")
    print(caso['titulo'])
    print('='*70)
    
    resultados = buscar_contexto(caso['archivo'], caso['palabras'])
    
    if not resultados:
        print("  (sin contextos encontrados)")
    else:
        for palabra, contexto in resultados:
            print(f"\n  [{palabra}]")
            print(f"  ...{contexto}...")