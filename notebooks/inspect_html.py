"""
Guarda el HTML completo de la página de épica y muestra fragmentos
relevantes para entender su estructura.
"""

import requests
from pathlib import Path

url = "https://discursos-presidenciales.vercel.app/epica"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

response = requests.get(url, headers=headers, timeout=30)

# Guardar HTML completo para inspección
Path('data/external').mkdir(parents=True, exist_ok=True)
ruta_html = 'data/external/epica_pagina.html'
Path(ruta_html).write_text(response.text, encoding='utf-8')
print(f"HTML guardado en: {ruta_html}")
print(f"Tamaño: {len(response.text):,} caracteres")

# Contar cuántas veces aparece cada presidente
print("\nApariciones por presidente:")
for nombre in ['Aylwin', 'Frei', 'Lagos', 'Bachelet', 'Piñera', 'Boric']:
    n = response.text.count(nombre)
    print(f"  {nombre}: {n}")

# Buscar palabras clave que probablemente sean etiquetas estructurales
print("\nPalabras clave estructurales (búsqueda case-insensitive):")
texto_lower = response.text.lower()
for clave in ['protagonista', 'antagonista', 'sueño', 'épica', 'metáfora', 'reconciliación', 'reparación', 'modernización']:
    n = texto_lower.count(clave)
    print(f"  '{clave}': {n}")

# Buscar primeros 500 caracteres alrededor de "el pueblo chileno"
print("\nContexto alrededor de la primera frase conocida:")
idx = response.text.find('el pueblo chileno recuperando la democracia')
if idx > -1:
    inicio = max(0, idx - 300)
    fin = min(len(response.text), idx + 500)
    print(response.text[inicio:fin])