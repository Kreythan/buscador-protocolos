import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

# 1. CONFIGURACIÓN
st.set_page_config(page_title="Sistema de Protocolos", layout="wide")

# 2. ESTADO DEL TEMA (MODO OSCURO O CLARO)
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

def toggle_theme():
    st.session_state.dark_mode = not st.session_state.dark_mode

# 3. CHAT TAWK.TO
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

# 4. CSS DINÁMICO SEGÚN EL MODO
bg_color = "#0e1117" if st.session_state.dark_mode else "white"
text_color = "white" if st.session_state.dark_mode else "black"
input_bg = "#262730" if st.session_state.dark_mode else "#000000" # Buscador
filter_bg = "#262730" if st.session_state.dark_mode else "white"
border_color = "#444" if st.session_state.dark_mode else "#cccccc"

st.markdown(f"""
    <style>
    .stApp {{ background-color: {bg_color} !important; }}
    
    /* PESTAÑAS */
    button[data-baseweb="tab"] p {{
        font-size: 30px !important; 
        font-weight: bold !important;
        color: {text_color} !important;
    }}

    /* TÍTULOS */
    .stWidgetLabel p, label p {{
        font-size: 24px !important;
        font-weight: bold !important;
        color: {text_color} !important;
        -webkit-text-fill-color: {text_color} !important;
    }}

    /* BUSCADOR */
    div[data-testid="stTextInput"] > div {{
        background-color: {input_bg} !important;
        border: 1px solid {border_color} !important;
    }}
    div[data-testid="stTextInput"] input {{
        color: white !important;
        font-size: 22px !important;
    }}

    /* FILTROS */
    div[data-testid="stSelectbox"] [data-baseweb="select"] {{
        background-color: {filter_bg} !important;
        border: 1px solid {border_color} !important;
    }}
    div[data-testid="stSelectbox"] span {{
        color: {text_color} !important;
        font-size: 20px !important;
    }}

    /* TABLA (Para que se vea bien en ambos modos) */
    [data-testid="stDataFrame"] {{
        background-color: {bg_color} !important;
    }}

    [data-testid="InputInstructions"] {{ display: none !important; }}
    </style>
""", unsafe_allow_html=True)

# 5. CARGA DE DATOS POR GID
@st.cache_data(ttl=5)
def load_data_by_gid(gid_number):
    doc_id = "2PACX-1vRXI7sk1CdNqrMCi3lapZjt8DMoRwjVsiSknQwjgvBjVJHbusZ4GWjDYTJzTl40wictijbYo8ESq7gI"
    url = f"https://docs.google.com/spreadsheets/d/e/{doc_id}/pub?gid={gid_number}&single=true&output=csv"
    try:
        data = pd.read_csv(url)
        data.columns = data.columns.str.strip()
        return data
    except:
        return pd.DataFrame(columns=['Nº Documento', 'Fecha', 'Hora', 'Falta', 'Hecho por', 'Realizado por', 'Lo tiene', 'Protocolo'])

def reset_tab_fields(tab_name):
    st.session_state[f"search_{tab_name}"] = ""
    st.session_state[f"f1_{tab_name}"] = "Todos"
    st.session_state[f"f2_{tab_name}"] = "Todos"
    st.session_state[f"f3_{tab_name}"] = "Todos"

# 6. INTERFAZ SUPERIOR (Botón de Tema)
col_title, col_theme = st.columns([4, 1])
with col_title:
    st.markdown(f"<h1 style='color: {text_color};'>Sistema de Búsqueda y Filtros</h1>", unsafe_allow_html=True)
with col_theme:
    label_tema = "☀️ Modo Claro" if st.session_state.dark_mode else "🌙 Modo Oscuro"
    st.button(label_tema, on_click=toggle_theme)

# 7. ESTRUCTURA DE PESTAÑAS
config_pestanas = {
    "Escrituras": "0",
    "Poderes": "1447229472",
    "Recos": "743245780",
    "Actas": "1916128539",
    "Certificaciones": "971802621",
    "Declaraciones": "1180331770"
}

nombres = list(config_pestanas.keys())
tabs = st.tabs(nombres)

for i, tab in enumerate(tabs):
    nombre_pestana = nombres[i]
    gid_actual = config_pestanas[nombre_pestana]
    
    with tab:
        df = load_data_by_gid(gid_actual)
        
        search_query = st.text_input(f"Buscar en {nombre_pestana}", placeholder="Escriba aquí...", key=f"search_{nombre_pestana}")
        st.button("🧹 Limpiar Campos", key=f"btn_{nombre_pestana}", on_click=reset_tab_fields, args=(nombre_pestana,))

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

        df_final = df.copy()
        if search_query:
            df_final = df_final[df_final.apply(lambda row: row.astype(str).str.contains(search_query, case=False).any(), axis=1)]
        if f_hecho != "Todos": df_final = df_final[df_final['Hecho por'].astype(str) == f_hecho]
        if f_realizado != "Todos": df_final = df_final[df_final['Realizado por'].astype(str) == f_realizado]
        if f_lo_tiene != "Todos": df_final = df_final[df_final['Lo tiene'].astype(str) == f_lo_tiene]

        st.markdown(f"<p style='font-size: 24px; color: {text_color};'>Registros: {len(df_final)}</p>", unsafe_allow_html=True)
        st.dataframe(df_final, use_container_width=True, hide_index=True)
