"""
Página 1: Fidelidad programática.

Compara los temas anunciados en el programa de gobierno con los temas
efectivamente desarrollados en las cuentas públicas anuales.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# ============================================
# CONFIGURACIÓN DE PÁGINA
# ============================================

st.set_page_config(
    page_title="Fidelidad programática",
    page_icon="📊",
    layout="wide",
)

# ============================================
# CSS CONSISTENTE CON HOME
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
    fidelidad = pd.read_csv('data/derived/fidelidad_vs_programa.csv')
    top3 = pd.read_csv('data/derived/fidelidad_top3.csv')
    desvios = pd.read_csv('data/derived/desvios_tematicos.csv')
    return fidelidad, top3, desvios

fidelidad, top3, desvios = cargar_datos()

# ============================================
# TÍTULO
# ============================================

st.markdown('<div class="page-title">Fidelidad programática</div>', unsafe_allow_html=True)
st.markdown('<div class="page-subtitle">¿Cumplen los gobiernos lo que prometen?</div>', unsafe_allow_html=True)

# ============================================
# EXPLICACIÓN INICIAL
# ============================================

st.markdown("""
<div class="explanation-box">
Esta página compara los <strong>9 programas de gobierno</strong> (lo que cada candidato 
prometió en campaña) con las <strong>36 cuentas públicas</strong> (lo que efectivamente 
habló cada presidente en mayo de cada año ante el Congreso).<br><br>

La comparación se hace por temas: 19 categorías construidas a partir del vocabulario 
identificado en los documentos (Economía, Educación, Salud, Seguridad, Pensiones, 
Migración, entre otras). Para cada documento se calcula cuántas veces aparece cada 
tema por cada mil palabras del texto.
</div>
""", unsafe_allow_html=True)

# ============================================
# BLOQUE 1: TRAYECTORIA DE FIDELIDAD
# ============================================

st.markdown('<div class="section-header">Trayectoria de fidelidad por gobierno</div>', unsafe_allow_html=True)

st.markdown("""
<div class="explanation-box">
<strong>Cómo se lee este gráfico:</strong> cada línea representa un gobierno. 
El eje vertical muestra qué tan parecida es la distribución de temas de cada 
cuenta pública al programa original de ese gobierno. Un valor de 1 significa 
distribución idéntica; valores más bajos indican mayor desvío.<br><br>

