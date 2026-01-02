import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="Sistema de Protocolos", layout="wide")

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

# 3. CSS: PESTAÑAS NEGRAS, LETRA GRANDE Y FILTROS FINOS
# 3. CSS: SUPER-FORZADO DE TAMAÑOS
# 3. CSS: CORRECCIÓN DE COLORES Y TAMAÑOS GRANDES
st.markdown("""
    <style>
    /* 1. APP FONDO BLANCO */
    .stApp { background-color: white !important; }

    /* 2. PESTAÑAS (TABS) - MUY GRANDES Y NEGRAS */
    button[data-baseweb="tab"] p {
        font-size: 35px !important; 
        font-weight: bold !important;
        color: black !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        border-bottom-color: black !important;
    }
    
    /* 3. TÍTULOS (LABELS) - SIEMPRE NEGROS Y GRANDES */
    .stWidgetLabel p {
        font-size: 28px !important;
        font-weight: bold !important;
        color: black !important;
    }

    /* 4. BUSCADOR - FONDO NEGRO Y LETRA BLANCA */
    [data-testid="stTextInput"] > div {
        background-color: black !important;
        border-radius: 8px !important;
    }
    [data-testid="stTextInput"] input {
        font-size: 25px !important;
        color: white !important;
        -webkit-text-fill-color: white !important;
    }

    /* 5. FILTROS (SELECTBOX) - FONDO BLANCO Y LETRA NEGRA */
    [data-testid="stSelectbox"] > div {
        background-color: white !important;
        border: 1px solid #cccccc !important;
        border-radius: 8px !important;
    }
    /* Texto dentro del filtro */
    [data-testid="stSelectbox"] div[data-baseweb="select"] {
        font-size: 22px !important;
        color: black !important;
    }
    /* Forzar que el fondo del menú desplegable sea blanco */
    div[data-baseweb="select"] > div {
        background-color: white !important;
    }
    /* Texto seleccionado en negro */
    [data-testid="stSelectbox"] span {
        color: black !important;
        -webkit-text-fill-color: black !important;
    }

    /* 6. BOTÓN LIMPIAR */
    div.stButton > button {
        font-size: 22px !important;
        padding: 10px 25px !important;
        background-color: #f8f9fa;
        color: black;
        border: 1px solid #cccccc;
    }
    div.stButton > button:hover {
        background-color: #ff4b4b;
        color: white;
    }

    /* 7. TEXTO DE REGISTROS (Línea 121) */
    .stMarkdown p {
        font-size: 24px !important;
        color: black !important;
    }

    /* Ocultar instrucciones de Streamlit */
    [data-testid="InputInstructions"] { display: none !important; }
    </style>
""", unsafe_allow_html=True)
# 4. FUNCIÓN DE CARGA POR GID (Identificador único de hoja)
@st.cache_data(ttl=5)
def load_data_by_gid(gid_number):
    doc_id = "2PACX-1vRXI7sk1CdNqrMCi3lapZjt8DMoRwjVsiSknQwjgvBjVJHbusZ4GWjDYTJzTl40wictijbYo8ESq7gI"
    # Forzamos la descarga de la hoja específica usando gid y single=true
    url = f"https://docs.google.com/spreadsheets/d/e/{doc_id}/pub?gid={gid_number}&single=true&output=csv"
    try:
        data = pd.read_csv(url)
        data.columns = data.columns.str.strip()
        return data
    except:
        # Estructura de respaldo por si falla la conexión
        return pd.DataFrame(columns=['Nº Documento', 'Fecha', 'Hora', 'Falta', 'Hecho por', 'Realizado por', 'Lo tiene', 'Protocolo'])

# 5. LÓGICA DE RESETEO
def reset_tab_fields(tab_name):
    st.session_state[f"search_{tab_name}"] = ""
    st.session_state[f"f1_{tab_name}"] = "Todos"
    st.session_state[f"f2_{tab_name}"] = "Todos"
    st.session_state[f"f3_{tab_name}"] = "Todos"

# 6. DICCIONARIO DE CONFIGURACIÓN CON TUS GIDs
config_pestanas = {
    "Escrituras": "0",
    "Poderes": "1447229472",
    "Recos": "743245780",
    "Actas": "1916128539",
    "Certificaciones": "971802621",
    "Declaraciones": "1180331770"
}

# 7. INTERFAZ
st.markdown("<h1 style='text-align: center; color: black;'>Sistema de Búsqueda y Filtros</h1>", unsafe_allow_html=True)

nombres = list(config_pestanas.keys())
tabs = st.tabs(nombres)

for i, tab in enumerate(tabs):
    nombre_pestana = nombres[i]
    gid_actual = config_pestanas[nombre_pestana]
    
    with tab:
        df = load_data_by_gid(gid_actual)
        
        # --- BUSCADOR ---
        search_query = st.text_input(f"Buscar en {nombre_pestana}", placeholder="Escriba aquí...", key=f"search_{nombre_pestana}")

        # Botón Limpiar
        st.button("Limpiar Campos", key=f"btn_{nombre_pestana}", on_click=reset_tab_fields, args=(nombre_pestana,))

        st.markdown("<br>", unsafe_allow_html=True)

        # --- FILTROS ---
        col1, col2, col3 = st.columns(3)
        
        def get_options(column_name, dataframe):
            if column_name in dataframe.columns:
                return ["Todos"] + sorted(list(dataframe[column_name].dropna().astype(str).unique()))
            return ["Todos"]

        with col1:
            f_hecho = st.selectbox("Hecho por", get_options('Hecho por', df), key=f"f1_{nombre_pestana}")
        with col2:
            f_realizado = st.selectbox("Realizado por", get_options('Realizado por', df), key=f"f2_{nombre_pestana}")
        with col3:
            f_lo_tiene = st.selectbox("Lo tiene", get_options('Lo tiene', df), key=f"f3_{nombre_pestana}")

        # --- FILTRADO DE DATOS ---
        df_final = df.copy()
        
        if search_query:
            df_final = df_final[df_final.apply(lambda row: row.astype(str).str.contains(search_query, case=False).any(), axis=1)]
        
        if f_hecho != "Todos":
            df_final = df_final[df_final['Hecho por'].astype(str) == f_hecho]
        if f_realizado != "Todos":
            df_final = df_final[df_final['Realizado por'].astype(str) == f_realizado]
        if f_lo_tiene != "Todos":
            df_final = df_final[df_final['Lo tiene'].astype(str) == f_lo_tiene]

        st.markdown(f"**Registros en {nombre_pestana}: {len(df_final)}**")
        st.dataframe(df_final, use_container_width=True, hide_index=True)
