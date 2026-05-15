import pdfplumber
from pdf2image import convert_from_path
import pytesseract
from pathlib import Path
import pandas as pd
import time

# ============================================
# CONFIGURACIÓN
# ============================================

# Archivos que sabemos que requieren OCR (del diagnóstico previo)
ARCHIVOS_OCR_FORZADO = {
    'programas/1990_Programa_Aylwin.pdf',
    'programas/1994_Programa_Frei.pdf',
    'cuentas/19960521.pdf',
    'cuentas/19970521.pdf',
}

# Mapeo año → presidente para cuentas públicas
AÑO_A_PRESIDENTE = {
    range(1990, 1994): 'aylwin',
    range(1994, 2000): 'frei',
    range(2000, 2006): 'lagos',
    range(2006, 2010): 'bachelet',
    range(2010, 2014): 'pinera',
    range(2014, 2018): 'bachelet',
    range(2018, 2022): 'pinera',
    range(2022, 2026): 'boric',
}

def año_a_presidente(año):
    for rango, presidente in AÑO_A_PRESIDENTE.items():
        if año in rango:
            return presidente
    return 'desconocido'

# ============================================
# FUNCIONES DE EXTRACCIÓN
# ============================================

def extraer_con_pdfplumber(ruta_pdf):
    """Extrae texto con pdfplumber. Rápido pero requiere capa de texto."""
    texto_total = []
    with pdfplumber.open(ruta_pdf) as pdf:
        for pagina in pdf.pages:
            texto = pagina.extract_text()
            if texto:
                texto_total.append(texto)
    return "\n\n".join(texto_total)

def extraer_con_ocr(ruta_pdf):
    """Extrae texto con OCR. Lento pero funciona con escaneos."""
    imagenes = convert_from_path(ruta_pdf, dpi=400)
    print(f"    OCR sobre {len(imagenes)} páginas...", end=' ', flush=True)
    texto_total = []
    for i, imagen in enumerate(imagenes, 1):
        texto = pytesseract.image_to_string(imagen, lang='spa', config='--psm 1')
        texto_total.append(texto)
        if i % 10 == 0:
            print(f"{i}", end=' ', flush=True)
    print("(listo)")
    return "\n\n".join(texto_total)

# ============================================
# PROCESAMIENTO
# ============================================

# Asegurar que existen las carpetas de salida
Path('data/processed/programas').mkdir(parents=True, exist_ok=True)
Path('data/processed/cuentas').mkdir(parents=True, exist_ok=True)
Path('data/derived').mkdir(parents=True, exist_ok=True)

resultados = []
inicio_total = time.time()

# Procesar programas
print("\n" + "="*60)
print("PROGRAMAS DE GOBIERNO")
print("="*60)

programas = sorted(Path('data/raw/programas').glob('*.pdf'))
for pdf_path in programas:
    nombre_corto = f"programas/{pdf_path.name}"
    
    # Extraer año y presidente del nombre del archivo
    # Formato: AÑO_Programa_Apellido.pdf
    partes = pdf_path.stem.split('_')
    año = int(partes[0])
    presidente = partes[2].lower()
    
    print(f"\n[{pdf_path.name}]")
    
    metodo = 'ocr' if nombre_corto in ARCHIVOS_OCR_FORZADO else 'pdfplumber'
    inicio = time.time()
    
    try:
        if metodo == 'ocr':
            texto = extraer_con_ocr(pdf_path)
        else:
            texto = extraer_con_pdfplumber(pdf_path)
        
        duracion = time.time() - inicio
        n_palabras = len(texto.split())
        
        # Guardar archivo de texto
        ruta_salida = Path(f'data/processed/programas/{año}_{presidente}.txt')
        ruta_salida.write_text(texto, encoding='utf-8')
        
        print(f"  → {metodo}, {n_palabras} palabras, {duracion:.0f}s")
        
        resultados.append({
            'tipo': 'programa',
            'año': año,
            'presidente': presidente,
            'archivo_origen': pdf_path.name,
            'archivo_procesado': ruta_salida.name,
            'metodo': metodo,
            'n_palabras': n_palabras,
            'duracion_segundos': round(duracion, 1)
        })
    except Exception as e:
        print(f"  → ERROR: {e}")
        resultados.append({
            'tipo': 'programa', 'año': año, 'presidente': presidente,
            'archivo_origen': pdf_path.name, 'archivo_procesado': None,
            'metodo': 'error', 'n_palabras': 0, 'duracion_segundos': 0
        })

# Procesar cuentas públicas
print("\n" + "="*60)
print("CUENTAS PÚBLICAS")
print("="*60)

cuentas = sorted(Path('data/raw/cuentas').glob('*.pdf'))
for pdf_path in cuentas:
    nombre_corto = f"cuentas/{pdf_path.name}"
    
    # Formato: AAAAMMDD.pdf
    año = int(pdf_path.stem[:4])
    presidente = año_a_presidente(año)
    
    print(f"\n[{pdf_path.name}]")
    
    metodo = 'ocr' if nombre_corto in ARCHIVOS_OCR_FORZADO else 'pdfplumber'
    inicio = time.time()
    
    try:
        if metodo == 'ocr':
            texto = extraer_con_ocr(pdf_path)
        else:
            texto = extraer_con_pdfplumber(pdf_path)
        
        duracion = time.time() - inicio
        n_palabras = len(texto.split())
        
        ruta_salida = Path(f'data/processed/cuentas/{año}_{presidente}.txt')
        ruta_salida.write_text(texto, encoding='utf-8')
        
        print(f"  → {metodo}, {n_palabras} palabras, {duracion:.0f}s")
        
        resultados.append({
            'tipo': 'cuenta',
            'año': año,
            'presidente': presidente,
            'archivo_origen': pdf_path.name,
            'archivo_procesado': ruta_salida.name,
            'metodo': metodo,
            'n_palabras': n_palabras,
            'duracion_segundos': round(duracion, 1)
        })
    except Exception as e:
        print(f"  → ERROR: {e}")
        resultados.append({
            'tipo': 'cuenta', 'año': año, 'presidente': presidente,
            'archivo_origen': pdf_path.name, 'archivo_procesado': None,
            'metodo': 'error', 'n_palabras': 0, 'duracion_segundos': 0
        })

# ============================================
# RESUMEN Y GUARDADO
# ============================================

duracion_total = time.time() - inicio_total

df = pd.DataFrame(resultados)
df.to_csv('data/derived/corpus_index.csv', index=False)

print("\n" + "="*60)
print("RESUMEN FINAL")
print("="*60)
print(f"Total archivos procesados: {len(df)}")
print(f"  Programas: {(df['tipo'] == 'programa').sum()}")
print(f"  Cuentas: {(df['tipo'] == 'cuenta').sum()}")
print(f"Métodos usados:")
print(f"  pdfplumber: {(df['metodo'] == 'pdfplumber').sum()}")
print(f"  ocr: {(df['metodo'] == 'ocr').sum()}")
print(f"  errores: {(df['metodo'] == 'error').sum()}")
print(f"\nTotal palabras en corpus: {df['n_palabras'].sum():,}")
print(f"Tiempo total: {duracion_total/60:.1f} minutos")
print(f"\nÍndice guardado en: data/derived/corpus_index.csv")
print(f"Textos guardados en: data/processed/{{programas,cuentas}}/")