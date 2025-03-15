import streamlit as st
from openai import OpenAI
import os

# OpenAI API-Key aus Streamlit Secrets laden
api_key = st.secrets["OPENAI_API_KEY"]
client = OpenAI(api_key=api_key)

# Streamlit Seitenkonfiguration
st.set_page_config(page_title="KI-Chat mit Websuche & Bildanalyse", page_icon="🤖")

st.title("🤖 Chatbot mit Websuche & Bildverstehen")

# Chatverlauf initialisieren
if "messages" not in st.session_state:
    st.session_state.messages = []

# Vorherige Nachrichten anzeigen
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 🖼️ Bild-Upload für multimodale Analyse
uploaded_file = st.file_uploader("Lade ein Bild hoch, um es von der KI analysieren zu lassen", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    st.image(uploaded_file, caption="Hochgeladenes Bild", use_column_width=True)

    # Datei in Binary-Format umwandeln
    image_bytes = uploaded_file.getvalue()

    with st.spinner("KI analysiert das Bild..."):
        try:
            response = client.responses.create(
                model="gpt-4o",
                input=[{"type": "image", "image": image_bytes}],  # Bild an API senden
            )
            image_analysis = response.output_text  # Antwort der KI abrufen
        except Exception as e:
            image_analysis = f"❌ Fehler bei der Bildanalyse: {e}"

    # Antwort speichern & anzeigen
    st.session_state.messages.append({"role": "assistant", "content": image_analysis})
    with st.chat_message("assistant"):
        st.markdown(image_analysis)

# 📩 Chat-Eingabe für normalen Text-Chat
if user_input := st.chat_input("Frage mich etwas..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # KI antwortet auf den Text
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
