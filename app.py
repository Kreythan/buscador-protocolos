import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

# 1. FORZAR MODO CLARO Y CONFIGURACIÓN
st.set_page_config(page_title="Búsqueda Protocolos", layout="wide", initial_sidebar_state="collapsed")

# 2. CHAT FLOTANTE PERSONALIZADO
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

# 3. CSS BLINDADO PARA TEXTOS NEGROS
st.markdown("""
    <style>
    /* Fondo total blanco */
    .stApp, .main, .block-container { background-color: #FFFFFF !important; }

    /* Títulos y textos generales en Negro */
    h1, h2, h3, p, span, label, .stMarkdown {
        color: #000000 !important;
    }

    /* Estilo de los nombres de los filtros */
    .filter-title {
        color: #000000 !important;
        font-weight: bold !important;
        font-size: 16px !important;
        margin-bottom: 5px !important;
        display: block;
    }

    /* Forzar color negro dentro de la barra de búsqueda y selectores */
    input {
        color: #000000 !important;
        background-color: #F1F3F4 !important;
    }
    
    /* Color de los elementos seleccionados en los filtros */
    div[data-baseweb="select"] div {
        color: #000000 !important;
    }

    /* Bordes de los cuadros para que se vean */
    .stTextInput>div>div>input, div[data-baseweb="select"] {
        border: 1px solid #000000 !important;
        border-radius: 10px !important;
    }
    
    /* Eliminar el fondo oscuro de la tabla si existe */
    .stDataFrame { background-color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# 4. CARGA DE DATOS
@st.cache_data(ttl=60)
def load_data():
    # REEMPLAZA ESTE LINK CON TU CSV DE GOOGLE SHEETS
    url = "TU_LINK_DE_GOOGLE_SHEETS_AQUI" 
    try:
        df = pd.read_csv(url)
        return df
    except:
        # Datos de prueba para que veas los nombres de las columnas
        data = {'N°': [], 'Fecha': [], 'Hora': [], 'Falta': [], 'Hecho': [], 'Realizado': [], 'Lo Tiene': [], 'Protocolo': []}
        return pd.DataFrame(data)

df = load_data()

# --- INTERFAZ ---

st.title("Sistema de Búsqueda y Filtros")

# BUSCADOR
st.markdown('<span class="filter-title">Buscador General</span>', unsafe_allow_html=True)
search_query = st.text_input("Buscador", placeholder="Buscar en todos los campos...", label_visibility="collapsed")

st.markdown("<br>", unsafe_allow_html=True)

# FILTROS
c1, c2, c3 = st.columns(3)

with c1:
    st.markdown('<span class="filter-title">Filtrar por Hecho</span>', unsafe_allow_html=True)
    f_hecho = st.selectbox("H", ["Todos"] + sorted(list(df['Hecho'].unique())), key="h", label_visibility="collapsed")

with c2:
    st.markdown('<span class="filter-title">Filtrar por Realizado</span>', unsafe_allow_html=True)
    f_realizado = st.selectbox("R", ["Todos"] + sorted(list(df['Realizado'].unique())), key="r", label_visibility="collapsed")

with c3:
    st.markdown('<span class="filter-title">Filtrar por Lo Tiene</span>', unsafe_allow_html=True)
    f_lo_tiene = st.selectbox("L", ["Todos"] + sorted(list(df['Lo Tiene'].unique())), key="l", label_visibility="collapsed")

st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<span class="filter-title">Filtrar por Protocolo</span>', unsafe_allow_html=True)
f_protocolo = st.selectbox("P", ["Todos"] + sorted(list(df['Protocolo'].unique())), key="p", label_visibility="collapsed")

# LÓGICA FILTRADO
filtered_df = df.copy()
if search_query:
    mask = df.apply(lambda row: row.astype(str).str.contains(search_query, case=False).any(), axis=1)
    filtered_df = filtered_df[mask]

if f_hecho != "Todos": filtered_df = filtered_df[filtered_df['Hecho'] == f_hecho]
if f_realizado != "Todos": filtered_df = filtered_df[filtered_df['Realizado'] == f_realizado]
if f_lo_tiene != "Todos": filtered_df = filtered_df[filtered_df['Lo Tiene'] == f_lo_tiene]
if f_protocolo != "Todos": filtered_df = filtered_df[filtered_df['Protocolo'] == f_protocolo]

# TABLA
st.markdown(f'<p style="color:black; font-weight:bold;">Mostrando {len(filtered_df)} registros</p>', unsafe_allow_html=True)
st.dataframe(filtered_df, use_container_width=True, hide_index=True)
