import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

# 1. CONFIGURACIÓN
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

# 3. CSS: ELIMINAR INTERFAZ DE ESCRITURA EN FILTROS
st.markdown("""
    <style>
    .stApp { background-color: white !important; }
    
    label { font-size: 20px !important; font-weight: bold !important; color: black !important; }

    /* BORDE EXTERIOR ÚNICO */
    [data-testid="stTextInput"] > div, 
    [data-testid="stSelectbox"] > div {
        background-color: white !important;
        border: 2px solid #000000 !important;
        border-radius: 8px !important;
        box-shadow: none !important;
    }

    /* ELIMINAR EL CUADRO INTERNO DE ESCRITURA EN LOS SELECTORES */
    div[data-baseweb="select"] > div:nth-child(1) {
        border: none !important;
        background-color: transparent !important;
        box-shadow: none !important;
    }

    /* OCULTAR EL CURSOR DE ESCRITURA EN LOS FILTROS */
    div[data-baseweb="select"] input {
        caret-color: transparent !important;
        cursor: pointer !important;
    }

    /* TEXTO NEGRO */
    input, div[data-baseweb="select"] span {
        color: black !important;
        font-size: 18px !important;
    }

    /* QUITAR SOMBRAS Y DOBLE BORDE AL HACER CLIC */
    div[data-baseweb="select"]:focus-within, input:focus {
        outline: none !important;
        border: none !important;
        box-shadow: none !important;
    }
    </style>
""", unsafe_allow_html=True)

# 4. CARGA DE DATOS
@st.cache_data(ttl=10)
def load_data():
    url = "TU_LINK_AQUI" 
    try:
        return pd.read_csv(url)
    except:
        return pd.DataFrame({'Hecho': ['Dato A', 'Dato B'], 'Realizado': ['SI', 'NO'], 'Lo Tiene': ['SI']})

df = load_data()

# 5. INTERFAZ
st.markdown("<h1 style='text-align: center; color: black;'>Sistema de Búsqueda</h1>", unsafe_allow_html=True)

# El buscador general sigue permitiendo escribir (es necesario)
search_query = st.text_input("Buscador General", placeholder="Escriba aquí...")

st.markdown("<br>", unsafe_allow_html=True)

# Filtros como listas desplegables
col1, col2, col3 = st.columns(3)
with col1:
    f_hecho = st.selectbox("Filtrar por Hecho", ["Todos"] + sorted(list(df['Hecho'].dropna().unique())))
with col2:
    f_realizado = st.selectbox("Filtrar por Realizado", ["Todos"] + sorted(list(df['Realizado'].dropna().unique())))
with col3:
    f_lo_tiene = st.selectbox("Filtrar por Lo Tiene", ["Todos"] + sorted(list(df['Lo Tiene'].dropna().unique())))

# 6. RESULTADOS
df_final = df.copy()
if search_query:
    df_final = df_final[df_final.apply(lambda row: row.astype(str).str.contains(search_query, case=False).any(), axis=1)]

st.dataframe(df_final, use_container_width=True)
