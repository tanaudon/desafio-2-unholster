"""
Vectorización temática: transforma cada documento del corpus en un vector
con la frecuencia de cada uno de los 16 temas.

Match por raíz para palabras simples (regex con boundary inicial).
Match exacto para frases multi-palabra.
Una mención puede contar para múltiples temas.
"""

import re
import pandas as pd
from pathlib import Path
import sys

# Importar el diccionario temático
sys.path.insert(0, str(Path(__file__).parent))
from topics import DICCIONARIO_TEMATICO


def normalizar_texto(texto):
    """
    Convierte a minúsculas y normaliza espacios.
    NO quita tildes (los términos del diccionario las preservan).
    """
    texto = texto.lower()
    # Colapsar múltiples espacios/saltos de línea en uno solo
    texto = re.sub(r'\s+', ' ', texto)
    return texto


def contar_palabras_totales(texto):
    """
    Cuenta tokens según el criterio metodológico definido:
    palabras alfabéticas de 3 o más letras (con tildes y ñ permitidas).
    Sirve como denominador para 'menciones por mil palabras'.
    """
    patron = r'\b[a-záéíóúñü]{3,}\b'
    return len(re.findall(patron, texto.lower()))


def contar_menciones_tema(texto_normalizado, terminos):
    """
    Cuenta menciones de un tema sumando matches de todos sus términos.
    
    Para términos de una sola palabra: match por raíz (la raíz seguida
    de cero o más letras dentro de la palabra). Ejemplo: 'educa' captura
    educación, educativo, educar, educadora.
    
    Para frases multi-palabra: match exacto de la secuencia.
    """
    total = 0
    for termino in terminos:
        termino_lower = termino.lower()
        
        if ' ' in termino_lower:
            # Frase multi-palabra: match exacto (con flexibilidad en espacios)
            # Escapamos caracteres especiales y permitimos múltiples espacios
            palabras = termino_lower.split()
            patron = r'\b' + r'\s+'.join(re.escape(p) for p in palabras) + r'\b'
        else:
            # Palabra simple: match por raíz
            # \b al inicio (boundary), después la raíz, después cero o más letras
            patron = r'\b' + re.escape(termino_lower) + r'[a-záéíóúñü]*\b'
        
        matches = re.findall(patron, texto_normalizado)
        total += len(matches)
    
    return total


def vectorizar_documento(ruta_txt):
    """
    Toma la ruta de un .txt, devuelve un dict con:
    - n_palabras_total (denominador)
    - menciones_absolutas por tema
    - menciones_por_mil_palabras por tema
    """
    texto = Path(ruta_txt).read_text(encoding='utf-8')
    texto_norm = normalizar_texto(texto)
    
    n_total = contar_palabras_totales(texto)
    
    resultado = {'n_palabras_total': n_total}
    
    for tema, terminos in DICCIONARIO_TEMATICO.items():
        n_menciones = contar_menciones_tema(texto_norm, terminos)
        resultado[f'menciones_{tema}'] = n_menciones
        # Menciones por mil palabras (la normalización clave)
        if n_total > 0:
            resultado[f'por_mil_{tema}'] = round(n_menciones * 1000 / n_total, 2)
        else:
            resultado[f'por_mil_{tema}'] = 0
    
    return resultado


def vectorizar_corpus():
    """
    Procesa todos los documentos del corpus y devuelve un DataFrame.
    """
    # Cargar índice del corpus
    corpus_index = pd.read_csv('data/derived/corpus_index.csv')
    
    resultados = []
    
    for _, fila in corpus_index.iterrows():
        if fila['metodo'] == 'error':
            continue
        
        tipo = fila['tipo']  # 'programa' o 'cuenta'
        carpeta = 'programas' if tipo == 'programa' else 'cuentas'
        ruta_txt = Path(f'data/processed/{carpeta}/{fila["archivo_procesado"]}')
        
        if not ruta_txt.exists():
            print(f"  ADVERTENCIA: no encontrado {ruta_txt}")
            continue
        
        print(f"  Vectorizando {fila['archivo_procesado']}...")
        
        vector = vectorizar_documento(ruta_txt)
        vector['tipo'] = tipo
        vector['año'] = fila['año']
        vector['presidente'] = fila['presidente']
        vector['archivo'] = fila['archivo_procesado']
        
        resultados.append(vector)
    
    df = pd.DataFrame(resultados)
    
    # Reordenar columnas para que la metadata vaya primero
    cols_meta = ['tipo', 'año', 'presidente', 'archivo', 'n_palabras_total']
    cols_temas = [c for c in df.columns if c not in cols_meta]
    df = df[cols_meta + sorted(cols_temas)]
    
    return df


if __name__ == "__main__":
    print("Vectorizando corpus...")
    df = vectorizar_corpus()
    
    Path('data/derived').mkdir(exist_ok=True)
    df.to_csv('data/derived/vectores_tematicos.csv', index=False)
    
    print(f"\n=== RESUMEN ===")
    print(f"Documentos vectorizados: {len(df)}")
    print(f"Programas: {(df['tipo'] == 'programa').sum()}")
    print(f"Cuentas: {(df['tipo'] == 'cuenta').sum()}")
    print(f"\nGuardado en: data/derived/vectores_tematicos.csv")