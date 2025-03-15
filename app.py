import streamlit as st
from openai import OpenAI

# Streamlit-Seitenkonfiguration (Titel und Icon)
st.set_page_config(page_title="Chatbot mit Websuche", page_icon="🔎")

st.title("🤖 ChatGPT mit Web-Suche")

# Initialisiere den Chat-Verlauf in der Session-State
if "messages" not in st.session_state:
    st.session_state.messages = []  # Liste der Nachrichten (Dicts mit "role" und "content")

# Bisherigen Chat-Verlauf anzeigen
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Eingabefeld für neue Nutzerfrage (unten im Chat-Fenster)
if user_input := st.chat_input("Ihre Nachricht eingeben..."):
    # 1. Nutzer-Nachricht zum Verlauf hinzufügen und anzeigen
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
    # 2. API-Aufruf an OpenAI (mit Websuche-Tool) und KI-Antwort generieren
    with st.spinner("KI denkt nach..."):
        try:
            client = OpenAI()  # OpenAI-Client mit API-Key (aus Umgebungsvariable)
            response = client.responses.create(
                model="gpt-4o",
                tools=[{"type": "web_search_preview"}],  # Web-Suche als Tool aktivieren&#8203;:contentReference[oaicite:1]{index=1}
                input=st.session_state.messages         # gesamter Unterhaltungsverlauf als Eingabe
            )
            assistant_answer = response.output_text    # extrahiere generierten Antwort-Text
        except Exception as e:
            assistant_answer = "Entschuldigung, es ist ein Fehler aufgetreten. 🛑"
            print(f"OpenAI API Fehler: {e}")
    # 3. KI-Antwort zum Verlauf hinzufügen und in der UI darstellen
    st.session_state.messages.append({"role": "assistant", "content": assistant_answer})
    with st.chat_message("assistant"):
        st.markdown(assistant_answer)