La métrica usada es la similitud Jensen-Shannon, una medida que compara dos 
distribuciones de frecuencias. Valores entre 0.9 y 1.0 son altos; entre 0.7 
y 0.9 son moderados.
</div>
""", unsafe_allow_html=True)

# Preparar datos para el gráfico
# Filtrar solo cuentas (no programas) y armar para graficar
fid_cuentas = fidelidad[fidelidad['tipo'] == 'cuenta'].copy() if 'tipo' in fidelidad.columns else fidelidad.copy()

# Colores por presidente
COLORES_PRES = {
    'aylwin': '#2563eb',
    'frei': '#dc2626',
    'lagos': '#9333ea',
    'bachelet': '#ea580c',
    'pinera': '#0891b2',
    'boric': '#16a34a',
}

fig_trayectoria = go.Figure()

for pres in ['aylwin', 'frei', 'lagos', 'bachelet', 'pinera', 'boric']:
    datos_pres = fid_cuentas[fid_cuentas['presidente'] == pres].sort_values('año')
    if datos_pres.empty:
        continue
    
    # Bachelet tiene 2 mandatos, los separamos
    if pres == 'bachelet':
        # Mandato 1: 2006-2009
        b1 = datos_pres[datos_pres['año'] <= 2010]
        if not b1.empty:
            fig_trayectoria.add_trace(go.Scatter(
                x=b1['año'],
                y=b1['fidelidad_js'],
                mode='lines+markers',
                name='Bachelet I (2006-2009)',
                line=dict(color=COLORES_PRES[pres], width=2.5),
                marker=dict(size=9),
                hovertemplate='<b>%{x}</b><br>Fidelidad: %{y:.3f}<extra></extra>'
            ))
        # Mandato 2: 2014-2017
        b2 = datos_pres[datos_pres['año'] >= 2014]
        if not b2.empty:
            fig_trayectoria.add_trace(go.Scatter(
                x=b2['año'],
                y=b2['fidelidad_js'],
                mode='lines+markers',
                name='Bachelet II (2014-2017)',
                line=dict(color=COLORES_PRES[pres], width=2.5, dash='dot'),
                marker=dict(size=9),
                hovertemplate='<b>%{x}</b><br>Fidelidad: %{y:.3f}<extra></extra>'
            ))
    elif pres == 'pinera':
        # Mandato 1: 2010-2013
        p1 = datos_pres[datos_pres['año'] <= 2013]
        if not p1.empty:
            fig_trayectoria.add_trace(go.Scatter(
                x=p1['año'],
                y=p1['fidelidad_js'],
                mode='lines+markers',
                name='Piñera I (2010-2013)',
                line=dict(color=COLORES_PRES[pres], width=2.5),
                marker=dict(size=9),
                hovertemplate='<b>%{x}</b><br>Fidelidad: %{y:.3f}<extra></extra>'
            ))
        # Mandato 2: 2018-2021
        p2 = datos_pres[datos_pres['año'] >= 2018]
        if not p2.empty:
            fig_trayectoria.add_trace(go.Scatter(
                x=p2['año'],
                y=p2['fidelidad_js'],
                mode='lines+markers',
                name='Piñera II (2018-2021)',
                line=dict(color=COLORES_PRES[pres], width=2.5, dash='dot'),
                marker=dict(size=9),
                hovertemplate='<b>%{x}</b><br>Fidelidad: %{y:.3f}<extra></extra>'
            ))
    else:
        fig_trayectoria.add_trace(go.Scatter(
            x=datos_pres['año'],
            y=datos_pres['fidelidad_js'],
            mode='lines+markers',
            name=pres.capitalize(),
            line=dict(color=COLORES_PRES[pres], width=2.5),
            marker=dict(size=9),
            hovertemplate='<b>%{x}</b><br>Fidelidad: %{y:.3f}<extra></extra>'
        ))

fig_trayectoria.update_layout(
    height=480,
    xaxis_title='Año',
    yaxis_title='Fidelidad (Jensen-Shannon)',
    yaxis=dict(range=[0.7, 1.0]),
    template='plotly_white',
    hovermode='x unified',
    legend=dict(
        orientation='h',
        yanchor='bottom',
        y=-0.25,
        xanchor='center',
        x=0.5,
    ),
    margin=dict(t=30, b=30, l=10, r=10),
)

st.plotly_chart(fig_trayectoria, use_container_width=True)

# ============================================
# BLOQUE 2: FIDELIDAD TOP-3
# ============================================

st.markdown('<div class="section-header">Fidelidad de los temas principales (top-3)</div>', unsafe_allow_html=True)

st.markdown("""
<div class="explanation-box">
<strong>Cómo se lee este gráfico:</strong> esta es una métrica complementaria 
y más estricta que la anterior. Para cada cuenta pública, se evalúa cuántos 
de los tres temas principales del programa siguen estando en el top-3 de la 
cuenta.<br><br>

Resultado posible: 3 (fidelidad total del top), 2, 1 (cambio parcial), o 0 
(cambio total del top temático). La métrica anterior puede ser alta aunque 
los temas principales hayan cambiado; esta lo detecta más directamente.
</div>
""", unsafe_allow_html=True)

# Preparar heatmap top-3
top3_pivot = top3.pivot_table(
    index='presidente',
    columns='año',
    values='coincidencias_top3',
    aggfunc='first'
)

# Ordenar presidentes por su primer año
orden_pres = ['aylwin', 'frei', 'lagos', 'bachelet', 'pinera', 'boric']
top3_pivot = top3_pivot.reindex([p for p in orden_pres if p in top3_pivot.index])

fig_top3 = go.Figure(data=go.Heatmap(
    z=top3_pivot.values,
    x=top3_pivot.columns,
    y=[p.capitalize() for p in top3_pivot.index],
    colorscale=[
        [0, '#fee2e2'],
        [0.33, '#fdba74'],
        [0.66, '#86efac'],
        [1.0, '#15803d']
    ],
    zmin=0,
    zmax=3,
    colorbar=dict(
        title='Coincidencias',
        tickmode='array',
        tickvals=[0, 1, 2, 3],
        ticktext=['0', '1', '2', '3'],
    ),
    hovertemplate='<b>%{y} %{x}</b><br>%{z}/3 temas coinciden<extra></extra>',
    text=top3_pivot.values,
    texttemplate='%{text}',
    textfont={"size": 13},
))

fig_top3.update_layout(
    height=350,
    xaxis_title='Año',
    yaxis_title='',
    template='plotly_white',
    margin=dict(t=30, b=30, l=10, r=10),
)

st.plotly_chart(fig_top3, use_container_width=True)

# ============================================
# BLOQUE 3: DESVÍOS TEMÁTICOS
# ============================================

st.markdown('<div class="section-header">Temas que suben y temas que bajan</div>', unsafe_allow_html=True)

st.markdown("""
<div class="explanation-box">
<strong>Cómo se lee este gráfico:</strong> seleccione un gobierno y vea qué 
temas crecieron o cayeron entre lo que prometió el programa y lo que efectivamente 
habló en sus cuentas. Valores positivos: temas que aparecieron más en las cuentas 
que en el programa (temas emergentes). Valores negativos: temas que aparecieron 
menos (temas abandonados).<br><br>

