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

# 3. CSS PARA LETRAS GRANDES Y FONDO CLARO
st.markdown("""
    <style>
    /* Forzar fondo blanco */
    .stApp { background-color: white !important; }
    
    /* AGRANDAR LETRAS DE TODO EL SISTEMA */
    html, body, [class*="st-"] {
        font-size: 20px !important;
        color: black !important;
    }

    /* Títulos de los filtros más grandes y negros */
    label, .stMarkdown p {
        font-size: 22px !important;
        font-weight: bold !important;
        color: black !important;
    }

    /* Agrandar texto dentro de los cuadros (Inputs y Selects) */
    input, div[data-baseweb="select"] {
        font-size: 20px !important;
        height: 50px !important;
        border: 2px solid black !important;
    }
    
    /* Eliminar espacios vacíos innecesarios */
    .block-container { padding-top: 2rem; }
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
        return pd.DataFrame({'Estado': ['Cargando...'], 'Aviso': ['Pega el link de Sheets']})

df = load_data()

# 5. INTERFAZ VISUAL
st.markdown("<h1 style='text-align: center; color: black; font-size: 40px;'>Sistema de Búsqueda y Filtros</h1>", unsafe_allow_html=True)

# Buscador General
search_query = st.text_input("Buscador General (Escribe aquí)", placeholder="🔍 Buscar...")

st.markdown("---")

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

# 6. TABLA DE RESULTADOS (Sin error de width)
st.write(f"**Registros encontrados: {len(df_final)}**")
st.dataframe(df_final, use_container_width=True)
