import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

# 1. CONFIGURACIÓN
st.set_page_config(page_title="Búsqueda Protocolos", layout="wide")

# 2. CHAT TAWK.TO
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

# 3. CSS (Buscador Negro / Filtros Blancos)
st.markdown("""
    <style>
    .stApp { background-color: white !important; }
    label { font-size: 18px !important; font-weight: bold !important; color: black !important; }
    [data-testid="stTextInput"] > div { background-color: #262730 !important; border-radius: 8px !important; border: 2px solid black !important; }
    [data-testid="stTextInput"] input { color: white !important; -webkit-text-fill-color: white !important; }
    [data-testid="stSelectbox"] > div { background-color: white !important; border: 2px solid black !important; border-radius: 8px !important; }
    [data-testid="stSelectbox"] div[data-baseweb="select"] span { color: black !important; }
    div.stButton > button { background-color: #f0f2f6; color: black; border: 1px solid black; font-weight: bold; }
    div.stButton > button:hover { background-color: #ff4b4b; color: white; border: 1px solid #ff4b4b; }
    </style>
""", unsafe_allow_html=True)

# 4. CARGA DE DATOS (Ajustado a tus nuevas columnas)
@st.cache_data(ttl=5) # Cache corto para ver cambios rápido
def load_data():
    # REEMPLAZA ESTA URL CON EL LINK CSV DE TU IMAGEN
    url = "TU_LINK_DE_GOOGLE_SHEETS_AQUI" 
    try:
        data = pd.read_csv(url)
        # Limpiar espacios en los nombres de las columnas por si acaso
        data.columns = data.columns.str.strip()
        return data
    except Exception as e:
        # Si falla o no hay link, muestra una tabla vacía con tus columnas
        return pd.DataFrame(columns=['Nº Documento', 'Fecha', 'Hora', 'Falta', 'Hecho por', 'Realizado por', 'Lo tiene', 'Protocolo'])

df = load_data()

# 5. LÓGICA DE LIMPIEZA
def clear_fields():
    st.session_state["search_key"] = ""
    st.session_state["f1_key"] = "Todos"
    st.session_state["f2_key"] = "Todos"
    st.session_state["f3_key"] = "Todos"

# 6. INTERFAZ
st.markdown("<h1 style='text-align: center; color: black;'>Sistema de Búsqueda</h1>", unsafe_allow_html=True)

search_query = st.text_input("Buscador General", placeholder="Escriba aquí para buscar...", key="search_key")

col_btn, _ = st.columns([1, 5])
with col_btn:
    st.button("🧹 Limpiar Campos", on_click=clear_fields)

st.markdown("<br>", unsafe_allow_html=True)

# FILTROS DINÁMICOS (Se adaptan a tus columnas)
col1, col2, col3 = st.columns(3)

# Función auxiliar para sacar listas de filtros sin errores
def get_options(column_name):
    if column_name in df.columns:
        return ["Todos"] + sorted(list(df[column_name].dropna().unique()))
    return ["Todos"]

with col1:
    f_hecho = st.selectbox("Filtrar por Hecho por", get_options('Hecho por'), key="f1_key")
with col2:
    f_realizado = st.selectbox("Filtrar por Realizado por", get_options('Realizado por'), key="f2_key")
with col3:
    f_lo_tiene = st.selectbox("Filtrar por Lo tiene", get_options('Lo tiene'), key="f3_key")

# 7. PROCESAMIENTO Y TABLA
df_final = df.copy()

if search_query:
    df_final = df_final[df_final.apply(lambda row: row.astype(str).str.contains(search_query, case=False).any(), axis=1)]
if f_hecho != "Todos":
    df_final = df_final[df_final['Hecho por'] == f_hecho]
if f_realizado != "Todos":
    df_final = df_final[df_final['Realizado por'] == f_realizado]
if f_lo_tiene != "Todos":
    df_final = df_final[df_final['Lo tiene'] == f_lo_tiene]

st.markdown(f"**Registros encontrados: {len(df_final)}**")
st.dataframe(df_final, use_container_width=True, hide_index=True)
