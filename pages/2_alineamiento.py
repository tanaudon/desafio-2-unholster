"""
Página 2: Alineamiento ciudadano.

Compara la agenda temática del discurso presidencial con la agenda
ciudadana derivada de la encuesta CEP (1994-2025).
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# ============================================
# CONFIGURACIÓN DE PÁGINA
# ============================================

st.set_page_config(
    page_title="Alineamiento ciudadano",
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
    
    .explanation-box {
        background-color: #f8fafc;
        border-left: 4px solid #1e40af;
        border-radius: 6px;
        padding: 1rem 1.3rem;
        margin-bottom: 1.2rem;
        font-size: 0.95rem;
        color: #334155;
        line-height: 1.55;
    }
    
    .limitation-box {
        background-color: #fef3c7;
        border-left: 4px solid #d97706;
        border-radius: 6px;
        padding: 1rem 1.3rem;
        margin-top: 1.5rem;
        font-size: 0.9rem;
        color: #78350f;
        line-height: 1.55;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# CARGA DE DATOS
# ============================================

@st.cache_data
def cargar_datos():
    agenda = pd.read_csv('data/derived/agenda_ciudadana.csv')
    alineamiento = pd.read_csv('data/derived/alineamiento_global.csv')
    brechas = pd.read_csv('data/derived/alineamiento_brechas.csv')
    aprobacion_align = pd.read_csv('data/derived/aprobacion_vs_alineamiento.csv')
    return agenda, alineamiento, brechas, aprobacion_align

agenda, alineamiento, brechas, aprobacion_align = cargar_datos()

# ============================================
# TÍTULO
# ============================================

st.markdown('<div class="page-title">Alineamiento ciudadano</div>', unsafe_allow_html=True)
st.markdown('<div class="page-subtitle">¿Hablan los gobiernos de lo que a la gente le importa?</div>', unsafe_allow_html=True)

# ============================================
# EXPLICACIÓN INICIAL
# ============================================

st.markdown("""
<div class="explanation-box">
Esta página compara dos agendas temáticas año a año:<br><br>

<strong>Agenda presidencial:</strong> derivada de las cuentas públicas anuales. 
Se cuenta cuánto aparece cada tema en cada cuenta (menciones por mil palabras) 
y se normaliza a porcentajes.<br><br>

<strong>Agenda ciudadana:</strong> derivada de la encuesta CEP (1994-2025). En cada 
medición, las personas señalan los tres problemas que consideran más importantes 
para el país. Sus respuestas se mapean a la misma taxonomía de temas, se ponderan 
con el factor poblacional <em>pond</em>, y se agregan por año.<br><br>

