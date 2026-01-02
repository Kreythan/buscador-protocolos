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
        
        // ESTA PARTE MUEVE EL CHAT A LA IZQUIERDA
        Tawk_API.customStyle = {
            visibility : {
                desktop : { xOffset : 15, yOffset : 15 },
                mobile : { xOffset : 15, yOffset : 15 }
            }
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
    """, height=0)

chat_flotante()

# 3. CSS ULTRA-AGRESIVO PARA FORZAR TEXTO NEGRO
st.markdown("""
    <style>
    /* 1. Forzar fondo blanco en todo */
    [data-testid="stAppViewContainer"], .stApp, .main {
        background-color: white !important;
    }

    /* 2. Forzar NEGRO en todos los textos, títulos y párrafos */
    * {
        color: #000000 !important;
        -webkit-text-fill-color: #000000 !important;
    }

    /* 3. Estilo de los nombres de los filtros */
    .filter-label {
        color: #000000 !important;
        font-weight: bold !important;
        font-size: 16px !important;
        display: block;
        margin-bottom: 8px;
    }

    /* 4. Forzar visibilidad de inputs y selectores */
    input, div[data-baseweb="select"] {
        background-color: #f0f2f6 !important;
        border: 2px solid #000000 !important;
        border-radius: 8px !important;
    }

    /* 5. Asegurar que el texto dentro de los filtros sea negro */
    div[data-baseweb="select"] span, div[data-baseweb="select"] div {
        color: #000000 !important;
    }

    /* 6. Forzar que la tabla no sea transparente */
    [data-testid="stDataFrame"] {
        background-color: white !important;
    }
    
    /* 7. Bloquear cualquier filtro de inversión de color del
