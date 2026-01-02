import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

# 1. CONFIGURACIÓN INICIAL
st.set_page_config(page_title="Búsqueda Protocolos", layout="wide")

# 2. CHAT FLOTANTE PERSONALIZADO (Tu código Tawk.to)
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
    """, height=100)

chat_flotante()

# 3. CSS EXTREMO: FUERZA EL COLOR NEGRO EN CUALQUIER TEMA
st.markdown("""
    <style>
    /* Forzar fondo blanco en toda la aplicación */
    html, body, [data-testid="stAppViewContainer"], .main, .stApp {
        background-color: white !important;
    }

    /* Forzar color NEGRO en absolutamente todos los textos */
    h1, h2, h3, p, span, label, div, input, .stMarkdown, [data-testid="stMarkdownContainer"] p {
        color: #000000 !important;
        fill: #000000 !important;
    }

    /* Estilo de los nombres de los filtros */
    .filter-label {
        color: #000000 !important;
        font-weight: bold !important;
        font-size: 16px !important;
        margin-bottom: 5px;
    }

    /* Barra de búsqueda y Selectores */
    input[type="text"], .stTextInput div div input, div[data-baseweb="select"] {
        background-color: #F1F3F4 !important;
        color: #000000 !important;
        border: 1px solid #000000 !important;
    }
    
    /* Color de las flechas y textos de selección */
    div[data-baseweb="select"] * {
        color: #000000 !important;
    }
    
    /* Forzar tabla blanca con texto negro */
    [data-testid="stDataFrame"] {
        background-color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 4. CARGA DE DATOS
@st.cache_data(ttl=30)
def load_data():
    # REEMPLAZA ESTE LINK CON TU CSV DE GOOGLE SHEETS
    url = "TU_LINK_DE_GOOGLE_SHEETS_AQUI" 
    try:
        df = pd.read_csv(url)
        return df
    except:
        # Datos ficticios para verificar que el texto negro funciona
        data = {
            'N°': ['001'], 'Fecha': ['2026-01-01'], 'Hora': ['08:00'], 
            'Falta': ['Ejemplo'], 'Hecho': ['Ejemplo'], 'Realizado': ['Ejemplo'], 
            'Lo Tiene': ['Ejemplo'], 'Protocolo': ['Sí']
        }
        return pd.DataFrame(data)

df = load_data()

# --- INTERFAZ ---
st.title("Sistema de Búsqueda y Filtros")

st.markdown('<p class="filter-label">Buscador General</p>', unsafe_allow_html=True)
search_query = st.text_input("Buscador", placeholder="Escriba aquí para buscar...", label_visibility="collapsed")

st.markdown("<br>", unsafe_allow_html=True)

# Filtros en columnas
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown('<p class="filter-label">Filtrar por Hecho</p>', unsafe_allow_html=True)
    f_hecho = st.selectbox("H", ["Todos"] + sorted(list(df['Hecho'].unique())), key="h", label_visibility="collapsed")
with c2:
    st.markdown('<p class="filter-label">Filtrar por Realizado</p>', unsafe_allow_html=True)
    f_realizado = st.selectbox("R", ["Todos"] + sorted(list(df['Realizado'].unique())), key="r", label_visibility="collapsed")
with c3:
    st.markdown('<p class="filter-label">Filtrar por Lo Tiene</p>', unsafe_allow_html=True)
    f_lo_tiene = st.selectbox("L", ["Todos"] + sorted(list(df['Lo Tiene'].unique())), key="l", label_visibility="collapsed")

st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<p class="filter-label">Filtrar por Protocolo</p>', unsafe_allow_html=True)
f_protocolo = st.selectbox("P", ["Todos"] + sorted(list(df['Protocolo'].unique())), key="p", label_visibility="collapsed")

# Lógica de filtrado
filtered_df = df.copy()
if search_query:
    mask = df.apply(lambda row: row.astype(str).str.contains(search_query, case=False).any(), axis=1)
    filtered_df = filtered_df[mask]

# Mostrar Resultados
st.markdown(f'<p style="color:black;">Mostrando {len(filtered_df)} registros encontrados</p>', unsafe_allow_html=True)
st.dataframe(filtered_df, use_container_width=True, hide_index=True)
