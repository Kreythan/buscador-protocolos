import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="Búsqueda Protocolos", layout="wide")

# 2. CHAT FLOTANTE (Configurado a la IZQUIERDA)
def chat_flotante():
    components.html("""
        <script type="text/javascript">
        var Tawk_API=Tawk_API||{}, Tawk_LoadStart=new Date();
        
        // Mover a la izquierda
        Tawk_API.customStyle = {
            visibility : {
                desktop : { xOffset : 20, yOffset : 20 },
                mobile : { xOffset : 10, yOffset : 10 }
            },
            placement : 'bottom-left'
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
    """, height=100)

chat_flotante()

# 3. CSS PARA BLOQUEAR EL MODO OSCURO DEL NAVEGADOR
st.markdown("""
    <style>
    /* Bloqueo total de inversión de colores */
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #FFFFFF !important;
        filter: none !important;
        color-scheme: light !important;
    }
    /* Forzar que todos los textos sean negros */
    * { color: #000000 !important; }
    
    /* Estilo para los cuadros de búsqueda y filtros */
    input, div[data-baseweb="select"] {
        border: 2px solid #000000 !important;
        background-color: #FFFFFF !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 4. CARGA DE DATOS
@st.cache_data(ttl=30)
def load_data():
    # REEMPLAZA ESTE LINK CON TU CSV DE GOOGLE SHEETS
    url = "TU_LINK_DE_GOOGLE_SHEETS_AQUI" 
    try:
        return pd.read_csv(url)
    except:
        # Fila de prueba con HTML forzado para ver si el negro funciona
        return pd.DataFrame({'N°': ['1'], 'Hecho': ['Dato de Prueba'], 'Realizado': ['SI'], 'Lo Tiene': ['SI'], 'Protocolo': ['A']})

df = load_data()

# --- INTERFAZ CON HTML FORZADO (NEGRO) ---

st.markdown('<h1 style="color: black !important; font-family: sans-serif;">Sistema de Búsqueda y Filtros</h1>', unsafe_allow_html=True)

st.markdown('<b style="color: black !important;">Buscador General</b>', unsafe_allow_html=True)
search_query = st.text_input("Buscador", placeholder="Escriba aquí...", label_visibility="collapsed")

st.markdown("<br>", unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)
with c1:
    st.markdown('<b style="color: black !important;">Filtrar por Hecho</b>', unsafe_allow_html=True)
    f_hecho = st.selectbox("H", ["Todos"] + sorted(list(df['Hecho'].unique())), key="h", label_visibility="collapsed")
with c2:
    st.markdown('<b style="color: black !important;">Filtrar por Realizado</b>', unsafe_allow_html=True)
    f_realizado = st.selectbox("R", ["Todos"] + sorted(list(df['Realizado'].unique())), key="r", label_visibility="collapsed")
with c3:
    st.markdown('<b style="color: black !important;">Filtrar por Lo Tiene</b>', unsafe_allow_html=True)
    f_lo_tiene = st.selectbox("L", ["Todos"] + sorted(list(df['Lo Tiene'].unique())), key="l", label_visibility="collapsed")

st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<b style="color: black !important;">Filtrar por Protocolo</b>', unsafe_allow_html=True)
f_protocolo = st.selectbox("P", ["Todos"] + sorted(list(df['Protocolo'].unique())), key="p", label_visibility="collapsed")

# Filtrado
filtered_df = df.copy()
if search_query:
    mask = df.apply(lambda row: row.astype(str).str.contains(search_query, case=False).any(), axis=1)
    filtered_df = filtered_df[mask]

# Tabla final
st.markdown(f'<p style="color: black !important; font-weight: bold;">Registros encontrados: {len(filtered_df)}</p>', unsafe_allow_html=True)
st.dataframe(filtered_df, use_container_width=True, hide_index=True)
