"""
Discursos presidenciales chilenos 1990-2025
Plataforma de análisis para Unholster
"""

import streamlit as st

st.set_page_config(
    page_title="Discursos presidenciales chilenos",
    page_icon="📊",
    layout="wide",
)

st.title("Discursos presidenciales chilenos 1990-2025")
st.markdown("### Plataforma de análisis para Unholster")

st.markdown("""
Bienvenido. Esta plataforma analiza 35 años de discursos presidenciales chilenos
(programas de campaña y cuentas públicas anuales) usando técnicas de procesamiento
de texto y datos de opinión pública.

**Esta es una versión preliminar del proyecto. Las páginas se irán habilitando progresivamente.**

Use el menú lateral para navegar entre las distintas secciones de análisis.
""")

st.info("Proyecto en construcción — versión inicial del deploy.")