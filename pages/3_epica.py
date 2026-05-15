"""
Página 3: Evolución de la épica.

Analiza los marcos narrativos de los discursos presidenciales:
protagonista, antagonista, sueño, marco épico y metáfora central.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# ============================================
# CONFIGURACIÓN DE PÁGINA
# ============================================

st.set_page_config(
    page_title="Evolución de la épica",
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
    
    .discurso-card {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 1.3rem 1.5rem;
        margin-bottom: 1rem;
    }
    
    .dim-title {
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #64748b;
        margin-top: 0.8rem;
        margin-bottom: 0.3rem;
    }
    
    .dim-label {
        font-size: 1rem;
        font-weight: 600;
        color: #0f172a;
        line-height: 1.4;
    }
    
    .dim-desc {
        font-size: 0.9rem;
        color: #475569;
        line-height: 1.55;
        margin-top: 0.3rem;
    }
    
    .cita-text {
        font-size: 0.85rem;
        color: #475569;
        font-style: italic;
        padding-left: 0.8rem;
        border-left: 2px solid #cbd5e1;
        margin-top: 0.4rem;
        line-height: 1.5;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# CARGA DE DATOS
# ============================================

@st.cache_data
def cargar_datos():
    epica = pd.read_csv('data/derived/epica_clasificada.csv')
    eventos = pd.read_csv('data/derived/eventos_criticos.csv')
    gobiernos = pd.read_csv('data/derived/gobiernos.csv')
    return epica, eventos, gobiernos

epica, eventos, gobiernos = cargar_datos()

# ============================================
# TÍTULO
# ============================================

st.markdown('<div class="page-title">Evolución de la épica</div>', unsafe_allow_html=True)
st.markdown('<div class="page-subtitle">¿Cómo cuentan los gobiernos su propio relato?</div>', unsafe_allow_html=True)

# ============================================
# EXPLICACIÓN INICIAL
# ============================================

st.markdown("""
<div class="explanation-box">
Esta página analiza los <strong>marcos narrativos</strong> de los 36 discursos 
presidenciales: quién es el protagonista del relato, contra qué se enfrenta, 
qué Chile sueña, bajo qué épica se cuenta el momento histórico, y cuál es la 
metáfora central.<br><br>

Sobre esos análisis, agregamos dos capas: una tipología que agrupa los 36 
protagonistas y antagonistas en categorías mayores, y un cruce con 15 eventos 
críticos del período 1990-2025 para visualizar coincidencias entre cambios 
narrativos y eventos del mundo real.
</div>
""", unsafe_allow_html=True)

# ============================================
# BLOQUE 2: TRAYECTORIA DE MARCOS ÉPICOS
# ============================================

st.markdown('<div class="section-header">Trayectoria de los marcos épicos</div>', unsafe_allow_html=True)

st.markdown("""
<div class="explanation-box">
<strong>Cómo se lee este gráfico:</strong> cada cuenta pública entre 1990 y 
2025 tiene un marco épico asignado. Los marcos 
posibles incluyen <em>reconciliación</em>, <em>modernización</em>, 
<em>recuperación</em>, <em>oportunidad</em>, <em>crisis</em>, <em>balance</em>, 
entre otros. Cada color representa un marco distinto, y permite ver la 
evolución narrativa a lo largo de las décadas.
</div>
""", unsafe_allow_html=True)

# Colores para cada marco épico
COLORES_MARCO = {
    'reconciliación': '#9333ea',
    'recuperación': '#2563eb',
    'oportunidad': '#f59e0b',
    'modernización': '#16a34a',
    'balance': '#0891b2',
    'crisis': '#dc2626',
    'reconstrucción': '#7c3aed',
    'reparación': '#db2777',
    'refundación': '#0d9488',
    'continuidad': '#65a30d',
    'ruptura': '#be123c',
}

epica_orden = epica.sort_values('año')

fig_marcos = go.Figure()

# Una traza por marco para tener leyenda agrupada
for marco in epica_orden['epica_marco'].unique():
    datos_m = epica_orden[epica_orden['epica_marco'] == marco]
    color = COLORES_MARCO.get(marco, '#64748b')
    
    fig_marcos.add_trace(go.Scatter(
        x=datos_m['año'],
        y=[marco] * len(datos_m),
        mode='markers',
        name=marco,
        marker=dict(size=16, color=color, line=dict(color='white', width=2)),
        customdata=datos_m[['presidente', 'epica_descripcion', 'metafora_central']].values,
        hovertemplate=(
            '<b>%{customdata[0]} — %{x}</b><br><br>'
            '<b>Marco:</b> ' + marco + '<br>'
            '<b>Metáfora:</b> %{customdata[2]}<br><br>'
            '%{customdata[1]}<extra></extra>'
        ),
    ))

# Orden vertical de los marcos (más comunes arriba)
orden_marcos = epica['epica_marco'].value_counts().index.tolist()
fig_marcos.update_yaxes(categoryorder='array', categoryarray=orden_marcos[::-1])

fig_marcos.update_layout(
    height=420,
    xaxis_title='Año',
    yaxis_title='',
    template='plotly_white',
    showlegend=False,
    margin=dict(t=30, b=30, l=10, r=10),
)

st.plotly_chart(fig_marcos, use_container_width=True)

# ============================================
# BLOQUE 3: PROTAGONISTAS Y ANTAGONISTAS
# ============================================

st.markdown('<div class="section-header">Protagonistas y antagonistas en el tiempo</div>', unsafe_allow_html=True)

st.markdown("""
<div class="explanation-box">
<strong>Cómo se lee este gráfico:</strong> los 36 protagonistas y antagonistas 
fueron agrupados manualmente en tipologías mayores para facilitar la lectura 
comparativa. Cada punto del gráfico es una cuenta pública. El color indica 
el tipo de protagonista (gráfico izquierdo) o antagonista (gráfico derecho) 
identificado en el análisis épico.<br><br>

