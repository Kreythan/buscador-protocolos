import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

# 1. FORZAR MODO CLARO Y CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="Búsqueda Protocolos", layout="wide")

# 2. CHAT FLOTANTE (Configurado a la IZQUIERDA con retraso de carga)
def chat_flotante():
    # El height=1 permite que el script se ejecute sin ocupar espacio visual
    components.html("""
        <script type="text/javascript">
        var Tawk_API=Tawk_API||{}, Tawk_LoadStart=new Date();
        
        // FORZAR POSICIÓN IZQUIERDA
        Tawk_API.onLoad = function(){
            Tawk_API.setAttributes({
                'placement' : 'bottom-left'
            }, function(error){});
        };

        Tawk_API.customStyle = {
            visibility : {
                desktop : { xOffset : 20, yOffset : 20 },
                mobile : { xOffset : 10, yOffset : 10 }
            }
        };

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

# 3. CSS "ESCUDO NEGRO" (Bloquea modos oscuros de Chrome/Edge)
st.markdown("""
    <style>
    /* Bloqueo de inversión de color del navegador */
    :root { color-scheme: light !important; }
    html, body { filter: none !important; -webkit-filter: none !important; }

    /* Fondo blanco obligatorio */
   

    /* FORZAR TEXTO NEGRO EN TODO */
    * {
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
    }

    /* Estilo de los nombres de filtros */
    .titulos-negros {
        color: #000000 !important;
        font-weight: bold !important;
        font-size: 16px !important;
        margin-bottom: 5px;
        display: block;
    }

    /* Bordes y fondo de inputs */
    input, div[data-baseweb="select"] {
        border: 2px solid #000000 !important;
        background-color: #F8F9FA !important;
        border-radius: 8px !important;
    }
    
    /* Asegurar visibilidad de tabla */
    [data-testid="stDataFrame"] { background-color: white !important; }
    </style>
    """, unsafe_allow_html=True)

# 4. CARGA DE DATOS (PON TU LINK AQUÍ)
@st.cache_data(ttl=10)
def load_data():
    url = "TU_LINK_DE_GOOGLE_SHEETS_AQUI" 
    try:
        return pd.read_csv(url)
    except:
        # Fila de prueba garantizada para ser visible
        return pd.DataFrame({'N°': ['1'], 'Dato': ['SI VES ESTO NEGRO, FUNCIONA']})

df = load_data()

# --- INTERFAZ ---
st.markdown('<h1 style="color: black !important; text-align: center;">Sistema de Búsqueda y Filtros</h1>', unsafe_allow_html=True)

st.markdown('<span class="titulos-negros">Buscador General</span>', unsafe_allow_html=True)
search_query = st.text_input("Buscar", placeholder="Escriba algo...", label_visibility="collapsed")

st.markdown("<br>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown('<span class="titulos-negros">Filtrar por Hecho</span>', unsafe_allow_html=True)
    f_hecho = st.selectbox("H", ["Todos"] + (sorted(list(df['Hecho'].unique())) if 'Hecho' in df.columns else []), key="h", label_visibility="collapsed")
with col2:
    st.markdown('<span class="titulos-negros">Filtrar por Realizado</span>', unsafe_allow_html=True)
    f_realizado = st.selectbox("R", ["Todos"] + (sorted(list(df['Realizado'].unique())) if 'Realizado' in df.columns else []), key="r", label_visibility="collapsed")
with c3 if 'c3' in locals() else col3:
    st.markdown('<span class="titulos-negros">Filtrar por Lo Tiene</span>', unsafe_allow_html=True)
    f_lo_tiene = st.selectbox("L", ["Todos"] + (sorted(list(df['Lo Tiene'].unique())) if 'Lo Tiene' in df.columns else []), key="l", label_visibility="collapsed")

# Tabla
st.markdown('<p style="color: black !important; font-weight: bold;">Resultados:</p>', unsafe_allow_html=True)
st.dataframe(df, use_container_width=True, hide_index=True)
