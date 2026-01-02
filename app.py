import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

# 1. FORZAR MODO CLARO Y ELIMINAR MARGENES
st.set_page_config(page_title="Búsqueda Protocolos", layout="wide")

# 2. CHAT FLOTANTE CON ALTURA FORZADA (Para que aparezca sí o sí)
def chat_flotante():
    # Aumentamos el height a 1 para que el iframe exista pero no estorbe
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
    """, height=1)

chat_flotante()

# 3. CSS PARA FORZAR NEGRO ABSOLUTO
st.markdown("""
    <style>
    /* Forzar fondo blanco en toda la pantalla */
    .stApp { background-color: white !important; }
    
    /* Forzar color NEGRO en TODOS los textos posibles */
    h1, h2, h3, p, span, label, li, div, input, .stMarkdown {
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
    }

    /* Estilo de la barra de búsqueda */
    .stTextInput input {
        background-color: #f0f2f6 !important;
        border: 2px solid #000000 !important;
        color: #000000 !important;
    }

    /* Estilo de los Selectores (Filtros) */
    div[data-baseweb="select"] > div {
        background-color: #f0f2f6 !important;
        border: 2px solid #000000 !important;
    }
    
    /* Iconos y flechas en negro */
    svg { fill: #000000 !important; }
    
    /* Texto de los placeholders (lo que dice adentro antes de escribir) */
    ::placeholder { color: #444444 !important; opacity: 1; }
    </style>
    """, unsafe_allow_html=True)

# 4. CARGA DE DATOS (Asegúrate de poner tu link real aquí)
@st.cache_data(ttl=30)
def load_data():
    url = "TU_LINK_DE_GOOGLE_SHEETS_AQUI" 
    try:
        return pd.read_csv(url)
    except:
        # Datos visibles de prueba para confirmar que el color negro funciona
        data = {
            'N°': ['Prueba 1'], 'Fecha': ['2026-01-01'], 'Hora': ['12:00'], 
            'Falta': ['TEST'], 'Hecho': ['TEST'], 'Realizado': ['TEST'], 
            'Lo Tiene': ['TEST'], 'Protocolo': ['SI']
        }
        return pd.DataFrame(data)

df = load_data()

# --- INTERFAZ ---
st.title("Sistema de Búsqueda y Filtros")

st.write("### Buscador General")
search_query = st.text_input("Buscador", placeholder="Escribe aquí para buscar...", label_visibility="collapsed")

st.markdown("---")

# Filtros
c1, c2, c3 = st.columns(3)
with c1:
    st.write("**Filtrar por Hecho**")
    f_hecho = st.selectbox("H", ["Todos"] + sorted(list(df['Hecho'].unique())), key="h", label_visibility="collapsed")
with c2:
    st.write("**Filtrar por Realizado**")
    f_realizado = st.selectbox("R", ["Todos"] + sorted(list(df['Realizado'].unique())), key="r", label_visibility="collapsed")
with c3:
    st.write("**Filtrar por Lo Tiene**")
    f_lo_tiene = st.selectbox("L", ["Todos"] + sorted(list(df['Lo Tiene'].unique())), key="l", label_visibility="collapsed")

# Lógica de filtrado
filtered_df = df.copy()
if search_query:
    mask = df.apply(lambda row: row.astype(str).str.contains(search_query, case=False).any(), axis=1)
    filtered_df = filtered_df[mask]

# Tabla
st.write(f"**Registros encontrados: {len(filtered_df)}**")
st.dataframe(filtered_df, use_container_width=True, hide_index=True)
