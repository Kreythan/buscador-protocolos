import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

# 1. CONFIGURACIÓN DE PÁGINA
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

# 3. CSS MAESTRO: BUSCADOR OSCURO/LETRAS BLANCAS Y FILTROS BLANCO PURO
st.markdown("""
    <style>
    /* Fondo general de la aplicación */
    .stApp { background-color: white !important; }
    
    /* Títulos de los campos */
    label { 
        font-size: 20px !important; 
        font-weight: bold !important; 
        color: black !important; 
    }

    /* --- ESTILO DEL BUSCADOR GENERAL (FONDO OSCURO) --- */
    [data-testid="stTextInput"] > div {
        background-color: #262730 !important;
        border: 2px solid #000000 !important;
        border-radius: 8px !important;
        box-shadow: none !important;
    }

    /* Letras blancas al escribir en el buscador */
    [data-testid="stTextInput"] input {
        color: white !important;
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
        caret-color: white !important;
    }

    /* Eliminar el cuadro blanco/botón a la derecha del buscador (tu círculo verde) */
    [data-testid="stTextInput"] button, [data-testid="stTextInput"] ul {
        display: none !important;
    }

    /* --- ESTILO DE LOS FILTROS (FONDO BLANCO) --- */
    [data-testid="stSelectbox"] > div {
        background-color: white !important;
        border: 2px solid #000000 !important;
        border-radius: 8px !