La comparación se hace sobre 14 temas comunes a ambas fuentes. Cinco temas 
presidenciales no tienen equivalente directo en CEP (Araucanía/Mapuche, Género, 
Niños/Infancia, Regiones, Tecnología) y quedan excluidos de la comparación. 
La encuesta CEP no tiene mediciones en 2020 por la pandemia.
</div>
""", unsafe_allow_html=True)

# ============================================
# BLOQUE 2: AGENDA CIUDADANA EN 30 AÑOS
# ============================================

st.markdown('<div class="section-header">Cómo cambió la agenda ciudadana en 30 años</div>', unsafe_allow_html=True)

st.markdown("""
<div class="explanation-box">
<strong>Cómo se lee este gráfico:</strong> cada línea representa un tema. 
El eje vertical muestra el porcentaje de menciones que recibió ese tema en 
la encuesta CEP del año respectivo. Use la leyenda para activar o desactivar 
temas y comparar trayectorias específicas.
</div>
""", unsafe_allow_html=True)

# Preparar agenda en formato largo para Plotly
agenda_long = agenda.melt(id_vars='año', var_name='tema', value_name='porcentaje')

# Lista de temas a mostrar por defecto (los más relevantes)
TEMAS_DESTACADOS = ['Seguridad', 'Trabajo/Empleo', 'Salud', 'Educación', 'Pensiones', 'Pobreza']

fig_agenda = go.Figure()

# Paleta extendida para múltiples temas
PALETA_TEMAS = {
    'Seguridad': '#dc2626',
    'Trabajo/Empleo': '#2563eb',
    'Salud': '#16a34a',
    'Educación': '#9333ea',
    'Pensiones': '#ea580c',
    'Pobreza': '#0891b2',
    'Economía': '#7c3aed',
    'Vivienda': '#65a30d',
    'Migración': '#db2777',
    'Constitución': '#0d9488',
    'Derechos humanos': '#facc15',
    'Medio ambiente': '#10b981',
    'Corrupción': '#f59e0b',
    'Desigualdad': '#6366f1',
    'Otros': '#94a3b8',
}

temas_disponibles = sorted([c for c in agenda.columns if c != 'año'])

for tema in temas_disponibles:
    datos_t = agenda_long[agenda_long['tema'] == tema].sort_values('año')
    color = PALETA_TEMAS.get(tema, '#64748b')
    visible = True if tema in TEMAS_DESTACADOS else 'legendonly'
    
    fig_agenda.add_trace(go.Scatter(
        x=datos_t['año'],
        y=datos_t['porcentaje'],
        mode='lines+markers',
        name=tema,
        line=dict(color=color, width=2.5),
        marker=dict(size=6),
        visible=visible,
        hovertemplate='<b>' + tema + '</b><br>%{x}: %{y:.1f}%<extra></extra>',
    ))

fig_agenda.update_layout(
    height=480,
    xaxis_title='Año',
    yaxis_title='Porcentaje de menciones ciudadanas (%)',
    template='plotly_white',
    hovermode='x unified',
    legend=dict(
        orientation='v',
        yanchor='top',
        y=1.0,
        xanchor='left',
        x=1.02,
    ),
    margin=dict(t=30, b=30, l=10, r=10),
)

st.plotly_chart(fig_agenda, use_container_width=True)

# ============================================
# BLOQUE 3: ALINEAMIENTO GLOBAL POR AÑO
# ============================================

st.markdown('<div class="section-header">Alineamiento global por año</div>', unsafe_allow_html=True)

st.markdown("""
<div class="explanation-box">
<strong>Cómo se lee este gráfico:</strong> cada punto muestra qué tan parecida 
es la agenda temática del presidente con la agenda ciudadana de ese año. Los 
colores indican qué presidente estaba en el poder. Un valor de 1 significaría 
que ambas agendas tienen exactamente la misma distribución de temas; valores 
más bajos indican mayor desvío.<br><br>

La métrica usada es la similitud Jensen-Shannon, calculada sobre los 14 temas 
comparables después de normalizar ambas distribuciones a 100%.
</div>
""", unsafe_allow_html=True)

COLORES_PRES = {
    'aylwin': '#2563eb',
    'frei': '#dc2626',
    'lagos': '#9333ea',
    'bachelet': '#ea580c',
    'pinera': '#0891b2',
    'boric': '#16a34a',
}

# Etiqueta legible
def etiqueta_pres(pres, año):
    if pres == 'bachelet' and año <= 2010:
        return 'Bachelet I'
    elif pres == 'bachelet' and año >= 2014:
        return 'Bachelet II'
    elif pres == 'pinera' and año <= 2013:
        return 'Piñera I'
    elif pres == 'pinera' and año >= 2018:
        return 'Piñera II'
    else:
        return pres.capitalize()

alineamiento_show = alineamiento.copy()
alineamiento_show['mandato'] = alineamiento_show.apply(
    lambda r: etiqueta_pres(r['presidente'], r['año']), axis=1
)

fig_align = go.Figure()

orden_mandatos = ['Aylwin', 'Frei', 'Lagos', 'Bachelet I', 'Piñera I', 'Bachelet II', 'Piñera II', 'Boric']

for mandato in orden_mandatos:
    datos_m = alineamiento_show[alineamiento_show['mandato'] == mandato].sort_values('año')
    if datos_m.empty:
        continue
    pres = datos_m.iloc[0]['presidente']
    
    dash = 'dot' if mandato in ['Bachelet II', 'Piñera II'] else 'solid'
    
    fig_align.add_trace(go.Scatter(
        x=datos_m['año'],
        y=datos_m['alineamiento_global'],
        mode='lines+markers',
        name=mandato,
        line=dict(color=COLORES_PRES[pres], width=2.5, dash=dash),
        marker=dict(size=9),
        hovertemplate='<b>' + mandato + ' — %{x}</b><br>Alineamiento: %{y:.3f}<extra></extra>',
    ))

fig_align.update_layout(
    height=440,
    xaxis_title='Año',
    yaxis_title='Alineamiento (Jensen-Shannon)',
    yaxis=dict(range=[0.65, 1.0]),
    template='plotly_white',
    hovermode='x unified',
    legend=dict(
        orientation='h',
        yanchor='bottom',
        y=-0.3,
        xanchor='center',
        x=0.5,
    ),
    margin=dict(t=30, b=30, l=10, r=10),
)

st.plotly_chart(fig_align, use_container_width=True)

# ============================================
# BLOQUE 4: BRECHAS TEMA POR TEMA
# ============================================

st.markdown('<div class="section-header">Brechas por tema entre gobierno y ciudadanía</div>', unsafe_allow_html=True)

st.markdown("""
<div class="explanation-box">
<strong>Cómo se lee este gráfico:</strong> cada celda muestra la diferencia 
porcentual entre el énfasis del presidente y el énfasis de la ciudadanía en 
ese tema y año. Valores positivos (azules) significan que el presidente habla 
más del tema que la ciudadanía. Valores negativos (rojos) significan lo 
contrario: la ciudadanía señala el tema como problema más de lo que el 
presidente lo aborda en su cuenta.<br><br>

