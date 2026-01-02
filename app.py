# 3. CSS: LIMPIEZA TOTAL Y BUSCADOR BLANCO PURO
st.markdown("""
    <style>
    /* Fondo general de la app */
    .stApp { background-color: white !important; }
    
    label { font-size: 20px !important; font-weight: bold !important; color: black !important; }

    /* CUADROS PRINCIPALES: Fondo blanco y borde negro */
    [data-testid="stTextInput"] > div, 
    [data-testid="stSelectbox"] > div {
        background-color: white !important;
        border: 2px solid #000000 !important;
        border-radius: 8px !important;
        box-shadow: none !important;
    }

    /* ELIMINAR EL COLOR PLOMO INTERNO DEL BUSCADOR AL ESCRIBIR */
    [data-testid="stTextInput"] input {
        background-color: white !important;
        color: black !important;
        border: none !important;
        box-shadow: none !important;
    }

    /* ELIMINAR EL COLOR PLOMO EN LOS FILTROS (SELECTORES) */
    div[data-baseweb="select"] > div {
        background-color: white !important;
    }

    /* HACER QUE EL SELECTOR SEA SOLO LISTA (Ocultar cursor de escritura) */
    div[data-baseweb="select"] input {
        caret-color: transparent !important;
        cursor: pointer !important;
    }

    /* TEXTO NEGRO EN TODO */
    input, div[data-baseweb="select"] span {
        color: black !important;
        font-size: 18px !important;
    }

    /* QUITAR BORDES INTERNOS Y SOMBRAS DE ENFOQUE */
    [data-testid="stTextInput"] > div > div, 
    [data-testid="stSelectbox"] > div > div,
    [data-testid="stTextInput"] > div:focus-within {
        border: none !important;
        box-shadow: none !important;
        outline: none !important;
        background-color: white !important;
    }
    </style>
""", unsafe_allow_html=True)
