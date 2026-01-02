import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

# 1. FORZAR MODO CLARO A NIVEL DE NAVEGADOR
st.set_page_config(page_title="Búsqueda Protocolos", layout="wide")

# 2. CHAT FLOTANTE
def chat_flotante():
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

chat_flotante()

# 3. CSS "BLINDADO" CONTRA INVERSIÓN DE COLORES
st.markdown("""
    <style>
    /* Bloquea la inversión de colores del navegador */
    :root {
        color-scheme: light !important;
    }

    /* Fuerza fondo blanco y texto negro en todo */
    html, body, [data-testid="stAppViewContainer"], .stApp {
        background-color: #FFFFFF !important;
        color: #000000 !important;
    }

    /* Asegura que los títulos sean negros */
    h1, h2, h3, .filter-label {
        color: #000000 !important;
    }

    /* Estilo para las etiquetas de los filtros */
    .filter-label {
        font-weight: bold;
        font-size: 16px;
        margin-bottom: 5px;
        display: block;
    }

    /* Caja de búsqueda y Selectores con borde negro para que se vean */
    input, div[data-baseweb="select"] {
        background-color: #F8F9FA !important;
        color: #000000 !important;
        border: 2px solid #000000 !important;
    }

    /* Texto dentro de los menús desplegables */
    div[data-baseweb="select"] * {
        color: #000000 !important;
    }
    
    /* Forzar que la tabla de datos tenga texto negro */
    [data-testid="stDataFrame"] * {
        color: #000000 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 4. CARGA DE DATOS
@st.cache_data(ttl=30)
def load_data():
    # REEMPLAZA CON TU LINK DE GOOGLE SHEETS
    url = "TU_LINK_DE_GOOGLE_SHEETS_AQUI" 
    try:
        return pd.read_csv(url)
    except:
        # Fila de prueba para confirmar que se ve el negro
        return pd.DataFrame({'N°': ['1'], 'Hecho': ['Prueba Negro'], 'Realizado': ['OK'], 'Lo Tiene': ['SI'], 'Protocolo': ['A']})

df = load_data()

# --- INTERFAZ ---
st.title("Sistema de Búsqueda y Filtros")

st.markdown('<span class="filter-label">Buscador General</span>', unsafe_allow_html=True)
search_query = st.text_input("Buscador", placeholder="Escribe aquí para buscar...", label_visibility="collapsed")

st.markdown("<br>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown('<span class="filter-label">Filtrar por Hecho</span>', unsafe_allow_html=True)
    f_hecho = st.selectbox("H", ["Todos"] + sorted(list(df['Hecho'].unique())), key="h", label_visibility="collapsed")
with col2:
    st.markdown('<span class="filter-label">Filtrar por Realizado</span>', unsafe_allow_html=True)
    f_realizado = st.selectbox("R", ["Todos"] + sorted(list(df['Realizado'].unique())), key="r", label_visibility="collapsed")
with col3:
    st.markdown('<span class="filter-label">Filtrar por Lo Tiene</span>', unsafe_allow_html=True)
    f_lo_tiene = st.selectbox("L", ["Todos"] + sorted(list(df['Lo Tiene'].unique())), key="l", label_visibility="collapsed")

st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<span class="filter-label">Filtrar por Protocolo</span>', unsafe_allow_html=True)
f_protocolo = st.selectbox("P", ["Todos"] + sorted(list(df['Protocolo'].unique())), key="p", label_visibility="collapsed")

# Filtrado
filtered_df = df.copy()
if search_query:
    mask = df.apply(lambda row: row.astype(str).str.contains(search_query, case=False).any(), axis=1)
    filtered_df = filtered_df[mask]

# Tabla final
st.write(f"**Registros encontrados: {len(filtered_df)}**")
st.dataframe(filtered_df, use_container_width=True, hide_index=True)