Pase el cursor sobre cada celda para ver los valores exactos.
</div>
""", unsafe_allow_html=True)

# Construir matriz de brechas
brechas_pivot = brechas.pivot_table(
    index='tema',
    columns='año',
    values='brecha',
    aggfunc='first'
)

# Ordenar temas por brecha promedio absoluta (los más extremos arriba)
brechas_pivot['orden'] = brechas_pivot.abs().mean(axis=1)
brechas_pivot = brechas_pivot.sort_values('orden', ascending=False).drop(columns='orden')

# Construir hover personalizado con datos del CSV
hover_text_brechas = []
for tema in brechas_pivot.index:
    fila_hover = []
    for año in brechas_pivot.columns:
        match = brechas[(brechas['tema'] == tema) & (brechas['año'] == año)]
        if match.empty:
            fila_hover.append('')
        else:
            row = match.iloc[0]
            hover = (
                f"<b>{tema} — {año}</b><br>"
                f"Presidente: {row['pct_presidencial']:.1f}%<br>"
                f"Ciudadanía: {row['pct_ciudadana']:.1f}%<br>"
                f"Brecha: {row['brecha']:+.1f} puntos"
            )
            fila_hover.append(hover)
    hover_text_brechas.append(fila_hover)

fig_brechas = go.Figure(data=go.Heatmap(
    z=brechas_pivot.values,
    x=brechas_pivot.columns,
    y=brechas_pivot.index,
    customdata=hover_text_brechas,
    hovertemplate='%{customdata}<extra></extra>',
    colorscale=[
        [0, '#dc2626'],     # rojo intenso (ciudadanía pide más)
        [0.3, '#f87171'],
        [0.5, '#f8fafc'],   # neutro (sin brecha)
        [0.7, '#93c5fd'],
        [1.0, '#1e40af']    # azul intenso (presidente habla más)
    ],
    zmin=-25,
    zmax=25,
    zmid=0,
    colorbar=dict(
        title='Brecha<br>(puntos)',
        len=0.7,
    ),
    xgap=1,
    ygap=1,
))

fig_brechas.update_layout(
    height=520,
    xaxis_title='Año',
    yaxis_title='',
    template='plotly_white',
    margin=dict(t=30, b=30, l=10, r=10),
)

st.plotly_chart(fig_brechas, use_container_width=True)

# ============================================
# BLOQUE 5: ALINEAMIENTO VS APROBACIÓN
# ============================================

st.markdown('<div class="section-header">Alineamiento vs aprobación</div>', unsafe_allow_html=True)

st.markdown("""
<div class="explanation-box">
<strong>Cómo se construyó este gráfico:</strong> en el eje horizontal se ubica 
el alineamiento del discurso presidencial con la agenda ciudadana del año (la 
métrica del bloque anterior). En el eje vertical, el porcentaje de aprobación 
presidencial promedio del año, según la pregunta de la encuesta CEP "¿Aprueba 
o desaprueba la forma como está conduciendo el presidente el gobierno?".<br><br>

<strong>Qué muestra:</strong> cada punto es un año del período 1994-2025 
(excepto 2020 sin datos CEP). Los colores indican el presidente del año. La 
correlación numérica entre ambas variables se muestra debajo del gráfico.<br><br>

