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

# 3. CSS: BUSCADOR NEGRO Y FILTROS BLANCO PURO
st.markdown("""
    <style>
    .stApp { background-color: white !important; }
    label { font-size: 18px !important; font-weight: bold !important; color: black !important; }
    
    /* BUSCADOR NEGRO */
    [data-testid="stTextInput"] > div { 
        background-color: #000000 !important; 
        border-radius: 8px !important; 
        border: 2px solid black !important; 
    }
    [data-testid="stTextInput"] input { 
        color: white !important; 
        -webkit-text-fill-color: white !important; 
    }

    /* FILTROS BLANCO PURO */
    [data-testid="stSelectbox"] > div { 
        background-color: white !important; 
        border: 2px solid black !important; 
        border-radius: 8px !important; 
    }
    
    /* Forzar fondo blanco dentro del selector cuando está cerrado y abierto */
    div[data-baseweb="select"] > div {
        background-color: white !important;
    }
    
    /* Texto de los filtros en negro */
    [data-testid="stSelectbox"] div[data-baseweb="select"] span { 
        color: black !important; 
    }

    /* Botón Limpiar */
    div.stButton > button { 
        background-color: #f0f2f6; 
        color: black; 
        border: 1px solid black; 
        font-weight: bold; 
    }
    div.stButton > button:hover { 
        background-color: #ff4b4b; 
        color: white; 
        border: 1px solid #ff4b4b; 
    }

    /* Ocultar instrucciones de Streamlit */
    [data-testid="InputInstructions"] { display: none !important; }
    </style>
""", unsafe_allow_html=True)

# 4. CARGA DE DATOS (Enlace corregido a CSV)
@st.cache_data(ttl=5)
def load_data():
    # Corregido: de output=ods a output=csv
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRXI7sk1CdNqrMCi3lapZjt8DMoRwjVsiSknQwjgvBjVJHbusZ4GWjDYTJzTl40wictijbYo8ESq7gI/pub?output=csv" 
    try:
        data = pd.read_csv(url)
        data.columns = data.columns.str.strip()
        return data
    except Exception as e:
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
    st.button("Limpiar Campos", on_click=clear_fields)

st.markdown("<br>", unsafe_allow_html=True)

# FILTROS
col1, col2, col3 = st.columns(3)

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

# 7. PROCESAMIENTO
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
