import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="Búsqueda Protocolos", layout="wide")

# 2. CHAT TAWK.TO (Script Original)
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

# 3. CSS PARA DISEÑO LIMPIO (BLANCO TOTAL Y BORDE ÚNICO)
st.markdown("""
    <style>
    /* Fondo general blanco */
    .stApp { background-color: white !important; }
    
    /* Títulos de los campos */
    label, .stMarkdown p {
        font-size: 20px !important;
        font-weight: bold !important;
        color: black !important;
        margin-bottom: 8px !important;
    }

    /* CORRECCIÓN: Fondo blanco total (quita el plomo) y borde negro simple */
    input, div[data-baseweb="select"] > div {
        background-color: white !important; 
        border: 2.5px solid #000000 !important; 
        box-shadow: none !important; /* Elimina sombras que parecen doble borde */
        border-radius: 8px !important;
        height: 50px !important;
    }

    /* Asegurar que el fondo del contenedor del select sea blanco */
    div[data-baseweb="select"] {
        background-color: transparent !important;
        border: none !important;
    }

    /* Texto negro dentro de los cuadros */
    input, div[data-baseweb="select"] div, div[data-baseweb="select"] span {
        color: black !important;
        font-size: 18px !important;
    }

    /* Eliminar el efecto de borde azul/sombra al hacer clic */
    input:focus, div[data-baseweb="select"]:focus-within {
        border-color: #000000 !important;
        box-shadow: none !important;
        outline: none !important;
    }

    /* Quitar bordes internos de Streamlit */
    [data-testid="stTextInput"] > div, [data-testid="stSelectbox"] > div {
        border: none !important;
        box-shadow: none !important;
    }

    .stDataFrame { border: none !important; }
    </style>
""", unsafe_allow_html=True)

# 4. CARGA DE DATOS
@st.cache_data(ttl=10)
def load_data():
    url = "TU_LINK_AQUI" # Reemplaza con tu link real de Google Sheets
    try:
        return pd.read_csv(url)
    except:
        return pd.DataFrame({
            'Hecho': ['Ejemplo A', 'Ejemplo B'], 
            'Realizado': ['SI', 'NO'], 
            'Lo Tiene': ['SI', 'NO']
        })

df = load_data()

# 5. INTERFAZ VISUAL
st.markdown("<h1 style='text-align: center; color: black; font-size: 36px;'>Sistema de Búsqueda y Filtros</h1>", unsafe_allow_html=True)

# Buscador General
search_query = st.text_input("Buscador General (Escribe aquí)", placeholder="🔍 Buscar...")

st.markdown("<br>", unsafe_allow_html=True)

# Filtros en 3 columnas
col1, col2, col3 = st.columns(3)

with col1:
    opciones_hecho = ["Todos"] + (sorted(list(df['Hecho'].dropna().unique())) if 'Hecho' in df.columns else [])
    f_hecho = st.selectbox("Filtrar por Hecho", opciones_hecho)

with col2:
    opciones_realizado = ["Todos"] + (sorted(list(df['Realizado'].dropna().unique())) if 'Realizado' in df.columns else [])
    f_realizado = st.selectbox("Filtrar por Realizado", opciones_realizado)

with col3:
    opciones_lo_tiene = ["Todos"] + (sorted(list(df['Lo Tiene'].dropna().unique())) if 'Lo Tiene' in df.columns else [])
    f_lo_tiene = st.selectbox("Filtrar por Lo Tiene", opciones_lo_tiene)

# Lógica de Filtrado
df_final = df.copy()
if search_query:
    df_final = df_final[df_final.apply(lambda row: row.astype(str).str.contains(search_query, case=False).any(), axis=1)]
if f_hecho != "Todos":
    df_final = df_final[df_final['Hecho'] == f_hecho]
if f_realizado != "Todos":
    df_final = df_final[df_final['Realizado'] == f_realizado]
if f_lo_tiene != "Todos":
    df_final = df_final[df_final['Lo Tiene'] == f_lo_tiene]

# 6. TABLA DE RESULTADOS
st.markdown(f"<h3 style='color: black;'>Registros encontrados: {len(df_final)}</h3>", unsafe_allow_html=True)
st.dataframe(df_final, use_container_width=True)
