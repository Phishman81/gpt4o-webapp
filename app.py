import streamlit as st
from openai import OpenAI
import os

# Initialisiere den OpenAI-Client mit dem API-Schlüssel aus den Umgebungsvariablen
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Stelle sicher, dass der Chatverlauf in der Session gespeichert wird
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.title("Chat mit GPT-4o – Websuche & Reasoning")

def get_gpt4o_response(user_message):
    """
    Ruft die neue Responses API von OpenAI auf, um eine Antwort zu erhalten,
    die Websuche und Reasoning integriert.
    """
    try:
        # Hier wird der API-Aufruf gemäß der Dokumentation durchgeführt.
        response = client.responses.create(
            model="gpt-4o",
            # Übergibt den aktuellen Nutzer-Input als einzelne Nachricht in einer Liste.
            input=[user_message],
            text={
                "format": {
                    "type": "text"
                }
            },
            reasoning={},
            tools=[
                {
                    "type": "web_search_preview",
                    "user_location": {
                        "type": "approximate",
                        "country": "DE"
                    },
                    "search_context_size": "medium"
                }
            ],
            temperature=1,
            max_output_tokens=2048,
            top_p=1,
            store=True
        )
        # Extrahiere das Ergebnis aus dem Antwortobjekt.
        # Hier wird angenommen, dass die Antwort unter response["text"]["result"] geliefert wird.
        answer = response.get("text", {}).get("result")
        if not answer:
            answer = str(response)
        return answer
    except Exception as e:
        return f"Fehler beim Abrufen der Antwort: {e}"

# Erstelle ein Formular für die Eingabe
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_input("Schreibe deine Nachricht:")
    submit = st.form_submit_button("Senden")
    if submit and user_input:
        st.session_state.chat_history.append({"role": "user", "message": user_input})
        assistant_reply = get_gpt4o_response(user_input)
        st.session_state.chat_history.append({"role": "assistant", "message": assistant_reply})
    

# Zeige den bisherigen Chatverlauf an
for chat in st.session_state.chat_history:
    if chat["role"] == "user":
        st.markdown(f"**User:** {chat['message']}")
    else:
        st.markdown(f"**Assistant:** {chat['message']}")
