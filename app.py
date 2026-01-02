import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="Búsqueda Protocolos", layout="wide")

# 2. CHAT TAWK.TO (Sin tocar nada del script original)
components.html("""
<script type="text/javascript">
var Tawk_API=Tawk_API||{}, Tawk_LoadStart=new Date();
(function(){
var s1=document.createElement("script"),s0=document.getElementsByTagName("script")[0];
s1.async=true;
s1.src='https://embed.tawk.to/695732610a00df198198e359/1jdu9pk10';
s1.charset='UTF-8';
s1.setAttribute('crossorigin','*');
s0.parentNode.insertBefore(s1,s0);
})();
</script>
""", height=0)

# 3. CSS PARA SOLUCIONAR EL MODO OSCURO (Letras Negras)
st.markdown("""
    <style>
    /* Forzar fondo blanco */
    .stApp { background-color: white !important; }
    
    /* Forzar texto negro en todo (títulos, etiquetas y tablas) */
    h1, h2, h3, p, span, label, b, .stMarkdownContainer p { 
        color: black !important; 
        -webkit-text-fill-color: black !important;
    }
    
    /* Estilo para los cuadros de búsqueda y selectores */
    div[data-baseweb="select"] > div, input {
        border: 2px solid black !important;
        background-color: #f0f2f6 !important;
        color: black !important;
    }
    </style>
""", unsafe_allow_html=True)

# 4. CARGA DE DATOS
@st.cache_data(ttl=10)
def load_data():
    # REEMPLAZA ESTO CON TU LINK CSV DE GOOGLE SHEETS
    url = "TU_LINK_AQUI" 
    try:
        return pd.read_csv(url)
    except:
        return pd.DataFrame({'Estado': ['Cargando...'], 'Aviso': ['Pega el link de Sheets']})

df = load_data()

# 5. INTERFAZ (Corrigiendo el error de 'label' vacío de tus logs)
st.title("Sistema de Búsqueda y Filtros")

# SOLUCIÓN LOGS: No dejar el label vacío, usar un nombre real
search_query = st.text_input(label="Buscador General", placeholder="🔍 Buscar en todos los campos...")

st.markdown("---")

col1, col2, col3 = st.columns(3)
with col1:
    f_hecho = st.selectbox(label="Filtrar por Hecho", options=["Todos"] + (list(df['Hecho'].unique()) if 'Hecho' in df.columns else []))
with col2:
    f_realizado = st.selectbox(label="Filtrar por Realizado", options=["Todos"] + (list(df['Realizado'].unique()) if 'Realizado' in df.columns else []))
with col3:
    f_lo_tiene = st.selectbox(label="Filtrar por Lo Tiene", options=["Todos"] + (list(df['Lo Tiene'].unique()) if 'Lo Tiene' in df.columns else []))

# SOLUCIÓN LOGS: Actualización de use_container_width
st.dataframe(df, width=None) # width=None o width='stretch' según tu versión
# Lógica de filtrado (mantener igual)
filtered_df = df.copy()
if search_query:
    mask = df.apply(lambda row: row.astype(str).str.contains(search_query, case=False).any(), axis=1)
    filtered_df = filtered_df[mask]

# TABLA FINAL: Cambiamos width=None por use_container_width=True
st.markdown('<b style="color: black !important;">Resultados:</b>', unsafe_allow_html=True)
st.dataframe(filtered_df, use_container_width=True, hide_index=True)

# EL CHAT (mantener al final)
components.html("""
<script type="text/javascript">
var Tawk_API=Tawk_API||{}, Tawk_LoadStart=new Date();
(function(){
var s1=document.createElement("script"),s0=document.getElementsByTagName("script")[0];
s1.async=true;
s1.src='https://embed.tawk.to/695732610a00df198198e359/1jdu9pk10';
s1.charset='UTF-8';
s1.setAttribute('crossorigin','*');
s0.parentNode.insertBefore(s1,s0);
})();
</script>
""", height=0)
