import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

# Configuración visual
st.set_page_config(page_title="Búsqueda Protocolos", layout="wide")

# 1. CHAT FLOTANTE (Tawk.to)
# Nota: He puesto un código genérico. Para usar el tuyo, regístrate en tawk.to gratis.
def chat_flotante():
    components.html("""
       <!--Start of Tawk.to Script-->
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
<!--End of Tawk.to Script-->
        """, height=100)
    

chat_flotante()

# Estilos CSS mejorados
st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF; }
    .filter-label { font-weight: bold; margin-bottom: -20px; color: #333; font-size: 14px; }
    .stTextInput input { border-radius: 10px; background-color: #F1F3F4; }
    </style>
    """, unsafe_allow_html=True)

# Carga de datos
@st.cache_data(ttl=60)
def load_data():
    # REEMPLAZA CON TU LINK DE GOOGLE SHEETS (CSV)
    url = "TU_LINK_DE_GOOGLE_SHEETS_AQUI" 
    try:
        return pd.read_csv(url)
    except:
        return pd.DataFrame(columns=['N°', 'Fecha', 'Hora', 'Falta', 'Hecho', 'Realizado', 'Lo Tiene', 'Protocolo'])

df = load_data()

st.title("Sistema de Búsqueda y Filtros")

# 2. BUSCADOR CON TEXTO INTERNO
search_query = st.text_input("Buscador General", placeholder="Buscar en todos los campos...", label_visibility="collapsed")

st.markdown("<br>", unsafe_allow_html=True) # Espaciado

# 3. FILTROS CON NOMBRES CORRESPONDIENTES
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<p class="filter-label">Filtrar por Hecho</p>', unsafe_allow_html=True)
    f_hecho = st.selectbox("", ["Todos"] + sorted(list(df['Hecho'].unique())), key="hecho", label_visibility="collapsed")

with col2:
    st.markdown('<p class="filter-label">Filtrar por Realizado</p>', unsafe_allow_html=True)
    f_realizado = st.selectbox("", ["Todos"] + sorted(list(df['Realizado'].unique())), key="realizado", label_visibility="collapsed")

with col3:
    st.markdown('<p class="filter-label">Filtrar por Lo Tiene</p>', unsafe_allow_html=True)
    f_lo_tiene = st.selectbox("", ["Todos"] + sorted(list(df['Lo Tiene'].unique())), key="lotienne", label_visibility="collapsed")

st.markdown('<p class="filter-label">Filtrar por Protocolo</p>', unsafe_allow_html=True)
f_protocolo = st.selectbox("", ["Todos"] + sorted(list(df['Protocolo'].unique())), key="proto", label_visibility="collapsed")

# Lógica de Filtrado
filtered_df = df.copy()
if search_query:
    mask = df.apply(lambda row: row.astype(str).str.contains(search_query, case=False).any(), axis=1)
    filtered_df = filtered_df[mask]

if f_hecho != "Todos": filtered_df = filtered_df[filtered_df['Hecho'] == f_hecho]
if f_realizado != "Todos": filtered_df = filtered_df[filtered_df['Realizado'] == f_realizado]
if f_lo_tiene != "Todos": filtered_df = filtered_df[filtered_df['Lo Tiene'] == f_lo_tiene]
if f_protocolo != "Todos": filtered_df = filtered_df[filtered_df['Protocolo'] == f_protocolo]

# Tabla
st.markdown(f"**Mostrando {len(filtered_df)} registros**")
st.dataframe(filtered_df, use_container_width=True, hide_index=True)
