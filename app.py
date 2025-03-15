import base64
import streamlit as st
from openai import OpenAI

# OpenAI API-Key aus Streamlit Secrets laden
api_key = st.secrets["OPENAI_API_KEY"]
client = OpenAI(api_key=api_key)

# Streamlit Seitenkonfiguration
st.set_page_config(page_title="KI-Chat mit Websuche & Bildanalyse", page_icon="🤖")

st.title("🤖 Chatbot mit Websuche & Bildverstehen")

# **Chatverlauf initialisieren**
if "messages" not in st.session_state:
    st.session_state.messages = []

# **📩 Chat-Eingabe für normalen Text-Chat**
user_input = st.chat_input("Frage mich etwas...")

# **🖼️ Bild-Upload für multimodale Analyse**
st.subheader("📷 Bild hochladen zur Analyse")
uploaded_file = st.file_uploader("Lade ein Bild hoch:", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    # Bild anzeigen
    st.image(uploaded_file, caption="Hochgeladenes Bild", use_container_width=True)

    # Datei in Base64 umwandeln
    image_bytes = uploaded_file.getvalue()
    base64_image = base64.b64encode(image_bytes).decode("utf-8")

    # **KI-Bildanalyse ausführen**
    with st.spinner("🔍 KI analysiert das Bild..."):
        try:
            response = client.responses.create(
                model="gpt-4o",
                input=[
                    {
                        "type": "image",
                        "image": base64_image,  # Sende das Bild als Base64-String
                    }
                ],
            )
            image_analysis = response.output_text  # KI-Antwort abrufen
        except Exception as e:
            image_analysis = f"❌ Fehler bei der Bildanalyse: {e}"

    # Antwort anzeigen
    st.subheader("🧠 KI-Beschreibung des Bildes:")
    st.markdown(image_analysis)

    # **Antwort in den Chatverlauf speichern**
    st.session_state.messages.append({"role": "assistant", "content": image_analysis})

# **Bisherige Nachrichten anzeigen**
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# **KI antwortet auf den Text-Chat**
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.spinner("KI denkt nach..."):
        try:
            response = client.responses.create(
                model="gpt-4o",
                tools=[{"type": "web_search_preview"}],  # Websuche aktivieren
                input=st.session_state.messages
            )
            assistant_reply = response.output_text
        except Exception as e:
            assistant_reply = f"❌ Fehler: {e}"

    # Antwort speichern & anzeigen
    st.session_state.messages.append({"role": "assistant", "content": assistant_reply})
    with st.chat_message("assistant"):
        st.markdown(assistant_reply)
