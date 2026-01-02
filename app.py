import streamlit as st
import pandas as pd

# Configuración visual
st.set_page_config(page_title="Sistema de Búsqueda y Filtros", layout="wide")

# Estilo CSS para imitar tu diseño de Figma
st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF; }
    .stTextInput input { border-radius: 10px; background-color: #F1F3F4; border: none; }
    div[data-baseweb="select"] > div { border-radius: 10px; background-color: #F1F3F4; border: none; }
    .stDataFrame { border: 1px solid #E6E8EB; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# Función para cargar datos (Simulando el link de Google Sheets)
@st.cache_data(ttl=60)
def load_data():
    # OPCIÓN A: Archivo local (debes subirlo a GitHub también)
    # return pd.read_excel("datos.xlsx")
    
    # OPCIÓN B: Google Sheets (Recomendado para actualización diaria)
    # Reemplaza 'TU_LINK_CSV' con el link de "Publicar en la Web" de Google Sheets
    url = "TU_LINK_DE_GOOGLE_SHEETS_AQUI" 
    try:
        return pd.read_csv(url)
    except:
        # Esto es solo para que no de error mientras configuras el link
        return pd.DataFrame(columns=['N°', 'Fecha', 'Hora', 'Falta', 'Hecho', 'Realizado', 'Lo Tiene', 'Protocolo'])

df = load_data()

st.title("Sistema de Búsqueda y Filtros")

# 1. Buscador Global
search_query = st.text_input("", placeholder="🔍 Buscar en todos los campos...")

# 2. Filtros (Layout de 3 columnas + 1 abajo según tu diseño)
c1, c2, c3 = st.columns(3)
with c1: f_hecho = st.selectbox("Filtrar por Hecho", ["Todos"] + list(df['Hecho'].unique()) if not df.empty else ["Todos"])
with c2: f_realizado = st.selectbox("Filtrar por Realizado", ["Todos"] + list(df['Realizado'].unique()) if not df.empty else ["Todos"])
with c3: f_lo_tiene = st.selectbox("Filtrar por Lo Tiene", ["Todos"] + list(df['Lo Tiene'].unique()) if not df.empty else ["Todos"])

f_protocolo = st.selectbox("Filtrar por Protocolo", ["Todos"] + list(df['Protocolo'].unique()) if not df.empty else ["Todos"])

# 3. Lógica de Filtrado
filtered_df = df.copy()
if search_query:
    mask = df.apply(lambda row: row.astype(str).str.contains(search_query, case=False).any(), axis=1)
    filtered_df = filtered_df[mask]

if f_hecho != "Todos": filtered_df = filtered_df[filtered_df['Hecho'] == f_hecho]
if f_realizado != "Todos": filtered_df = filtered_df[filtered_df['Realizado'] == f_realizado]
if f_lo_tiene != "Todos": filtered_df = filtered_df[filtered_df['Lo Tiene'] == f_lo_tiene]
if f_protocolo != "Todos": filtered_df = filtered_df[filtered_df['Protocolo'] == f_protocolo]

# 4. Tabla de resultados
st.markdown(f"<p style='color: gray;'>Mostrando {len(filtered_df)} de {len(df)} registros</p>", unsafe_allow_html=True)
st.dataframe(filtered_df, use_container_width=True, hide_index=True)