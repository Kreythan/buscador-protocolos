import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

# 1. CONFIGURACIÓN DE PÁGINA (Sin temas automáticos)
st.set_page_config(page_title="Buscador", layout="wide")

# 2. EL CHAT (Tal cual lo pasaste, sin ninguna modificación)
# Lo ponemos arriba para que sea lo primero que intente cargar el navegador
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

# 3. FORZAR COLOR NEGRO (Estilo agresivo para celulares y PC)
st.markdown("""
    <style>
    /* Fondo blanco total */
    .stApp, [data-testid="stAppViewContainer"] { background-color: white !important; }
    
    /* Forzar texto negro con !important en cada etiqueta */
    h1, h2, h3, p, span, label, div, b { 
        color: #000000 !important; 
        -webkit-text-fill-color: #000000 !important;
    }

    /* Bordes de los filtros para que no se pierdan en el fondo */
    div[data-baseweb="select"] > div, input {
        border: 2px solid #000000 !important;
        background-color: #F0F2F6 !important;
    }
    </style>
""", unsafe_allow_html=True)

# 4. CARGA DE DATOS (Asegúrate de poner tu link de Google Sheets aquí)
@st.cache_data(ttl=5)
def load_data():
    url = "TU_LINK_DE_GOOGLE_SHEETS_AQUI" 
    try:
        return pd.read_csv(url)
    except:
        # Esto aparecerá si no hay link, verás el texto negro aquí
        return pd.DataFrame({'TEST': ['SI VES ESTO NEGRO, EL CODIGO ESTA BIEN']})

df = load_data()

# 5. CONTENIDO
st.title("🔎 Buscador de Protocolos")

st.write("### Buscador General")
search_query = st.text_input("B", placeholder="Escribe aquí...", label_visibility="collapsed")

st.markdown("---")

# Filtros
c1, c2, c3 = st.columns(3)
with c1:
    st.write("**Hecho:**")
    f_hecho = st.selectbox("1", ["Todos"] + list(df['Hecho'].unique()) if 'Hecho' in df.columns else ["Todos"], label_visibility="collapsed")
with c2:
    st.write("**Realizado:**")
    f_realizado = st.selectbox("2", ["Todos"] + list(df['Realizado'].unique()) if 'Realizado' in df.columns else ["Todos"], label_visibility="collapsed")
with c3:
    st.write("**Lo Tiene:**")
    f_lo_tiene = st.selectbox("3", ["Todos"] + list(df['Lo Tiene'].unique()) if 'Lo Tiene' in df.columns else ["Todos"], label_visibility="collapsed")

st.dataframe(df, use_container_width=True, hide_index=True)
