import streamlit as st
from openai import OpenAI
import os

# Setze API-Schlüssel (wird in secrets.toml oder Umgebungsvariable erwartet)
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    st.error("⚠️ OpenAI API-Schlüssel fehlt! Setze ihn in den GitHub Actions Secrets oder secrets.toml.")

# OpenAI-Client initialisieren
client = OpenAI(api_key=api_key)

# Streamlit Seitenkonfiguration
st.set_page_config(page_title="KI-Chatbot mit Websuche", page_icon="🔎")

st.title("🤖 Chatbot mit OpenAI Websuche")

# Chatverlauf initialisieren
if "messages" not in st.session_state:
    st.session_state.messages = []

# Vorherige Nachrichten anzeigen
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Benutzereingabe
if user_input := st.chat_input("Frage mich etwas..."):
    # Nutzer-Eingabe speichern und anzeigen
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # KI-Antwort abrufen
    with st.spinner("KI denkt nach..."):
        try:
            response = client.responses.create(
                model="gpt-4o",
                tools=[{"type": "web_search_preview"}],  # OpenAI Websuche aktivieren
                input=st.session_state.messages
            )
            assistant_reply = response.output_text
        except Exception as e:
            assistant_reply = f"❌ Fehler: {e}"

    # Antwort speichern & anzeigen
    st.session_state.messages.append({"role": "assistant", "content": assistant_reply})
    with st.chat_message("assistant"):
        st.markdown(assistant_reply)
