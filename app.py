import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

# 1. CONFIGURACIÓN BÁSICA
st.set_page_config(page_title="Buscador", layout="wide")

# 2. TRUCO PARA LETRAS NEGRAS (CSS directo)
st.markdown("""
    <style>
    /* Forzar fondo blanco y letras negras en todo el sitio */
    .stApp { background-color: white !important; }
    h1, h2, h3, p, b, span, label { color: black !important; }
    
    /* Hacer que los cuadros de los filtros sean muy visibles */
    div[data-baseweb="select"] > div {
        background-color: #eeeeee !important;
        border: 2px solid black !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. CARGA DE DATOS (Recuerda poner tu link de Google Sheets aquí)
@st.cache_data(ttl=20)
def load_data():
    url = "TU_LINK_DE_GOOGLE_SHEETS_AQUI" 
    try:
        return pd.read_csv(url)
    except:
        return pd.DataFrame({'N°': ['1'], 'Hecho': ['Prueba'], 'Realizado': ['SI'], 'Lo Tiene': ['SI'], 'Protocolo': ['A']})

df = load_data()

# 4. DISEÑO DE LA PÁGINA
st.write("# 🔎 Buscador de Protocolos")

search_query = st.text_input("Buscador General", placeholder="Escribe aquí...")

col1, col2, col3 = st.columns(3)
with col1:
    f_hecho = st.selectbox("Filtrar por Hecho", ["Todos"] + list(df['Hecho'].unique()) if 'Hecho' in df.columns else ["Todos"])
with col2:
    f_realizado = st.selectbox("Filtrar por Realizado", ["Todos"] + list(df['Realizado'].unique()) if 'Realizado' in df.columns else ["Todos"])
with col3:
    f_lo_tiene = st.selectbox("Filtrar por Lo Tiene", ["Todos"] + list(df['Lo Tiene'].unique()) if 'Lo Tiene' in df.columns else ["Todos"])

st.dataframe(df, use_container_width=True, hide_index=True)

# 5. EL CHAT (Tal cual lo pasaste, dentro de la única función que lo hace funcionar)
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