La clasificación es interpretativa y abierta a discusión. Pase el cursor sobre 
cada punto para ver la etiqueta original del análisis.
</div>
""", unsafe_allow_html=True)

# Colores para tipologías
COLORES_PROTAGONISTA = {
    'pueblo_ciudadania': '#2563eb',
    'nacion_chile': '#9333ea',
    'estado_gobierno': '#16a34a',
    'grupos_sociales': '#ea580c',
    'familias_individuos': '#0891b2',
    'otro': '#64748b',
}

COLORES_ANTAGONISTA = {
    'pasado_autoritario': '#7c3aed',
    'condiciones_estructurales': '#0891b2',
    'elites_conservadoras': '#dc2626',
    'amenazas_externas': '#f59e0b',
    'crimen_violencia': '#be123c',
    'crisis_social': '#ea580c',
    'corrupcion_institucional': '#db2777',
    'sin_antagonista': '#94a3b8',
}

col_prot, col_ant = st.columns(2)

with col_prot:
    st.markdown("##### Protagonistas")
    
    fig_prot = go.Figure()
    
    orden_protagonistas = epica['protagonista_tipo'].value_counts().index.tolist()
    
    for tipo in orden_protagonistas:
        datos_t = epica[epica['protagonista_tipo'] == tipo].sort_values('año')
        color = COLORES_PROTAGONISTA.get(tipo, '#64748b')
        label = datos_t.iloc[0]['protagonista_tipo_label']
        
        fig_prot.add_trace(go.Scatter(
            x=datos_t['año'],
            y=[label] * len(datos_t),
            mode='markers',
            name=label,
            marker=dict(size=14, color=color, line=dict(color='white', width=1.5)),
            customdata=datos_t[['presidente', 'protagonista_etiqueta']].values,
            hovertemplate=(
                '<b>%{customdata[0]} — %{x}</b><br>'
                '<i>%{customdata[1]}</i><extra></extra>'
            ),
        ))
    
    fig_prot.update_yaxes(categoryorder='array', categoryarray=[
        epica[epica['protagonista_tipo'] == t].iloc[0]['protagonista_tipo_label']
        for t in orden_protagonistas[::-1]
    ])
    
    fig_prot.update_layout(
        height=400,
        xaxis_title='Año',
        yaxis_title='',
        template='plotly_white',
        showlegend=False,
        margin=dict(t=20, b=20, l=10, r=10),
    )
    
    st.plotly_chart(fig_prot, use_container_width=True)

with col_ant:
    st.markdown("##### Antagonistas")
    
    fig_ant = go.Figure()
    
    orden_antagonistas = epica['antagonista_tipo'].value_counts().index.tolist()
    
    for tipo in orden_antagonistas:
        datos_t = epica[epica['antagonista_tipo'] == tipo].sort_values('año')
        color = COLORES_ANTAGONISTA.get(tipo, '#64748b')
        label = datos_t.iloc[0]['antagonista_tipo_label']
        
        fig_ant.add_trace(go.Scatter(
            x=datos_t['año'],
            y=[label] * len(datos_t),
            mode='markers',
            name=label,
            marker=dict(size=14, color=color, line=dict(color='white', width=1.5)),
            customdata=datos_t[['presidente', 'antagonista_etiqueta']].values,
            hovertemplate=(
                '<b>%{customdata[0]} — %{x}</b><br>'
                '<i>%{customdata[1]}</i><extra></extra>'
            ),
        ))
    
    fig_ant.update_yaxes(categoryorder='array', categoryarray=[
        epica[epica['antagonista_tipo'] == t].iloc[0]['antagonista_tipo_label']
        for t in orden_antagonistas[::-1]
    ])
    
    fig_ant.update_layout(
        height=400,
        xaxis_title='Año',
        yaxis_title='',
        template='plotly_white',
        showlegend=False,
        margin=dict(t=20, b=20, l=10, r=10),
    )
    
    st.plotly_chart(fig_ant, use_container_width=True)

# ============================================
# BLOQUE 4: EXPLORADOR DE DISCURSOS
# ============================================

st.markdown('<div class="section-header">Explorador de discursos individuales</div>', unsafe_allow_html=True)

st.markdown("""
<div class="explanation-box">
<strong>Cómo se usa:</strong> seleccione una cuenta pública específica para 
ver el análisis épico completo, incluyendo las citas textuales del discurso 
que respaldan cada dimensión.
</div>
""", unsafe_allow_html=True)

# Selector de discurso
epica_ordenada = epica.sort_values('año')
opciones_discursos = {
    f"{int(row['año'])} — {row['presidente'].capitalize()}": row['id']
    for _, row in epica_ordenada.iterrows()
}

discurso_seleccionado = st.selectbox(
    'Seleccione un discurso:',
    options=list(opciones_discursos.keys()),
    key='selector_discurso_epica'
)

id_seleccionado = opciones_discursos[discurso_seleccionado]
discurso = epica[epica['id'] == id_seleccionado].iloc[0]

# Mostrar tarjeta del discurso
st.markdown(f"""
<div class="discurso-card">
    <h3 style="margin-top: 0; color: #0f172a;">{discurso['presidente'].capitalize()} — {int(discurso['año'])}</h3>
    <p style="color: #64748b; font-size: 0.95rem; margin-bottom: 1.2rem;">
        <strong>Marco épico:</strong> {discurso['epica_marco']} · 
        <strong>Metáfora central:</strong> {discurso['metafora_central']}
    </p>
