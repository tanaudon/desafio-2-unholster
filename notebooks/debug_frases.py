"""
Diagnóstico: contar manualmente menciones de frases clave en documentos
donde esperaríamos verlas, para verificar que el matching funciona.
"""

import re
from pathlib import Path

casos = [
    {
        'archivo': 'data/processed/cuentas/1990_aylwin.txt',
        'frases': ['derechos humanos', 'violaciones a los derechos humanos', 
                   'dictadura', 'detenidos desaparecidos']
    },
    {
        'archivo': 'data/processed/programas/2022_boric.txt',
        'frases': ['nueva constitución', 'proceso constituyente', 
                   'convención constitucional', 'constituci']
    },
    {
        'archivo': 'data/processed/cuentas/2020_pinera.txt',
        'frases': ['pandemia', 'covid', 'salud', 'hospital', 'vacuna']
    },
    {
        'archivo': 'data/processed/cuentas/2018_pinera.txt',
        'frases': ['niño', 'niños', 'niña', 'niñas', 'infancia']
    },
    {
        'archivo': 'data/processed/programas/2026_kast.txt',
        'frases': ['migración', 'migrant', 'inmigra', 'extranjer', 'frontera']
    },
]

for caso in casos:
    print(f"\n{'='*70}")
    print(f"{caso['archivo']}")
    print('='*70)
    
    texto = Path(caso['archivo']).read_text(encoding='utf-8').lower()
    texto = re.sub(r'\s+', ' ', texto)
    
    for frase in caso['frases']:
        # Match flexible: si tiene espacios, frase exacta; si no, raíz
        if ' ' in frase:
            palabras = frase.split()
            patron = r'\b' + r'\s+'.join(re.escape(p) for p in palabras) + r'\b'
        else:
            patron = r'\b' + re.escape(frase) + r'[a-záéíóúñü]*\b'
        
        matches = re.findall(patron, texto)
        print(f"  '{frase}': {len(matches)} matches")
        # Mostrar 3 ejemplos de contexto si hay matches
        if matches and len(matches) > 0:
            for m in re.finditer(patron, texto):
                start = max(0, m.start() - 50)
                end = min(len(texto), m.end() + 50)
                print(f"    ...{texto[start:end]}...")
                if matches.index(m.group()) == 0:
                    break