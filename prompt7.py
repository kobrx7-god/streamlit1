import streamlit as st
from openai import OpenAI
import newconfig

api = newconfig.api
client = OpenAI(api_key = api, base_url = "https://api.groq.com/openai/v1")
model = 'openai/gpt-oss-20b'

def gen(prompt):
    try:
        response = client.chat.completions.create(
            model =  model,
            messages = [
                {
                    "role" : "user",
                    "content" : prompt
                }
            ],
            temperature = 0.3,
            max_tokens = 1024
        )
        return response.choices[0].message.content
    except Exception as e:
        return "Error"+str(e)

st.set_page_config(page_title = "AI Learning Assistant", layout="centered")
st.title("AI Learning Assistant")
st.write("Ask me anything...")
if "history" not in st.session_state:
    st.session_state.history = []
question = st.text_input("Enter your query : ")
if st.button("Send"):
    if question.strip():
        with st.spinner("Triangulating"):
            answer = gen(question)
        st.session_state.history.insert(
            0,
            {'question' : question,
             'answer' : answer
             }
            )
    else:
        st.warning("Please Enter a Query")

if st.session_state.history:
    st.markdown("### Conversation History")
    for i, chat in enumerate(st.session_state.history, 1):
        st.markdown(f"q{i}:{chat['question']}")
        st.write(chat['answer'])
        st.divider()

if st.button("Clear"):
    st.session_state.history=[] 
    st.rerun()

