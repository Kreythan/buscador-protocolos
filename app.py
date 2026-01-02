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

# 3. CSS: BLOQUEO DE COLOR OSCURO EN BUSCADOR
st.markdown("""
    <style>
    .stApp { background-color: white !important; }
    label { font-size: 20px !important; font-weight: bold !important; color: black !important; }

    /* --- BARRA DE BÚSQUEDA GENERAL (FORZAR OSCURO SIEMPRE) --- */
    /* Este bloque asegura que el contenedor no se vuelva blanco al escribir */
    [data-testid="stTextInput"] > div, 
    [data-testid="stTextInput"] > div:focus-within,
    [data-testid="stTextInput"] > div[data-baseweb="input"] {
        background-color: #262730 !important; 
        border: 2px solid #000000 !important;
        border-radius: 8px !important;
        box-shadow: none !important;
    }

    /* Forzar letras blancas y fondo transparente del input interno */
    [data-testid="stTextInput"] input {
        color: white !important;
        background-color: transparent !important;
        -webkit-text-fill-color: white !important; /* Para navegadores basados en Safari/Chrome */
    }

    /* Eliminar el cuadrito "Press Enter" y botones */
    [data-testid="stTextInput"] [data-testid="InputInstructions"],
    [data-testid="stTextInput"] button {
        display: none !important;
    }

    /* --- FILTROS (SELECTBOX) --- */
    [data-testid="stSelectbox"] > div {
        background-color: white !important;
        border: 2px solid #000000 !important;
        border-radius: 8px !important;
    }

    div[data-baseweb="select"] input {
        caret-color: transparent !important;
        cursor: pointer !important;
    }

    div[data-baseweb="select"] span {
        color: black !important;
        font-size: 18px !important;
    }

    /* Limpieza de bordes internos */
    [data-testid="stTextInput"] > div > div, 
    [data-testid="stSelectbox"] > div > div {
        border: none !important;
        box-shadow: none !important;
        background-color: transparent !important;
    }
    
    div[data-baseweb="select"] > div {
        background-color: white !important;
    }
    </style>
""", unsafe_allow_html=True)

# 4. CARGA DE DATOS
@st.cache_data(ttl=10)
def load_data():
    url = "TU_LINK_DE_GOOGLE_SHEETS_AQUI" 
    try:
        return pd.read_csv(url)
    except:
        return pd.DataFrame({
            'Hecho': ['Dato A', 'Dato B'],
            'Realizado': ['SI', 'NO'],
            'Lo Tiene': ['SI', 'NO']
        })

df = load_data()

# 5. INTERFAZ
st.markdown("<h1 style='text-align: center; color: black;'>Sistema de Búsqueda</h1>", unsafe_allow_html=True)

search_query = st.text_input("Buscador General", placeholder="Escriba aquí para buscar...")

st.markdown("<br>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    f_hecho = st.selectbox("Filtrar por Hecho", ["Todos"] + sorted(list(df['Hecho'].dropna().unique())))
with col2:
    f_realizado = st.selectbox("Filtrar por Realizado", ["Todos"] + sorted(list(df['Realizado'].dropna().unique())))
with col3:
    f_lo_tiene = st.selectbox("Filtrar por Lo Tiene", ["Todos"] + sorted(list(df['Lo Tiene'].dropna().unique())))

# 6. FILTRADO Y TABLA
df_final = df.copy()
if search_query:
    df_final = df_final[df_final.apply(lambda row: row.astype(str).str.contains(search_query, case=False).any(), axis=1)]
if f_hecho != "Todos":
    df_final = df_final[df_final['Hecho'] == f_hecho]
if f_realizado != "Todos":
    df_final = df_final[df_final['Realizado'] == f_realizado]
if f_lo_tiene != "Todos":
    df_final = df_final[df_final['Lo Tiene'] == f_lo_tiene]

st.markdown(f"**Registros encontrados: {len(df_final)}**")
st.dataframe(df_final, use_container_width=True)