<strong>Importante:</strong> este gráfico muestra una <em>correlación descriptiva</em>, 
no una relación causal. La aprobación presidencial depende de múltiples factores 
no controlados en este análisis (economía, escándalos, eventos externos, etc.). 
La correlación observada puede tener distintas interpretaciones posibles.
</div>
""", unsafe_allow_html=True)

# Scatter con color por presidente
aprob_show = aprobacion_align.copy()
aprob_show['mandato'] = aprob_show.apply(
    lambda r: etiqueta_pres(r['presidente'], r['año']), axis=1
)

fig_scatter = go.Figure()

for mandato in orden_mandatos:
    datos_m = aprob_show[aprob_show['mandato'] == mandato]
    if datos_m.empty:
        continue
    pres = datos_m.iloc[0]['presidente']
    
    fig_scatter.add_trace(go.Scatter(
        x=datos_m['alineamiento_global'],
        y=datos_m['pct_aprueba'],
        mode='markers+text',
        name=mandato,
        text=datos_m['año'].astype(str),
        textposition='top center',
        textfont=dict(size=10, color='#475569'),
        marker=dict(
            size=14,
            color=COLORES_PRES[pres],
            line=dict(color='white', width=1.5),
        ),
        hovertemplate='<b>' + mandato + ' — %{text}</b><br>'
                      'Alineamiento: %{x:.3f}<br>'
                      'Aprobación: %{y:.1f}%<extra></extra>',
    ))

# Calcular correlación
from scipy.stats import pearsonr, spearmanr
r_pearson, p_pearson = pearsonr(aprob_show['alineamiento_global'], aprob_show['pct_aprueba'])
r_spearman, p_spearman = spearmanr(aprob_show['alineamiento_global'], aprob_show['pct_aprueba'])

fig_scatter.update_layout(
    height=520,
    xaxis_title='Alineamiento del discurso con la agenda ciudadana',
    yaxis_title='Aprobación presidencial (%)',
    template='plotly_white',
    legend=dict(
        orientation='h',
        yanchor='bottom',
        y=-0.25,
        xanchor='center',
        x=0.5,
    ),
    margin=dict(t=30, b=30, l=10, r=10),
)

st.plotly_chart(fig_scatter, use_container_width=True)

# Mostrar correlación
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Correlación Pearson", f"{r_pearson:+.3f}", help="Mide relación lineal entre las dos variables.")
with col2:
    st.metric("Correlación Spearman", f"{r_spearman:+.3f}", help="Mide relación basada en rangos, robusta a no-linealidades.")
with col3:
    st.metric("Significancia (p Pearson)", f"{p_pearson:.4f}", help="Valores menores a 0.05 suelen considerarse estadísticamente significativos.")

st.markdown("""
<div class="explanation-box">
<strong>Lectura de las correlaciones:</strong> ambos coeficientes oscilan entre 
-1 y +1. Valores cercanos a 0 indican ausencia de relación; valores positivos, 
relación directa (cuando uno sube, el otro sube); valores negativos, relación 
inversa (cuando uno sube, el otro baja). La magnitud absoluta indica la fuerza 
de la relación.
</div>
""", unsafe_allow_html=True)

# ============================================
# LIMITACIONES
# ============================================

st.markdown('<div class="section-header">Limitaciones de esta sección</div>', unsafe_allow_html=True)

st.markdown("""
<div class="limitation-box">
<strong>1. Cobertura temporal de la encuesta CEP.</strong> Los datos van de 1994 
en adelante. Los años 1990-1993 (gobierno de Aylwin) quedan fuera del análisis. 
El año 2020 también, porque la pandemia interrumpió la realización de encuestas.<br><br>

<strong>2. Mapeo entre categorías.</strong> La encuesta CEP usa 27 categorías 
de problemas, mientras nuestro análisis temático presidencial usa 19. Hicimos 
un mapeo entre ambas, pero no es perfecto: cinco temas presidenciales (Araucanía, 
Género, Niños/Infancia, Regiones, Tecnología) no tienen equivalente en CEP, y 
quedaron excluidos de la comparación.<br><br>

<strong>3. Tres menciones con igual peso.</strong> CEP pregunta por los tres 
problemas más importantes. Tratamos las tres menciones con igual peso, lo que 
puede subrepresentar la jerarquía interna de prioridades de cada persona.<br><br>

<strong>4. La correlación no implica causalidad.</strong> El cruce entre 
alineamiento y aprobación es descriptivo. No controla por factores externos 
(economía, escándalos, eventos contingentes) ni establece dirección causal. 
Las interpretaciones posibles son múltiples y no excluyentes.
</div>
""", unsafe_allow_html=True)