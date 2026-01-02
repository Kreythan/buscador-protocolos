import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="Búsqueda Protocolos", layout="wide")

# 2. CHAT TAWK.TO
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

# 3. CSS MAESTRO: LIMPIEZA TOTAL DE BORDES INTERNOS
st.markdown("""
    <style>
    /* Fondo general */
    .stApp { background-color: white !important; }
    
    /* Títulos */
    label, .stMarkdown p {
        font-size: 20px !important;
        font-weight: bold !important;
        color: black !important;
    }

    /* ELIMINAR BORDE INTERNO AL ESCRIBIR (Focus) */
    /* Aplicamos transparencia a cualquier borde que Streamlit intente dibujar dentro */
    [data-testid="stTextInput"] > div > div, 
    [data-testid="stSelectbox"] > div > div {
        border: none !important;
        box-shadow: none !important;
        outline: none !important;
    }

    /* BORDE EXTERIOR ÚNICO: Negro sólido y fondo blanco puro */
    input, div[data-baseweb="select"] > div {
        background-color: white !important; 
        border: 2px solid #000000 !important; 
        border-radius: 8px !important;
        height: 50px !important;
        box-shadow: none !important;
    }

    /* Forzar que el fondo no se vuelva plomo al seleccionar */
    div[data-baseweb="select"] {
        background-color: white !important;
    }

    /* Texto negro */
    input, div[data-baseweb="select"] div, div[data-baseweb="select"] span {
        color: black !important;
        font-size: 18px !important;
    }

    /* Quitar cualquier sombra o resplandor al hacer clic */
    input:focus, div[data-baseweb="select"]:focus-within {
        outline: none !important;
        border-color: #000000 !important;
        box-shadow: none !important;
    }
    
    /* Limpieza de la tabla */
    .stDataFrame { border: none !important; }
    </style>
""", unsafe_allow_html=True)

# 4. CARGA DE DATOS
@st.cache_data(ttl=10)
def load_data():
    url = "TU_LINK_AQUI" 
    try:
        return pd.read_csv(url)
    except:
        return pd.DataFrame({'Hecho': ['Prueba'], 'Realizado': ['SI'], 'Lo Tiene': ['SI']})

df = load_data()

# 5. INTERFAZ
st.markdown("<h1 style='text-align: center; color: black;'>Sistema de Búsqueda</h1>", unsafe_allow_html=True)

search_query = st.text_input("Buscador General", placeholder="Escriba para buscar...")

st.markdown("<br>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    f_hecho = st.selectbox("Filtrar por Hecho", ["Todos"] + sorted(list(df['Hecho'].dropna().unique())) if 'Hecho' in df.columns else ["Todos"])
with col2:
    f_realizado = st.selectbox("Filtrar por Realizado", ["Todos"] + sorted(list(df['Realizado'].dropna().unique())) if 'Realizado' in df.columns else ["Todos"])
with col3:
    f_lo_tiene = st.selectbox("Filtrar por Lo Tiene", ["Todos"] + sorted(list(df['Lo Tiene'].dropna().unique())) if 'Lo Tiene' in df.columns else ["Todos"])

# Filtrado y Tabla
df_final = df.copy()
if search_query:
    df_final = df_final[df_final.apply(lambda row: row.astype(str).str.contains(search_query, case=False).any(), axis=1)]

st.markdown(f"**Registros: {len(df_final)}**")
st.dataframe(df_final, use_container_width=True)
