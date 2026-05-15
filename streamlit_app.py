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
# CSS PERSONALIZADO PARA REFINAR DETALLES
# ============================================

st.markdown("""
<style>
    /* Reducir padding superior */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1100px;
    }
    
    /* Estilo del título principal */
    .main-title {
        font-size: 2.6rem;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 0.3rem;
        line-height: 1.1;
    }
    
    .subtitle {
        font-size: 1.1rem;
        color: #475569;
        margin-bottom: 2rem;
        font-weight: 400;
    }
    
    /* Bloques de métricas */
    .metric-box {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 1.3rem 1rem;
        text-align: center;
    }
    
    .metric-number {
        font-size: 2rem;
        font-weight: 700;
        color: #1e40af;
        line-height: 1;
        margin-bottom: 0.3rem;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #64748b;
    }
    
    /* Tarjetas de pregunta */
    .question-card {
        background-color: #f8fafc;
        border-left: 4px solid #1e40af;
        border-radius: 6px;
        padding: 1.2rem 1.4rem;
        margin-bottom: 1rem;
        height: 100%;
    }
    
    .question-title {
        font-size: 1.05rem;
        font-weight: 600;
        color: #0f172a;
        margin-bottom: 0.5rem;
    }
    
    .question-text {
        font-size: 0.95rem;
        color: #334155;
        line-height: 1.5;
        margin-bottom: 0.6rem;
    }
    
    .question-link {
        font-size: 0.85rem;
        color: #1e40af;
        font-weight: 500;
    }
    
    /* Encabezados de sección */
    .section-header {
        font-size: 1.5rem;
        font-weight: 600;
        color: #0f172a;
        margin-top: 2.5rem;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #e2e8f0;
    }
    
    /* Footer */
    .footer {
        margin-top: 4rem;
        padding-top: 1.5rem;
        border-top: 1px solid #e2e8f0;
        font-size: 0.85rem;
        color: #64748b;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# BANNER SUPERIOR
# ============================================

st.markdown('<div class="main-title">Discursos presidenciales chilenos 1990–2025</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Plataforma de análisis comparativo</div>', unsafe_allow_html=True)

# ============================================
# MÉTRICAS DESTACADAS
# ============================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="metric-box">
        <div class="metric-number">35</div>
        <div class="metric-label">años analizados</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="metric-box">
        <div class="metric-number">45</div>
        <div class="metric-label">documentos<br>presidenciales</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="metric-box">
        <div class="metric-number">94.656</div>
        <div class="metric-label">entrevistas CEP<br>integradas</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="metric-box">
        <div class="metric-number">15</div>
        <div class="metric-label">eventos críticos<br>cruzados</div>
    </div>
    """, unsafe_allow_html=True)

# ============================================
# QUÉ ES ESTO
# ============================================

st.markdown('<div class="section-header">Qué es esto</div>', unsafe_allow_html=True)

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

# ============================================
# FUENTES
# ============================================

st.markdown('<div class="section-header">Qué fuentes usa</div>', unsafe_allow_html=True)

col_a, col_b = st.columns(2)

with col_a:
    st.markdown("""
    **Documentos presidenciales**

    - 9 programas de gobierno (1990–2026), descargados desde fuentes públicas.
    - 36 cuentas públicas anuales (1990–2025), desde la Biblioteca del Congreso Nacional.
    """)

with col_b:
    st.markdown("""
    **Datos complementarios**

    - Encuesta CEP, base consolidada 1994–2025: 64 mediciones, 94.656 entrevistas.
    - Análisis épicos generados por Unholster con Claude Sonnet 4.6.
    """)

# ============================================
# CUATRO PREGUNTAS
# ============================================

st.markdown('<div class="section-header">Qué preguntas permite explorar</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="question-card">
        <div class="question-title">1. ¿Cumplen los gobiernos lo que prometen?</div>
        <div class="question-text">
            Comparación entre los temas que cada gobierno prometió en su programa
            de campaña y los temas sobre los que efectivamente habló en sus cuentas
            públicas anuales.
        </div>
        <div class="question-link">→ Página: Fidelidad programática</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="question-card">
        <div class="question-title">3. ¿Cómo cuentan los gobiernos su propio relato?</div>
        <div class="question-text">
            Análisis de los marcos narrativos de los discursos: quién es el
            protagonista, contra qué se enfrenta el país, qué Chile sueña y bajo
            qué épica se cuenta el momento histórico.
        </div>
        <div class="question-link">→ Página: Evolución de la épica</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="question-card">
        <div class="question-title">2. ¿Hablan los gobiernos de lo que a la gente le importa?</div>
        <div class="question-text">
            Comparación entre los temas del discurso presidencial y los problemas
            que la ciudadanía señala como prioridades en la encuesta CEP, año a año.
        </div>
        <div class="question-link">→ Página: Alineamiento ciudadano</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="question-card">
        <div class="question-title">4. ¿Qué pasa con el discurso tras una derrota electoral?</div>
        <div class="question-text">
            Casos piloto que comparan cuentas públicas anteriores y posteriores
            a eventos electorales intermedios significativos para estudiar
            reacomodos discursivos.
        </div>
        <div class="question-link">→ Página: Triangulación electoral</div>
    </div>
    """, unsafe_allow_html=True)

# ============================================
# MENÚ DE LECTURA
# ============================================

st.markdown('<div class="section-header">Cómo navegar esta plataforma</div>', unsafe_allow_html=True)

st.markdown("""
Use el menú lateral para acceder a cada sección. Cada página tiene:

- **Una explicación corta** de qué se está mostrando y cómo se construyó.
- **Visualizaciones interactivas** con las que puede hacer sus propios cruces.
- **Limitaciones de la sección** explicadas en lenguaje accesible.

La página final, **Cómo leer estos datos**, reúne las decisiones metodológicas
del proyecto y las limitaciones generales del análisis.
""")

# ============================================
# FOOTER
# ============================================

st.markdown("""
<div class="footer">
    Autor: <strong>Tomás Naudon</strong> · Plataforma en construcción.
</div>
""", unsafe_allow_html=True)