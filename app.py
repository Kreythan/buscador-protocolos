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

# 3. CSS PARA CUADROS BLANCOS Y LETRAS GRANDES
st.markdown("""
    <style>
    /* Fondo general de la app siempre blanco */
    .stApp { background-color: white !important; }
    
    /* Etiquetas de los filtros (Títulos) */
    label, .stMarkdown p {
        font-size: 22px !important;
        font-weight: bold !important;
        color: black !important;
    }

    /* UNIFICACIÓN: Buscador y Selectores con fondo BLANCO */
    input, div[data-baseweb="select"] {
        background-color: #FFFFFF !important; /* Fondo Blanco */
        border: 2px solid #262730 !important;  /* Borde oscuro para contraste */
        border-radius: 10px !important;
        height: 55px !important;
    }

    /* Forzar color de texto NEGRO dentro de los cuadros */
    input, div[data-baseweb="select"] div, div[data-baseweb="select"] span {
        color: black !important;
        font-size: 20px !important;
    }

    /* Estilo para el buscador específico al escribir */
    .stTextInput input {
        color: black !important;
    }

    /* Lista desplegable de los filtros */
    div[role="listbox"] {
        background-color: white !important;
    }
    
    div[role="option"] {
        color: black !important;
    }

    /* Quitar bordes rojos de error o advertencia */
    .stDataFrame { border: none !important; }
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
        return pd.DataFrame({
            'Hecho': ['Ejemplo A', 'Ejemplo B'], 
            'Realizado': ['SI', 'NO'], 
            'Lo Tiene': ['SI', 'NO']
        })

df = load_data()

# 5. INTERFAZ VISUAL
st.markdown("<h1 style='text-align: center; color: black; font-size: 42px;'>Sistema de Búsqueda y Filtros</h1>", unsafe_allow_html=True)

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
