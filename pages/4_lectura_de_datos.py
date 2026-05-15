"""
Página 4: Cómo leer estos datos.

Reúne las decisiones metodológicas y limitaciones generales del proyecto
en lenguaje accesible. Funciona como guía para el lector.
"""

import streamlit as st

# ============================================
# CONFIGURACIÓN DE PÁGINA
# ============================================

st.set_page_config(
    page_title="Cómo leer estos datos",
    page_icon="📊",
    layout="wide",
)

# ============================================
# CSS CONSISTENTE
# ============================================

st.markdown("""
<style>
    .block-container {
        padding-top: 3rem;
        padding-bottom: 2rem;
        max-width: 1100px;
    }
    
    .page-title {
        font-size: 2.2rem;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 0.3rem;
        line-height: 1.2;
    }
    
    .page-subtitle {
        font-size: 1.05rem;
        color: #475569;
        margin-bottom: 1.5rem;
        font-weight: 400;
    }
    
    .section-header {
        font-size: 1.4rem;
        font-weight: 600;
        color: #0f172a;
        margin-top: 2.5rem;
        margin-bottom: 0.8rem;
        padding-bottom: 0.4rem;
        border-bottom: 2px solid #e2e8f0;
    }
    
    .info-box {
        background-color: #f8fafc;
        border-left: 4px solid #1e40af;
        border-radius: 6px;
        padding: 1rem 1.3rem;
        margin-bottom: 1.2rem;
        font-size: 0.95rem;
        color: #334155;
        line-height: 1.6;
    }
    
    .decision-card {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 1.2rem 1.5rem;
        margin-bottom: 1rem;
    }
    
    .decision-title {
        font-size: 1rem;
        font-weight: 600;
        color: #0f172a;
        margin-bottom: 0.4rem;
    }
    
    .decision-text {
        font-size: 0.92rem;
        color: #475569;
        line-height: 1.55;
    }
    
    .limitation-card {
        background-color: #fef3c7;
        border-left: 4px solid #d97706;
        border-radius: 6px;
        padding: 1rem 1.3rem;
        margin-bottom: 0.8rem;
        font-size: 0.92rem;
        color: #78350f;
        line-height: 1.6;
    }
    
    .can-table {
        background-color: #f0fdf4;
        border: 1px solid #86efac;
        border-radius: 8px;
        padding: 1.2rem 1.5rem;
        margin-bottom: 1rem;
    }
    
    .cannot-table {
        background-color: #fef2f2;
        border: 1px solid #fecaca;
        border-radius: 8px;
        padding: 1.2rem 1.5rem;
        margin-bottom: 1rem;
    }
    
    .can-title {
        font-size: 1.05rem;
        font-weight: 600;
        color: #15803d;
        margin-bottom: 0.6rem;
    }
    
    .cannot-title {
        font-size: 1.05rem;
        font-weight: 600;
        color: #b91c1c;
        margin-bottom: 0.6rem;
    }
    
    ul.clean-list {
        margin-top: 0.3rem;
        padding-left: 1.2rem;
        font-size: 0.92rem;
        line-height: 1.6;
    }
    
    ul.clean-list li {
        margin-bottom: 0.3rem;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# TÍTULO
# ============================================

st.markdown('<div class="page-title">Cómo leer estos datos</div>', unsafe_allow_html=True)
st.markdown('<div class="page-subtitle">Guía metodológica y limitaciones del proyecto</div>', unsafe_allow_html=True)

# ============================================
# BLOQUE 1: PROPÓSITO
# ============================================

st.markdown("""
<div class="info-box">
Esta página no entrega conclusiones. Es un manual: explica las decisiones que 
tomamos para construir los análisis de las páginas anteriores, las limitaciones 
generales de los datos, y orienta sobre qué preguntas pueden responderse con 
ellos y cuáles no.<br><br>

El objetivo es que cualquier persona que explore esta plataforma pueda hacer 
sus propias lecturas con criterio, entendiendo los alcances y los límites de 
lo que está viendo.
</div>
""", unsafe_allow_html=True)

# ============================================
# BLOQUE 2: DECISIONES METODOLÓGICAS
# ============================================

st.markdown('<div class="section-header">Principales decisiones metodológicas</div>', unsafe_allow_html=True)

decisiones = [
    {
        'titulo': 'Procesamiento de los documentos',
        'texto': """Los 9 programas presidenciales y las 36 cuentas públicas son archivos PDF 
        descargados de fuentes oficiales. La mayoría se procesó automáticamente, pero algunos 
        documentos antiguos (Aylwin 1990, Frei 1994, dos cuentas de Frei) requirieron 
        reconocimiento óptico de caracteres (OCR) por venir como imagen escaneada. El OCR 
        puede introducir pequeñas variaciones en el conteo de palabras."""
    },
    {
        'titulo': 'Diccionario temático',
        'texto': """Construimos un diccionario de 19 temas (Economía, Educación, Salud, 
        Seguridad, Pensiones, etc.), tomando como base la taxonomía pública de Unholster 
        y agregando tres temas adicionales: Corrupción, Pobreza y Desigualdad. Cada tema 
        agrupa entre 8 y 23 términos relacionados. Una mención puede contar para más de 
        un tema si el término es ambiguo."""
    },
    {
        'titulo': 'Métrica de frecuencia',
        'texto': """Para cada documento contamos cuántas veces aparece cada tema y lo 
        expresamos como <em>menciones por cada mil palabras del texto</em>. Esto permite 
        comparar documentos de distinto largo. Los textos de cuentas públicas son 
        sistemáticamente más largos que los programas."""
    },
    {
        'titulo': 'Métrica de comparación entre agendas',
        'texto': """Para comparar dos distribuciones temáticas (por ejemplo, programa vs 
        cuenta, o agenda presidencial vs agenda ciudadana) usamos la similitud Jensen-Shannon. 
        Es una métrica simétrica que entrega un valor entre 0 y 1: 1 indica distribuciones 
        idénticas, valores más bajos indican mayor desvío. Como métrica complementaria, 
        comparamos también los tres temas principales del programa con los tres temas 
        principales de cada cuenta."""
    },
    {
        'titulo': 'Procesamiento de la encuesta CEP',
        'texto': """Usamos la base consolidada CEP 1994-2025 (64 mediciones, 94.656 entrevistas). 
        La pregunta clave es "¿Cuáles son los tres problemas a los que debería dedicar mayor 
        esfuerzo el gobierno?". Tratamos las tres menciones con igual peso. Aplicamos el 
        factor de ponderación poblacional <em>pond</em> para que los porcentajes representen 
        adecuadamente a la población chilena. Agregamos las distintas mediciones de un año 
        promediando sus resultados."""
    },
    {
        'titulo': 'Mapeo entre categorías CEP y temas presidenciales',
        'texto': """CEP usa 27 categorías de problemas, nuestro análisis usa 19. Construimos 
        un mapeo entre ambas: por ejemplo, "Delincuencia", "Narcotráfico" y "Terrorismo" 
        de CEP se agrupan en "Seguridad" del análisis presidencial. Cinco temas presidenciales 
        (Araucanía, Género, Niños/Infancia, Regiones, Tecnología) no tienen equivalente en 
        CEP y quedan excluidos de la comparación de alineamiento."""
    },
    {
        'titulo': 'Origen de los análisis épicos',
        'texto': """Los análisis de protagonista, antagonista, sueño, marco épico y metáfora 
        no son nuestros. Provienen de la plataforma de Unholster, donde fueron generados con 
        el modelo Claude Sonnet 4.6 sobre el texto completo de cada discurso. Nosotros 
        descargamos esos análisis y agregamos dos capas: una tipología que agrupa los 36 
        protagonistas y antagonistas en categorías mayores, y un cruce con eventos críticos 
        del período."""
    },
    {
        'titulo': 'Selección de eventos críticos',
        'texto': """Seleccionamos 15 eventos del período 1990-2025: catástrofes naturales 
        (terremoto 27F), crisis económicas (asiática, financiera global), escándalos de 
        corrupción (MOP-Gate, Penta-SQM-Caval, caso Audios), crisis sociales (revolución 
        pingüina, movilización estudiantil 2011, estallido 2019), procesos políticos 
        (plebiscitos constitucionales, Rechazo 2022) y la pandemia. La selección es 
        discrecional y puede ampliarse."""
    },
]

for d in decisiones:
    st.markdown(f"""
    <div class="decision-card">
        <div class="decision-title">{d['titulo']}</div>
        <div class="decision-text">{d['texto']}</div>
    </div>
    """, unsafe_allow_html=True)

# ============================================
# BLOQUE 3: LIMITACIONES GENERALES
# ============================================

st.markdown('<div class="section-header">Limitaciones generales del proyecto</div>', unsafe_allow_html=True)

limitaciones = [
    {
        'titulo': '1. Frecuencia no es importancia',
        'texto': """El análisis cuenta cuántas veces aparece cada tema, no cuán central 
        es. Un tema puede mencionarse poco pero ser simbólicamente decisivo. Los derechos 
        humanos en la cuenta de 1990 de Aylwin, la Constitución en el programa de Boric 
        2022, o la idea de "deuda social" son ejemplos: aparecen subordinados en términos 
        de frecuencia, pero son estructurantes de la narrativa. La frecuencia es una 
        primera lectura, no la única ni la última."""
    },
    {
        'titulo': '2. Las palabras cambian de significado en el tiempo',
        'texto': """"Seguridad" en 1991 refería mayoritariamente a terrorismo político 
        residual (FPMR, Lautaro). "Seguridad" en 2024 refiere a delincuencia común, 
        narcotráfico y crimen organizado. Las frecuencias pueden ser comparables pero el 
        contenido sustantivo no lo es. Lo mismo ocurre con "modernización", "transición", 
        "desarrollo": las palabras se mantienen pero su carga semántica muta."""
    },
    {
        'titulo': '3. Calidad técnica heterogénea de los documentos',
        'texto': """Los PDFs varían en calidad. Algunos textos antiguos se procesaron 
        con OCR, lo cual puede generar pequeñas variaciones en el conteo (palabras 
        pegadas, símbolos malinterpretados). Donde detectamos problemas mayores hicimos 
        validación manual, pero variaciones menores son inevitables."""
    },
    {
        'titulo': '4. Cobertura desigual de la encuesta CEP',
        'texto': """Los datos de opinión pública empiezan en 1994. El período de Aylwin 
        (1990-1993) queda fuera del análisis de alineamiento. La pandemia interrumpió 
        las mediciones en 2020. Algunos años tienen una sola medición, otros tienen tres. 
        Promediamos los resultados anuales, lo que puede ocultar variaciones intra-anuales."""
    },
    {
        'titulo': '5. La correlación no implica causalidad',
        'texto': """Cuando dos variables se mueven juntas (por ejemplo, alineamiento del 
        discurso y aprobación presidencial), eso no significa que una cause la otra. 
        Pueden estar respondiendo ambas a un tercer factor (cambio de era política, 
        contexto económico, escándalos públicos), o la causalidad puede ir en sentido 
        contrario al esperado. Esta plataforma muestra coincidencias, no relaciones 
        causales."""
    },
    {
        'titulo': '6. La selección temática es interpretativa',
        'texto': """Definir qué cuenta como "tema" implica decisiones. Por qué "Seguridad" 
        es un tema y no varios subtipos (delincuencia, narco, terrorismo), por qué "Salud" 
        agrupa lo médico y lo sanitario, por qué creamos "Desigualdad" como categoría 
        propia y no la subsumimos en "Pobreza". Cada decisión es defendible y a la vez 
        revisable. Una taxonomía distinta daría resultados parcialmente distintos."""
    },
]

for l in limitaciones:
    st.markdown(f"""
    <div class="limitation-card">
        <strong>{l['titulo']}</strong><br>
        {l['texto']}
    </div>
    """, unsafe_allow_html=True)

# ============================================
# BLOQUE 4: QUÉ SÍ Y QUÉ NO PERMITE RESPONDER
# ============================================

st.markdown('<div class="section-header">Qué preguntas sí permite responder y cuáles no</div>', unsafe_allow_html=True)

st.markdown("""
<div class="info-box">
Lo que sigue es una guía orientativa. Los datos de esta plataforma son ricos 
pero acotados: sirven para hacer ciertas preguntas, no para responder otras 
que parecen similares pero requieren otro tipo de evidencia.
</div>
""", unsafe_allow_html=True)

col_si, col_no = st.columns(2)

with col_si:
    st.markdown("""
    <div class="can-table">
        <div class="can-title">Estos datos permiten:</div>
        <ul class="clean-list">
            <li>Comparar qué temas predominan en cada cuenta pública y cómo cambian respecto del programa.</li>
            <li>Ver cómo evoluciona la agenda ciudadana medida por encuesta en 30 años.</li>
            <li>Observar coincidencias y brechas entre lo que los gobiernos dicen y lo que la ciudadanía señala como problemas.</li>
            <li>Identificar los marcos narrativos (protagonistas, antagonistas, épicas) de cada discurso presidencial.</li>
            <li>Detectar coincidencias temporales entre cambios narrativos y eventos relevantes del país.</li>
            <li>Generar hipótesis y preguntas para investigaciones más profundas.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col_no:
    st.markdown("""
    <div class="cannot-table">
        <div class="cannot-title">Estos datos no permiten:</div>
        <ul class="clean-list">
            <li>Afirmar que un gobierno fue mejor o peor que otro.</li>
            <li>Determinar si las promesas se cumplieron en la realidad (solo si volvieron a aparecer en el discurso).</li>
            <li>Establecer causalidad entre alineamiento del discurso y aprobación presidencial.</li>
            <li>Concluir que la ciudadanía piensa lo mismo que indica la encuesta (que mide opiniones, no convicciones).</li>
            <li>Inferir significados profundos de un tema solo a partir de su frecuencia.</li>
            <li>Generalizar los hallazgos a otros países o contextos.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# ============================================
# BLOQUE 5: PARA PROFUNDIZAR
# ============================================

st.markdown('<div class="section-header">Para profundizar</div>', unsafe_allow_html=True)

st.markdown("""
<div class="info-box">
Esta plataforma se enfoca en mostrar los datos de forma descriptiva, sin tomar 
posición interpretativa. Existe material complementario con análisis más 
detallados (lecturas sociológicas, propuestas de extensión metodológica, 
discusión de hallazgos cruzados) disponible bajo solicitud.<br><br>

El proyecto está abierto a revisión, ajustes y extensiones. Tanto las decisiones 
metodológicas como las limitaciones son parte del diálogo necesario para construir 
mejor conocimiento sobre el discurso político y la opinión pública en Chile.
</div>
""", unsafe_allow_html=True)