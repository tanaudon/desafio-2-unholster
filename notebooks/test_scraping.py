"""
Prueba simple: bajar el HTML de la página de épica y ver si contiene
el contenido visible (escenario A) o solo un esqueleto vacío (escenario B).
"""

import requests

# URL principal de la sección épica
url = "https://discursos-presidenciales.vercel.app/epica"

# Headers para simular un navegador real
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

print(f"Bajando: {url}")
response = requests.get(url, headers=headers, timeout=30)
print(f"Status: {response.status_code}")
print(f"Tamaño respuesta: {len(response.text):,} caracteres")
print()

# Buscar contenido que sabemos que existe en la página
fragmentos_busqueda = [
    'Aylwin',
    'reconciliación',
    'el pueblo chileno recuperando la democracia',
    'PROTAGONISTA',
    'ANTAGONISTA',
]

print("Buscando fragmentos conocidos:")
for frag in fragmentos_busqueda:
    encontrado = frag in response.text
    print(f"  '{frag}': {'✓' if encontrado else '✗'}")

# Si nada se encontró, mostrar los primeros 1000 caracteres para diagnóstico
if not any(f in response.text for f in fragmentos_busqueda):
    print("\nNo se encontraron fragmentos. Inicio del HTML recibido:")
    print(response.text[:1000])