"""
Desescapar el array y parsearlo a estructura Python.
"""

from pathlib import Path
import json

array_escapado = Path('data/external/analyses_raw.txt').read_text(encoding='utf-8')

# Desescapar: las \" deben volver a ser ", y las \\ deben volver a ser \
# El método más simple: hacer un JSON-decode del string completo
# Como está escapado como si fuera un string JSON, lo envolvemos en comillas
# y lo parseamos como string, lo cual nos da el array crudo.

# Estrategia: usar json.loads sobre un string que envuelve el array como string
texto_envuelto = '"' + array_escapado + '"'

# json.loads va a interpretar las \" como " y las \\ como \
array_desescapado = json.loads(texto_envuelto)

print("Primeros 300 caracteres desescapados:")
print(array_desescapado[:300])
print()

# Ahora parsear el array como JSON real
analyses = json.loads(array_desescapado)

print(f"Total de análisis: {len(analyses)}")
print(f"\nEstructura del primer análisis (Aylwin 1990):")
print(json.dumps(analyses[0], ensure_ascii=False, indent=2)[:3000])