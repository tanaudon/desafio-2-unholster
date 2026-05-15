"""
Extrae los análisis épicos de la plataforma Unholster.
Hace scraping del HTML público, extrae el JSON embebido, y lo guarda
como CSV estructurado para análisis posterior.
"""

import requests
import json
import re
import pandas as pd
from pathlib import Path

URL = "https://discursos-presidenciales.vercel.app/epica"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}


def descargar_html():
    """Baja el HTML de la página de épica."""
    print(f"Descargando {URL}...")
    response = requests.get(URL, headers=HEADERS, timeout=30)
    response.raise_for_status()
    print(f"  {len(response.text):,} caracteres recibidos")
    return response.text


def extraer_analyses(html):
    """Extrae el array 'analyses' del HTML y lo parsea como Python."""
    match = re.search(r'\\"analyses\\":\[', html)
    if not match:
        raise ValueError("No se encontró el array 'analyses' en el HTML")
    
    inicio_array = match.end() - 1
    
    profundidad = 0
    pos = inicio_array
    escape_siguiente = False
    
    while pos < len(html):
        c = html[pos]
        
        if escape_siguiente:
            escape_siguiente = False
            pos += 1
            continue
        
        if c == '\\':
            escape_siguiente = True
            pos += 1
            continue
        
        if c == '[':
            profundidad += 1
        elif c == ']':
            profundidad -= 1
            if profundidad == 0:
                fin_array = pos + 1
                break
        pos += 1
    
    array_escapado = html[inicio_array:fin_array]
    array_desescapado = json.loads('"' + array_escapado + '"')
    analyses = json.loads(array_desescapado)
    
    return analyses


def aplanar_analisis(analisis):
    """Convierte un análisis anidado en un dict plano para CSV."""
    return {
        'id': analisis['id'],
        'año': analisis['year'],
        'presidente': analisis['label'].lower(),
        'protagonista_etiqueta': analisis['protagonista']['etiqueta'],
        'protagonista_descripcion': analisis['protagonista']['descripcion'],
        'protagonista_citas': ' || '.join(analisis['protagonista'].get('evidencia', [])),
        'antagonista_etiqueta': analisis['antagonista']['etiqueta'],
        'antagonista_descripcion': analisis['antagonista']['descripcion'],
        'antagonista_citas': ' || '.join(analisis['antagonista'].get('evidencia', [])),
        'sueno_etiqueta': analisis['sueno']['etiqueta'],
        'sueno_descripcion': analisis['sueno']['descripcion'],
        'sueno_citas': ' || '.join(analisis['sueno'].get('evidencia', [])),
        'epica_marco': analisis['epica']['marco'],
        'epica_descripcion': analisis['epica']['descripcion'],
        'epica_citas': ' || '.join(analisis['epica'].get('evidencia', [])),
        'metafora_central': analisis.get('metafora_central', ''),
    }


def main():
    html = descargar_html()
    
    print("\nExtrayendo análisis...")
    analyses = extraer_analyses(html)
    print(f"  {len(analyses)} análisis extraídos")
    
    print("\nAplanando estructura...")
    filas = [aplanar_analisis(a) for a in analyses]
    df = pd.DataFrame(filas)
    df = df.sort_values('año').reset_index(drop=True)
    
    Path('data/derived').mkdir(exist_ok=True)
    ruta_csv = 'data/derived/epica_analyses.csv'
    df.to_csv(ruta_csv, index=False)
    
    print(f"\nGuardado: {ruta_csv}")
    print(f"\nResumen:")
    print(f"  Total análisis: {len(df)}")
    print(f"  Rango años: {df['año'].min()} - {df['año'].max()}")
    print(f"  Presidentes: {df['presidente'].value_counts().to_dict()}")
    print(f"\nMarcos épicos encontrados:")
    print(df['epica_marco'].value_counts().to_string())


if __name__ == "__main__":
    main()