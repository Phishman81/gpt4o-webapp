import streamlit as st
import openai
import os

# Setze deinen OpenAI API-Schlüssel (wird später als Secret gesetzt)
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialisiere den Chat-Verlauf in der Session
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.title("Chat mit GPT-4o und Websuche")

def get_gpt4o_response(user_message):
    """
    Ruft die Responses API von OpenAI auf, um eine Antwort unter Einbeziehung der Websuche zu erhalten.
    """
    try:
        response = openai.Responses.create(
            model="gpt-4o",
            tools=[{"type": "web_search_preview"}],
            input=user_message
        )
        return response.get("output_text", "Keine Antwort erhalten.")
    except Exception as e:
        return f"Fehler beim Abrufen der Antwort: {e}"

# Anzeige des bisherigen Chatverlaufs
for entry in st.session_state.chat_history:
    if entry["role"] == "user":
        st.markdown(f"**User:** {entry['message']}")
    else:
        st.markdown(f"**Assistant:** {entry['message']}")

# Eingabefeld für neue Nachrichten
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("Schreibe deine Nachricht:")
    submit_button = st.form_submit_button(label="Senden")

if submit_button and user_input:
    st.session_state.chat_history.append({"role": "user", "message": user_input})
    assistant_reply = get_gpt4o_response(user_input)
    st.session_state.chat_history.append({"role": "assistant", "message": assistant_reply})
    st.experimental_rerun()