</div>
""", unsafe_allow_html=True)

# Función auxiliar para mostrar una dimensión con sus citas
def mostrar_dimension(titulo, etiqueta, descripcion, citas_raw):
    citas = [c.strip() for c in citas_raw.split('||') if c.strip()]
    citas_html = ''.join([f'<div class="cita-text">«{c}»</div>' for c in citas])
    return f"""
    <div class="discurso-card">
        <div class="dim-title">{titulo}</div>
        <div class="dim-label">{etiqueta}</div>
        <div class="dim-desc">{descripcion}</div>
        <div style="margin-top: 0.8rem;">{citas_html}</div>
    </div>
    """

# Mostrar las 4 dimensiones
st.markdown(mostrar_dimension(
    'Protagonista',
    discurso['protagonista_etiqueta'],
    discurso['protagonista_descripcion'],
    discurso['protagonista_citas']
), unsafe_allow_html=True)

st.markdown(mostrar_dimension(
    'Antagonista',
    discurso['antagonista_etiqueta'],
    discurso['antagonista_descripcion'],
    discurso['antagonista_citas']
), unsafe_allow_html=True)

st.markdown(mostrar_dimension(
    'Sueño',
    discurso['sueno_etiqueta'],
    discurso['sueno_descripcion'],
    discurso['sueno_citas']
), unsafe_allow_html=True)

st.markdown(mostrar_dimension(
    'Épica',
    discurso['epica_marco'],
    discurso['epica_descripcion'],
    discurso['epica_citas']
), unsafe_allow_html=True)

# Nota interpretativa de la clasificación
if pd.notna(discurso.get('nota_interpretativa')):
    st.markdown(f"""
    <div class="discurso-card" style="background-color: #fefce8; border-color: #fde68a;">
        <div class="dim-title">Nota interpretativa</div>
        <div class="dim-desc">{discurso['nota_interpretativa']}</div>
    </div>
    """, unsafe_allow_html=True)

# ============================================
# BLOQUE 5: EVENTOS CRÍTICOS SUPERPUESTOS
# ============================================

st.markdown('<div class="section-header">Trayectoria épica con eventos críticos</div>', unsafe_allow_html=True)

st.markdown("""
<div class="explanation-box">
<strong>Cómo se lee este gráfico:</strong> esta visualización superpone los 
marcos épicos a 15 eventos críticos del período 1990-2025: catástrofes 
naturales, crisis económicas, escándalos de corrupción, plebiscitos, estallidos 
sociales. Los eventos están marcados con líneas verticales y etiquetados.<br><br>

