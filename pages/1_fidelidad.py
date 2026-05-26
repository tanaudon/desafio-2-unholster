"""
Página 1: Fidelidad programática.

Compara los temas anunciados en el programa de gobierno con los temas
efectivamente desarrollados en las cuentas públicas anuales.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

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
st.markdown('<div class="page-subtitle">¿Hablan los gobiernos de lo que prometen?</div>', unsafe_allow_html=True)

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

# Iterar por cada combinación presidente + año_programa (porque Bachelet y Piñera tienen 2 mandatos cada uno)
for (pres, año_prog), datos_pres in fidelidad.groupby(['presidente', 'año_programa']):
    datos_pres = datos_pres.sort_values('año_cuenta')
    
    # Etiqueta legible
    if pres == 'bachelet' and año_prog == 2006:
        nombre = 'Bachelet I (2006-2009)'
        dash = 'solid'
    elif pres == 'bachelet' and año_prog == 2014:
        nombre = 'Bachelet II (2014-2017)'
        dash = 'dot'
    elif pres == 'pinera' and año_prog == 2010:
        nombre = 'Piñera I (2010-2013)'
        dash = 'solid'
    elif pres == 'pinera' and año_prog == 2018:
        nombre = 'Piñera II (2018-2021)'
        dash = 'dot'
    else:
        nombre = pres.capitalize()
        dash = 'solid'
    
    fig_trayectoria.add_trace(go.Scatter(
        x=datos_pres['año_cuenta'],
        y=datos_pres['fidelidad'],
        mode='lines+markers',
        name=nombre,
        line=dict(color=COLORES_PRES[pres], width=2.5, dash=dash),
        marker=dict(size=9),
        hovertemplate='<b>%{x}</b><br>Fidelidad: %{y:.3f}<extra></extra>'
    ))

fig_trayectoria.update_layout(
    height=480,
    xaxis_title='Año de la cuenta pública',
    yaxis_title='Fidelidad (Jensen-Shannon)',
    yaxis=dict(range=[0.7, 1.0]),
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
(cambio total del top temático). <em>Pase el cursor sobre cada celda para 
ver qué temas componen el top-3 del programa y de la cuenta.</em>
</div>
""", unsafe_allow_html=True)

# Crear etiqueta de "gobierno-mandato"
def etiqueta_mandato(row):
    if row['presidente'] == 'bachelet' and row['año_programa'] == 2006:
        return 'Bachelet I'
    elif row['presidente'] == 'bachelet' and row['año_programa'] == 2014:
        return 'Bachelet II'
    elif row['presidente'] == 'pinera' and row['año_programa'] == 2010:
        return 'Piñera I'
    elif row['presidente'] == 'pinera' and row['año_programa'] == 2018:
        return 'Piñera II'
    else:
        return row['presidente'].capitalize()

top3 = top3.copy()
top3['mandato'] = top3.apply(etiqueta_mandato, axis=1)

# Orden cronológico
orden_mandatos = ['Aylwin', 'Frei', 'Lagos', 'Bachelet I', 'Piñera I', 'Bachelet II', 'Piñera II', 'Boric']
orden_existente = [m for m in orden_mandatos if m in top3['mandato'].unique()]

# Construir matriz de coincidencias y matriz de hover personalizado
años_unicos = sorted(top3['año_cuenta'].unique())

z_values = []      # Para colorear
text_values = []   # Para mostrar el número en la celda
hover_text = []    # Para el hover detallado

for mandato in orden_existente:
    fila_z = []
    fila_text = []
    fila_hover = []
    for año in años_unicos:
        match = top3[(top3['mandato'] == mandato) & (top3['año_cuenta'] == año)]
        if match.empty:
            fila_z.append(None)
            fila_text.append('')
            fila_hover.append('')
        else:
            row = match.iloc[0]
            fila_z.append(row['coincidencias'])
            fila_text.append(str(int(row['coincidencias'])))
            hover = (
                f"<b>{mandato} — Cuenta {año}</b><br><br>"
                f"<b>Top-3 del programa:</b><br>{row['top3_programa']}<br><br>"
                f"<b>Top-3 de la cuenta:</b><br>{row['top3_cuenta']}<br><br>"
                f"<b>Coincidencias:</b> {int(row['coincidencias'])}/3"
            )
            fila_hover.append(hover)
    z_values.append(fila_z)
    text_values.append(fila_text)
    hover_text.append(fila_hover)

fig_top3 = go.Figure(data=go.Heatmap(
    z=z_values,
    x=años_unicos,
    y=orden_existente,
    text=text_values,
    texttemplate='%{text}',
    textfont={"size": 13, "color": "#0f172a"},
    customdata=hover_text,
    hovertemplate='%{customdata}<extra></extra>',
    colorscale=[
        [0, '#fecaca'],
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
        len=0.7,
    ),
    showscale=True,
    xgap=2,
    ygap=2,
))

fig_top3.update_layout(
    height=380,
    xaxis_title='Año de la cuenta pública',
    yaxis_title='',
    template='plotly_white',
    margin=dict(t=30, b=30, l=10, r=10),
    plot_bgcolor='white',
)

# Invertir orden Y para que el gobierno más antiguo quede arriba
fig_top3.update_yaxes(autorange='reversed')

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

# Agregar etiqueta de mandato también a desvios
desvios = desvios.copy()
desvios['mandato'] = desvios.apply(etiqueta_mandato, axis=1)

# Selector de mandato
mandatos_disponibles = [m for m in orden_mandatos if m in desvios['mandato'].unique()]
mandato_seleccionado = st.selectbox(
    'Seleccione un gobierno:',
    options=mandatos_disponibles,
    key='selector_mandato_desvios'
)

# Filtrar y agregar por tema (promedio de los desvíos del mandato)
desvios_gob = desvios[desvios['mandato'] == mandato_seleccionado].copy()
desvios_avg = desvios_gob.groupby('tema')['diferencia'].mean().reset_index()
desvios_avg = desvios_avg.sort_values('diferencia', ascending=True)

# Colorear según signo
colores_barras = ['#dc2626' if v < 0 else '#16a34a' for v in desvios_avg['diferencia']]

fig_desvios = go.Figure(data=go.Bar(
    y=desvios_avg['tema'],
    x=desvios_avg['diferencia'],
    orientation='h',
    marker_color=colores_barras,
    hovertemplate='<b>%{y}</b><br>Desvío: %{x:+.2f} por mil palabras<extra></extra>',
    text=[f'{v:+.2f}' for v in desvios_avg['diferencia']],
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