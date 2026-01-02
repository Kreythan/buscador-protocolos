import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="Búsqueda Protocolos", layout="wide")

# 2. ESCUDO ANTI-MODO OSCURO (CSS directo al HTML)
# Esto obliga al navegador a no invertir colores
st.markdown(""
    <style>
    :root { color-scheme: light !important; }
    html, body, [data-testid="stAppViewContainer"] {
        background-color: white !important;
        color: black !important;
    }
    /* Forzar negro en todos los textos de Streamlit */
    .stMarkdown, p, span, h1, h2, h3, label {
        color: black !important;
    }
    /* Estilo de inputs */
    input {
        color: black !important;
        border: 2px solid black !important;
    }
    </style>
"", unsafe_allow_html=True)

# 3. CARGA DE DATOS
@st.cache_data(ttl=20)
def load_data():
    url = "TU_LINK_DE_GOOGLE_SHEETS_AQUI" 
    try:
        return pd.read_csv(url)
    except:
        return pd.DataFrame({'Estado': ['Esperando datos...'], 'Aviso': ['Pega el link de Google Sheets']})

df = load_data()

# 4. INTERFAZ VISUAL
st.title("🔎 Sistema de Búsqueda")

# Buscador con estilo manual
st.write("### Buscador General")
search_query = st.text_input("buscador_input", placeholder="Escribe para buscar...", label_visibility="collapsed")

st.markdown("---")

# Filtros
c1, c2, c3 = st.columns(3)
with c1:
    st.write("**Hecho**")
    f_hecho = st.selectbox("H", ["Todos"] + (sorted(list(df['Hecho'].unique())) if 'Hecho' in df.columns else []), label_visibility="collapsed")
with c2:
    st.write("**Realizado**")
    f_realizado = st.selectbox("R", ["Todos"] + (sorted(list(df['Realizado'].unique())) if 'Realizado' in df.columns else []), label_visibility="collapsed")
with c3:
    st.write("**Lo Tiene**")
    f_lo_tiene = st.selectbox("L", ["Todos"] + (sorted(list(df['Lo Tiene'].unique())) if 'Lo Tiene' in df.columns else []), label_visibility="collapsed")

# Tabla de resultados
st.dataframe(df, use_container_width=True, hide_index=True)

# 5. CONTENEDOR ESPECIAL PARA EL CHAT (Al final para evitar errores)
# Usamos un truco para que el script no se rompa por las comillas
tawk_script = """
var Tawk_API=Tawk_API||{}, Tawk_LoadStart=new Date();
Tawk_API.customStyle = {
    visibility : {
        desktop : { xOffset : 20, yOffset : 20 },
        mobile : { xOffset : 10, yOffset : 10 }
    }
};
(function(){
var s1=document.createElement("script"),s0=document.getElementsByTagName("script")[0];
s1.async=true;
s1.src='https://embed.tawk.to/695732610a00df198198e359/1jdu9pk10';
s1.charset='UTF-8';
s1.setAttribute('crossorigin','*');
s0.parentNode.insertBefore(s1,s0);
})();
"""

# Inyectamos el componente en un contenedor pequeño
with st.container():
    components.html(f"<script>{tawk_script}</script>", height=0)
