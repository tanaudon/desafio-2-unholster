"""
Discursos presidenciales chilenos 1990-2025
Plataforma de análisis para Unholster

Página de inicio.
"""

import streamlit as st

st.set_page_config(
    page_title="Discursos presidenciales chilenos",
    page_icon="📊",
    layout="wide",
)

# ============================================
# TÍTULO
# ============================================

st.title("Discursos presidenciales chilenos 1990-2025")
st.markdown("##### Plataforma de análisis comparativo")

st.markdown("---")

# ============================================
# QUÉ ES ESTO
# ============================================

st.header("Qué es esto")

st.markdown("""
Esta plataforma analiza 35 años de discursos presidenciales chilenos: los **9 programas
de gobierno** presentados durante las campañas electorales entre 1990 y 2025, y las **36
cuentas públicas anuales** que cada presidente ha rendido al Congreso desde 1990 hasta
mayo de 2025.

El proyecto combina técnicas de procesamiento de texto con datos de opinión pública del
Centro de Estudios Públicos (CEP) para permitir distintos cruces y análisis sobre la
relación entre el discurso presidencial y la ciudadanía a lo largo del tiempo.

Esta plataforma es una propuesta de extensión del trabajo previo realizado por
[Unholster](https://discursos-presidenciales.vercel.app), agregando capas analíticas
adicionales sobre la base de la información ya disponible públicamente.
""")

st.markdown("---")

# ============================================
# FUENTES
# ============================================

st.header("Qué fuentes usa")

st.markdown("""
- **Programas presidenciales** (1990-2026): 9 documentos en PDF descargados desde el
sitio del Congreso Nacional y archivos oficiales de campaña.
- **Cuentas públicas anuales** (1990-2025): 36 documentos en PDF descargados del sitio
de la Cámara de Diputados.
- **Encuesta CEP**: base consolidada 1994-2025 que reúne 64 mediciones de opinión pública
con cobertura nacional, totalizando 94.656 entrevistas. Variables usadas:
percepción de problemas país y aprobación presidencial.
- **Análisis épicos**: scraping de la plataforma de Unholster, que generó análisis
retóricos de los 36 discursos usando Claude Sonnet 4.6.
""")

st.markdown("---")

# ============================================
# CUATRO PREGUNTAS
# ============================================

st.header("Qué preguntas permite explorar")

col1, col2 = st.columns(2)

with col1:
    st.markdown("##### 1. ¿Cumplen los gobiernos lo que prometen?")
    st.markdown("""
    Comparación entre los temas que cada gobierno prometió en su programa
    de campaña y los temas sobre los que efectivamente habló en sus cuentas
    públicas anuales.
    
    → Ver página **Fidelidad programática**.
    """)
    
    st.markdown("##### 2. ¿Hablan los gobiernos de lo que a la gente le importa?")
    st.markdown("""
    Comparación entre los temas del discurso presidencial y los problemas
    que la ciudadanía señala como prioridades en la encuesta CEP, año a año.
    
    → Ver página **Alineamiento ciudadano**.
    """)

with col2:
    st.markdown("##### 3. ¿Cómo cuentan los gobiernos su propio relato?")
    st.markdown("""
    Análisis de los marcos narrativos de los discursos: quién es el
    protagonista, contra qué se enfrenta el país, qué Chile sueña y bajo
    qué épica se cuenta el momento histórico.
    
    → Ver página **Evolución de la épica**.
    """)
    
    st.markdown("##### 4. ¿Qué pasa con el discurso tras una derrota electoral?")
    st.markdown("""
    Casos piloto que comparan cuentas públicas inmediatamente anteriores y
    posteriores a eventos electorales intermedios significativos para
    estudiar reacomodos discursivos.
    
    → Ver página **Triangulación electoral**.
    """)

st.markdown("---")

# ============================================
# MENÚ DE LECTURA
# ============================================

st.header("Cómo navegar esta plataforma")

st.markdown("""
Use el menú lateral para acceder a cada sección. Cada página tiene:
            
- **Una explicación corta** de qué se está mostrando y cómo se construyó.
- **Visualizaciones interactivas** con las que puede hacer sus propios cruces.
- **Limitaciones de la sección** explicadas en lenguaje accesible.

La página final, **Cómo leer estos datos**, reúne todas las decisiones metodológicas
del proyecto y las limitaciones generales, en lenguaje accesible.
""")

st.markdown("---")

# ============================================
# AUTORÍA Y NOTA FINAL
# ============================================

st.markdown("""
<small>

**Autor**: Tomás Naudon  

**Estado**: Esta plataforma se encuentra en construcción. Las secciones se irán
habilitando progresivamente.

</small>
""", unsafe_allow_html=True)