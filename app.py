import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

# 1. CONFIGURACIÓN
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

# 3. CSS MEJORADO (Buscador Negro, Filtros Finos y Pestañas)
st.markdown("""
    <style>
    .stApp { background-color: white !important; }
    label { font-size: 16px !important; font-weight: bold !important; color: black !important; }
    
    /* BUSCADOR NEGRO */
    [data-testid="stTextInput"] > div { 
        background-color: #000000 !important; 
        border-radius: 8px !important; 
        border: 1px solid #333333 !important; 
    }
    [data-testid="stTextInput"] input { 
        color: white !important; 
        -webkit-text-fill-color: white !important; 
    }

    /* FILTROS BLANCOS FINOS */
    [data-testid="stSelectbox"] > div { 
        background-color: white !important; 
        border: 1px solid #cccccc !important; 
        border-radius: 6px !important; 
    }
    
    div[data-baseweb="select"] span, div[data-baseweb="select"] div {
        color: black !important;
        -webkit-text-fill-color: black !important;
    }

    /* ESTILO DE LAS PESTAÑAS (TABS) */
    button[data-baseweb="tab"] {
        font-size: 18px !important;
        font-weight: bold !important;
    }

    /* Botón Limpiar */
    div.stButton > button { 
        background-color: #f8f9fa; 
        color: black; 
        border: 1px solid #cccccc; 
        border-radius: 5px;
    }
    
    [data-testid="InputInstructions"] { display: none !important; }
    </style>
""", unsafe_allow_html=True)

# 4. FUNCIÓN PARA CARGAR HOJAS ESPECÍFICAS
@st.cache_data(ttl=5)
def load_sheet_data(sheet_name):
    # Usamos el ID de tu documento pero cambiando el final para pedir una hoja por nombre
    base_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRXI7sk1CdNqrMCi3lapZjt8DMoRwjVsiSknQwjgvBjVJHbusZ4GWjDYTJzTl40wictijbYo8ESq7gI/pub?sheet="
    url = f"{base_url}{sheet_name}&output=csv"
    try:
        data = pd.read_csv(url)
        data.columns = data.columns.str.strip()
        return data
    except:
        return pd.DataFrame(columns=['Nº Documento', 'Fecha', 'Hora', 'Falta', 'Hecho por', 'Realizado por', 'Lo tiene', 'Protocolo'])

# 5. LÓGICA DE INTERFAZ
st.markdown("<h1 style='text-align: center; color: black;'>Sistema de Búsqueda y Filtros</h1>", unsafe_allow_html=True)

# Definición de pestañas según tu imagen
tab_names = ["Escrituras", "Poderes", "Recos", "Actas", "Certificaciones", "Declaraciones"]
tabs = st.tabs(tab_names)

# Procesar cada pestaña
for i, tab in enumerate(tabs):
    with tab:
        nombre_hoja = tab_names[i]
        df = load_sheet_data(nombre_hoja)
        
        # --- BUSCADOR Y BOTÓN (Únicos por pestaña) ---
        search_query = st.text_input("Buscador General", placeholder=f"Buscar en {nombre_hoja}...", key=f"search_{nombre_hoja}")
        
        if st.button("Limpiar Filtros", key=f"btn_{nombre_hoja}"):
            st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)

        # --- FILTROS ---
        col1, col2, col3 = st.columns(3)
        
        def get_options(column_name, dataframe):
            if column_name in dataframe.columns:
                return ["Todos"] + sorted(list(dataframe[column_name].dropna().unique()))
            return ["Todos"]

        with col1:
            f_hecho = st.selectbox("Filtrar por Hecho", get_options('Hecho por', df), key=f"f1_{nombre_hoja}")
        with col2:
            f_realizado = st.selectbox("Filtrar por Realizado", get_options('Realizado por', df), key=f"f2_{nombre_hoja}")
        with col3:
            f_lo_tiene = st.selectbox("Filtrar por Lo Tiene", get_options('Lo tiene', df), key=f"f3_{nombre_hoja}")

        # --- FILTRADO ---
        df_final = df.copy()
        if search_query:
            df_final = df_final[df_final.apply(lambda row: row.astype(str).str.contains(search_query, case=False).any(), axis=1)]
        if f_hecho != "Todos":
            df_final = df_final[df_final['Hecho por'] == f_hecho]
        if f_realizado != "Todos":
            df_final = df_final[df_final['Realizado por'] == f_realizado]
        if f_lo_tiene != "Todos":
            df_final = df_final[df_final['Lo tiene'] == f_lo_tiene]

        st.markdown(f"**Mostrando {len(df_final)} registros**")
        st.dataframe(df_final, use_container_width=True, hide_index=True)