La unidad es <em>menciones por cada mil palabras</em>. El promedio se calcula 
sobre todas las cuentas del mandato comparándolas con el programa original.
</div>
""", unsafe_allow_html=True)

# Selector de gobierno
gobiernos_disponibles = sorted(desvios['presidente'].unique())
gob_seleccionado = st.selectbox(
    'Seleccione un gobierno:',
    options=gobiernos_disponibles,
    format_func=lambda x: x.capitalize(),
    key='selector_gobierno_desvios'
)

# Filtrar y agregar por tema (promedio de los desvíos del mandato)
desvios_gob = desvios[desvios['presidente'] == gob_seleccionado].copy()
desvios_avg = desvios_gob.groupby('tema')['desvio'].mean().reset_index()
desvios_avg = desvios_avg.sort_values('desvio', ascending=True)

# Colorear según signo
colores_barras = ['#dc2626' if v < 0 else '#16a34a' for v in desvios_avg['desvio']]

fig_desvios = go.Figure(data=go.Bar(
    y=desvios_avg['tema'],
    x=desvios_avg['desvio'],
    orientation='h',
    marker_color=colores_barras,
    hovertemplate='<b>%{y}</b><br>Desvío: %{x:+.2f} por mil palabras<extra></extra>',
    text=[f'{v:+.2f}' for v in desvios_avg['desvio']],
    textposition='outside',
))

fig_desvios.update_layout(
    height=550,
    xaxis_title='Desvío promedio (menciones por mil palabras)',
    yaxis_title='',
    template='plotly_white',
    margin=dict(t=30, b=30, l=10, r=10),
    showlegend=False,
)

# Línea vertical en cero
fig_desvios.add_vline(x=0, line_dash='solid', line_color='#94a3b8', line_width=1)

st.plotly_chart(fig_desvios, use_container_width=True)

# ============================================
# LIMITACIONES
# ============================================

st.markdown('<div class="section-header">Limitaciones de esta sección</div>', unsafe_allow_html=True)

st.markdown("""
<div class="limitation-box">
<strong>1. Frecuencia no es importancia.</strong> Este análisis mide cuánto aparecen 
ciertos temas, no qué tan centrales son. Un tema puede mencionarse poco pero ser 
simbólicamente clave (por ejemplo, los derechos humanos en la cuenta de 1990 de 
Aylwin).<br><br>

<strong>2. Las palabras cambian de significado.</strong> "Seguridad" en 1991 podía 
referirse a terrorismo político residual; en 2024 refiere mayormente a delincuencia 
y narcotráfico. Aunque la frecuencia sea comparable, el contenido no lo es 
necesariamente.<br><br>

<strong>3. Documentos con calidad técnica heterogénea.</strong> Algunos PDFs 
antiguos requirieron reconocimiento óptico de caracteres (OCR), lo cual puede 
introducir leves variaciones en el conteo.<br><br>

<strong>4. La fidelidad no es igual a calidad de gobierno.</strong> Un gobierno 
fiel a su programa no es necesariamente mejor ni peor. Cambios respecto del 
programa pueden reflejar adaptación legítima a circunstancias imprevistas.
</div>
""", unsafe_allow_html=True)