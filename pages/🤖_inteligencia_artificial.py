import streamlit as st
from google import genai

# Configuración de la página
st.set_page_config(page_title="Chat Básico con Gemini", layout="centered")
st.title("💬 Chat con Gemini")
st.markdown("Ingresa un tema o pregunta para obtener una respuesta generada por Gemini.")

# Interfaz de usuario
prompt = st.text_input("Escribe tu pregunta o tema:", placeholder="¿Qué quieres consultar?")
enviar = st.button("Generar Respuesta")

# Función que usa el código original
def generar_respuesta(prompt):
    if not prompt:
        return "Por favor, ingresa un tema o pregunta."
    try:
        client = genai.Client(api_key="AIzaSyCqKCqmtAmKVObzXcGrCamxE_ORJ788PMs")  # Código original
        response = client.models.generate_content(
            model="gemini-2.0-flash", contents=prompt  # Código original con prompt dinámico
        )
        return response.text  # Código original
    except Exception as e:
        return f"Error: {str(e)}"

# Lógica principal
if enviar and prompt:
    with st.spinner("Generando respuesta..."):
        respuesta = generar_respuesta(prompt)
        st.subheader("Respuesta:")
        st.markdown(respuesta)
else:
    st.info("Haz clic en Generar Respuesta para hacer tu consulta.")