Permite explorar visualmente coincidencias temporales entre eventos del mundo 
real y cambios en el marco épico presidencial. Es una visualización 
exploratoria: las coincidencias visibles no implican causalidad.
</div>
""", unsafe_allow_html=True)

fig_cruzado = go.Figure()

# Puntos de marcos épicos
for marco in epica_orden['epica_marco'].unique():
    datos_m = epica_orden[epica_orden['epica_marco'] == marco]
    color = COLORES_MARCO.get(marco, '#64748b')
    
    fig_cruzado.add_trace(go.Scatter(
        x=datos_m['año'],
        y=[marco] * len(datos_m),
        mode='markers',
        name=marco,
        marker=dict(size=14, color=color, line=dict(color='white', width=1.5)),
        customdata=datos_m[['presidente']].values,
        hovertemplate='<b>%{customdata[0]} — %{x}</b><br>Marco: ' + marco + '<extra></extra>',
        showlegend=False,
    ))

# Líneas verticales para eventos
TIPOS_EVENTO_COLOR = {
    'DDHH': '#9333ea',
    'Económico': '#dc2626',
    'Corrupción': '#db2777',
    'Social': '#ea580c',
    'Natural': '#16a34a',
    'Crisis': '#be123c',
    'Sanitaria': '#0891b2',
    'Institucional': '#2563eb',
}

orden_marcos_y = epica['epica_marco'].value_counts().index.tolist()

for _, ev in eventos.iterrows():
    color_ev = TIPOS_EVENTO_COLOR.get(ev['tipo'], '#64748b')
    
    fig_cruzado.add_vline(
        x=ev['año'],
        line_dash='dash',
        line_color=color_ev,
        line_width=1,
        opacity=0.5,
    )
    
    # Annotation con el nombre del evento
    fig_cruzado.add_annotation(
        x=ev['año'],
        y=len(orden_marcos_y) - 0.3,
        text=ev['evento'],
        showarrow=False,
        font=dict(size=9, color=color_ev),
        textangle=-90,
        xanchor='left',
        yanchor='top',
    )

fig_cruzado.update_yaxes(categoryorder='array', categoryarray=orden_marcos_y[::-1])

fig_cruzado.update_layout(
    height=550,
    xaxis_title='Año',
    yaxis_title='',
    template='plotly_white',
    showlegend=False,
    margin=dict(t=80, b=30, l=10, r=10),
)

st.plotly_chart(fig_cruzado, use_container_width=True)

# Leyenda de tipos de eventos
st.markdown("""
<div style="font-size: 0.85rem; color: #475569; margin-top: 0.5rem; text-align: center;">
    <strong>Tipos de evento:</strong> 
    <span style="color: #9333ea;">●</span> DDHH ·
    <span style="color: #dc2626;">●</span> Económico ·
    <span style="color: #db2777;">●</span> Corrupción ·
    <span style="color: #ea580c;">●</span> Social ·
    <span style="color: #16a34a;">●</span> Natural ·
    <span style="color: #be123c;">●</span> Crisis ·
    <span style="color: #0891b2;">●</span> Sanitaria ·
    <span style="color: #2563eb;">●</span> Institucional
</div>
""", unsafe_allow_html=True)

# ============================================
# LIMITACIONES
# ============================================

st.markdown('<div class="section-header">Limitaciones de esta sección</div>', unsafe_allow_html=True)

st.markdown("""
<div class="limitation-box">
<strong>1. Los análisis épicos no son nuestros.</strong> Nuestra contribución es agruparlos en tipologías mayores y cruzarlos con eventos.<br><br>

<strong>2. La tipología es interpretativa.</strong> La agrupación de los 36 
protagonistas y antagonistas en categorías mayores es una lectura propia. 
Otros lectores podrían clasificar diferente. Cada caso lleva una nota 
interpretativa que documenta el sentido específico de la categoría.<br><br>

<strong>3. La coincidencia temporal no implica causalidad.</strong> El cruce 
con eventos críticos muestra coincidencias en el tiempo, no relaciones causales. 
Un cambio narrativo cercano a un evento puede deberse a ese evento, a otros 
factores simultáneos, o a procesos discursivos previos.<br><br>

<strong>4. La selección de eventos es discrecional.</strong> Los 15 eventos 
críticos fueron elegidos por su relevancia narrativa esperada. Otra selección 
mostraría coincidencias diferentes. La lista no es exhaustiva.
</div>
""", unsafe_allow_html=True)