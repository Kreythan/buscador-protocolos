import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

# 1. FORZAR MODO CLARO Y TEXTO NEGRO (CSS BÁSICO)
st.markdown("""
    <style>
    .stApp { background-color: white !important; }
    * { color: black !important; -webkit-text-fill-color: black !important; }
    div[data-baseweb="select"] > div, input {
        border: 2px solid black !important;
        background-color: #f0f2f6 !important;
    }
    </style>
""", unsafe_allow_html=True)

# 2. EL CHAT (Tu código original sin tocar nada)
# Usamos las triples comillas para proteger el script
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

# 3. INTERFAZ SIMPLE
st.title("🔎 Sistema de Búsqueda")

# Carga de datos segura
try:
    # REEMPLAZA ESTO CON TU LINK CSV DE GOOGLE SHEETS
    url = "TU_LINK_AQUI"
    df = pd.read_csv(url)
except:
    df = pd.DataFrame({'Columna': ['Sin datos'], 'Info': ['Pega el link de Sheets']})

st.write("### Buscador")
search = st.text_input("Buscar...", label_visibility="collapsed")

st.dataframe(df, use_container_width=True)
