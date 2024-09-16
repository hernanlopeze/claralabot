import streamlit as st
from PIL import Image
import time
import streamlit.components.v1 as components
import base64

st.set_page_config(layout="wide",page_title="Clara Labot", page_icon=":dart:​")



# Configuración de la página para establecer un fondo morado oscuro y texto blanco
st.markdown(
    """
    <style>
    .stApp {
        background-color: #3e1873; /* Fondo morado oscuro */
        color: #FFFFFF; /* Texto blanco */
    }
    .custom-title {
        font-family: 'Futura', sans-serif;
        font-size: 42px;
        font-weight: 900;
        color: #FFFFFF !important; /* Texto blanco */
        text-align: center;
        margin-bottom: 0px;
    }
    .custom-subtitle {
        font-family: 'Century Gothic', sans-serif;
        font-size: 24px;
        font-weight: 700;
        color: #FFFFFF !important; /* Texto blanco */
        text-align: center;
        margin-bottom: 20px;
    }
    .qr-instruction {
        font-family: 'Century Gothic', sans-serif;
        font-size: 18px;
        font-weight: 700;
        color: #FFFFFF !important; /* Texto blanco */
        text-align: center;
        margin-bottom: 10px;
    }
    .banner {
        width: 100%;
        text-align: center;
        margin-bottom: 20px;
    }
    label {
        color: #FFFFFF !important; /* Texto blanco para las etiquetas */
    }
    .stTextInput > label {
        color: #FFFFFF !important; /* Texto blanco para el texto del input */
    }
    .stButton button {
        background-color: #FFFFFF !important; /* Fondo blanco para los botones */
        color: #3e1873 !important; /* Texto morado oscuro para los botones */
    }
    .stSelectbox > label {
        color: #FFFFFF !important; /* Texto blanco para la selección de idioma */
    }
    </style>
    """,
    unsafe_allow_html=True
)



# Definir los estados de la conversación y los videos asociados
def display_initial_options():
    #st.write("Bot: Hola Jorge que bueno que hablemos de nuevo, ¿en qué te puedo ayudar hoy?")
    st.session_state.video = "initial.mp4" 
    
    
    if st.button("Quiero conocer mi deuda con AFIP"):
        st.session_state.step = 'show_tax_options'
        st.session_state.video = "intro_afip.webp"
    if st.button("Quiero generar un VEP"):
        st.session_state.step = 'show_tax_options'
        st.session_state.video = "generate_vep_intro.mp4"

def display_tax_options():
    #st.write("Bot: No hay problema, ¿qué impuesto necesitas pagar?")
    if st.button("IVA"):
        st.session_state.step = 'show_iva_payment_options'
        st.session_state.video = "iva_intro.mp4"
    if st.button("Impuesto a las Ganancias"):
        st.session_state.step = 'show_iva_payment_options'
        st.session_state.video = "ganancias_intro.webp"
    if st.button("Bienes personales"):
        st.session_state.step = 'show_iva_payment_options'
        st.session_state.video = "bienes_intro.webp"

def display_iva_payment_options():
    #st.write("Bot: Veo que el único período impago es julio 2024, indícame en qué plazo podrías pagar:")
    if st.button("Hoy"):
        st.session_state.step = 'generate_vep'
        st.session_state.video = "pagar_hoy.mp4"
    if st.button("5 días"):
        st.session_state.step = 'generate_vep'
        st.session_state.video = "pagar_5dias.webp"
    if st.button("10 días"):
        st.session_state.step = 'generate_vep'
        st.session_state.video = "pagar_10dias.webp"

def generate_vep():
    #st.write("Bot: Por favor aguarda mientras se genera...")
    #st.session_state.video = "generando_vep.webp"
    # Simulación de espera
    time.sleep(2)  # Simula el tiempo de procesamiento
    st.write("Listo! Aquí está tu VEP:")
    pdf_file = "Vep.pdf"

    # Ofrece el PDF para la descarga
    with open(pdf_file, "rb") as f:
        st.download_button(
            label="Descargar PDF",
            data=f,
            file_name=pdf_file,
            mime="application/pdf"
        )
# Inicializar el estado de la sesión
if 'step' not in st.session_state:
    st.session_state.step = 'initial'
    st.session_state.video = None

# Layout de dos columnas
col1, col2 = st.columns(2)


# Columna 2: Video o imagen (en este caso se muestra el video o el VEP)
with col1:
    if st.session_state.step == 'initial':
        st.session_state.video = "initial.mp4"        
    
    if st.session_state.video:
        video_file = st.session_state.video

        with open(video_file, 'rb') as f:
            video_bytes = f.read()

        video_base64 = base64.b64encode(video_bytes).decode('utf-8')
        video_data_url = f"data:video/mp4;base64,{video_base64}"

        # Ajuste para que el video tenga un tamaño de 800x800 píxeles
        video_html = f'''
        <center><button id="playButton" onclick="playVideo()">Comenzar/Escuchar de nuevo</button></center>
        <div style="display: flex; justify-content: center;">
            <video id="myVideo" width="800" height="800" style="object-fit: cover;">
                <source src="{video_data_url}" type="video/mp4">
                Tu navegador no soporta el elemento de video.
            </video>
        </div>
        <script>
        function playVideo() {{
            var video = document.getElementById('myVideo');
            video.play();
        }}
        document.getElementById('playButton').click();
        </script>
        '''
        components.html(video_html, height=850)    
# Columna 1: Opciones del Bot
with col2:
    st.image("logo.png")
    if st.session_state.step == 'initial':
        display_initial_options()
    elif st.session_state.step == 'show_tax_options':
        display_tax_options()
    elif st.session_state.step == 'show_iva_payment_options':
        display_iva_payment_options()
        
    if st.session_state.step == 'generate_vep':
        st.markdown("""
            <style>
            .stDownloadButton > button {
                background-color: #3e1873;
                color: white;
                border: 2px solid white;
                border-radius: 5px;
            }
            </style>
            """, unsafe_allow_html=True)

        time.sleep(15)
        generate_vep()
        if st.button("Comencemos de nuevo"):
            display_initial_options()
    


    
