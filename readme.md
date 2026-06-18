# Programas y Discursos Presidenciales de Chile

Extensión analítica de la plataforma pública de discursos presidenciales de Unholster. Convierte una herramienta descriptiva ("qué dice cada discurso") en una herramienta analítica para hacerse mejores preguntas sobre la representación democrática en Chile, cruzando lo prometido, lo ejecutado y lo que pide la ciudadanía.

**App en vivo:** https://programas-discursos-cl.streamlit.app

## El problema

La plataforma original mostraba el contenido de cada discurso, pero no permitía cruces analíticos profundos: ¿cómo se compara el discurso con la opinión ciudadana?, ¿hay patrones sistemáticos entre lo prometido y lo ejecutado?, ¿qué marcos narrativos dominan en cada época? Este proyecto agrega esas capas.

## Las cuatro preguntas

1. **Fidelidad programática** — ¿Cuánto se desvía cada gobierno de su programa de campaña en sus cuentas públicas anuales?
2. **Alineamiento ciudadano** — ¿Qué brecha existe entre lo que dicen los presidentes y lo que pide la ciudadanía (encuesta CEP)?
3. **Marcos narrativos (épica)** — ¿Qué protagonistas, antagonistas y metáforas estructuran los discursos, y cómo se relacionan con los eventos críticos del período?
4. **Cómo leer estos datos** — Decisiones metodológicas, limitaciones y guía de interpretación.

## Hallazgos principales

- La Economía es sobre-prometida en los programas y reducida en las cuentas públicas en **8 de 8** gobiernos analizados.
- Dos agendas con focos invertidos: los presidentes hablan del proyecto-país (Economía, Educación, Constitución); la ciudadanía, de su vida cotidiana (Seguridad, Trabajo, Pobreza).
- Corrupción es la gran ausencia: el único tema donde la ciudadanía habla más que el presidente en **31 de 31** años.
- Correlación negativa entre alineamiento y aprobación (**r = -0.53, p = 0.002**): los gobiernos más alineados con la agenda ciudadana tienden a ser los menos populares.

## Cómo está construido

**Stack:** Python · Streamlit (app + deploy en Streamlit Cloud) · Pandas · Plotly · pdfplumber + Tesseract (OCR) · requests (scraping)

**Métodos analíticos:**
- Diccionario temático de **19 categorías** para clasificar menciones (matching por raíz para términos simples, coincidencia exacta para frases compuestas).
- Similitud de **Jensen-Shannon** para comparar distribuciones temáticas (programa vs cuenta, discurso vs ciudadanía).
- Correlaciones de **Pearson y Spearman** entre alineamiento y aprobación.
- **Ponderación poblacional** (variable `pond` de la CEP) para que la agenda ciudadana represente a Chile y no a la muestra cruda.

## Estructura del repositorio

```
.streamlit/        Configuración de la app (tema visual)
data/              Datos crudos y derivados (17 CSV en data/derived/)
notebooks/         Notebooks de verificación de patrones y chequeos contra los datos
pages/             Páginas de la aplicación Streamlit
src/               Código fuente (topics.py: diccionario temático de 19 categorías)
streamlit_app.py   Punto de entrada de la aplicación
requirements.txt   Dependencias
```

## Cómo ejecutarlo localmente

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

## Datos y fuentes

- 45 documentos presidenciales (programas de campaña y cuentas públicas).
- 94.656 entrevistas de la encuesta CEP para reconstruir la agenda ciudadana.
- 15 eventos críticos del período (estallido social, terremoto 27F, plebiscitos, pandemia, etc.).
- Cobertura de ~35 años de historia presidencial.

Extracción de texto: 91% directa con pdfplumber, 9% vía OCR (Tesseract) para documentos escaneados antiguos.

## Nota sobre el uso de IA

Los análisis de marcos narrativos (protagonista, antagonista, metáfora) provienen de la plataforma original de Unholster, generados con un modelo de lenguaje. El aporte de este proyecto fue construir el aparato analítico sobre ellos: una tipología que agrupa los marcos en categorías cuantificables y su cruce con los eventos críticos. El análisis cuantitativo (clasificación temática, distancias, correlaciones) no usa LLMs: se apoya en métodos trazables y verificables.

## Limitaciones

Las limitaciones (tramos de datos, periodos cubiertos, supuestos de clasificación) están documentadas en detalle en la página "Cómo leer estos datos" de la aplicación. El criterio de diseño fue declarar explícitamente lo que los datos no permiten afirmar.

## Autor

Tomás Naudon
