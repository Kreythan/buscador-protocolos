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

# 3. CSS: LIMPIEZA TOTAL Y BUSCADOR BLANCO
st.markdown("""
    <style>
    /* Fondo general de la app */
    .stApp { background-color: white !important; }
    
    label { font-size: 20px !important; font-weight: bold !important; color: black !important; }

    /* BORDE NEGRO ÚNICO Y FONDO BLANCO PARA TODOS LOS CUADROS */
    [data-testid="stTextInput"] > div, 
    [data-testid="stSelectbox"] > div {
        background-color: white !important;
        border: 2px solid #000000 !important;
        border-radius: 8px !important;
        box-shadow: none !important;
    }

    /* ELIMINAR EL COLOR PLOMO INTERNO DEL BUSCADOR */
    [data-testid="stTextInput"] input {
        background-color: white !important;
        color: black !important;
        border: none !important;
        box-shadow: none !important;
    }

    /* QUITAR EL FONDO GRIS CUANDO SE HACE CLIC (FOCUS) */
    [data-testid="stTextInput"] > div:focus-within {
        background-color: white !important;
        border-color: #000000 !important;
        box-shadow: none !important;
    }

    /* HACER QUE EL SELECTOR SEA SOLO LISTA (No escritura) */
    div[data-baseweb="select"] input {
        caret-color: transparent !important;
        cursor: pointer !important;
    }

    /* TEXTO NEGRO EN TODO */
    input, div[data-baseweb="select"] span {
        color: black !important;
        font-size: 18px !important;
    }

    /* ELIMINAR CUALQUIER SOMBRA O BORDE ROJO DE ERROR */
    [data-testid="stTextInput"] > div > div, 
    [data-testid="stSelectbox"] > div > div {
        border: none !important;
        box-shadow: none !important;
        outline: none !important;
    }
    </style>
""", unsafe_allow_html=True)

# 4. CARGA DE DATOS
@st.cache_data(ttl=10)
def load_data():
    # IMPORTANTE: Reemplaza las comillas de abajo por tu link de Google Sheets
    url = "TU_LINK_DE_GOOGLE_SHEETS_AQUI" 
    try:
        return pd.read_csv(url)
    except:
        # Datos de prueba corregidos (todos tienen la misma cantidad de elementos)
        return pd.DataFrame({
            'Hecho': ['Esperando Link', 'Configura el CSV'],
            'Realizado': ['NO', 'NO'],
            'Lo Tiene': ['NO', 'NO']
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

st.dataframe(df_final, use_container_width=True)
