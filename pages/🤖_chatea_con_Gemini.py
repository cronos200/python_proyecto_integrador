import streamlit as st
from google import genai

# Configuración de la página
st.set_page_config(page_title="Chat sobre Cambio Climático", layout="centered")
st.title("🌍Chat sobre Cambio Climático con Gemini")
st.markdown("Pregunta cualquier cosa sobre el cambio climático y obtén respuestas precisas.")

# Interfaz de usuario
prompt = st.text_input("Haz una pregunta sobre el cambio climático:", placeholder="¿Cómo afecta el CO₂ al calentamiento global?")
enviar = st.button("Generar Respuesta")

# Función con enfoque en cambio climático
def generar_respuesta(prompt):
    if not prompt:
        return "Por favor, ingresa una pregunta sobre el cambio climático."
    try:
        client = genai.Client(api_key="AIzaSyCqKCqmtAmKVObzXcGrCamxE_ORJ788PMs")

        # Enfoque personalizado
        contexto = (
            "Actúa como un experto en cambio climático con conocimientos actualizados. "
            "Explica con claridad científica pero de manera comprensible. "
            "Asegúrate de responder siempre dentro del contexto ambiental y climático. "
            "Puedes hablar sobre causas, efectos, soluciones, políticas, energía renovable, etc."
        )

        prompt_personalizado = f"{contexto}\n\nPregunta del usuario: {prompt}"

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt_personalizado
        )
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

# Lógica principal
if enviar and prompt:
    with st.spinner("Generando respuesta sobre cambio climático..."):
        respuesta = generar_respuesta(prompt)
        st.subheader("Respuesta:")
        st.markdown(respuesta)
else:
    st.info("Haz clic en 'Generar Respuesta' para consultar sobre cambio climático.")
