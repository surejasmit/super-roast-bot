"""
RoastBot 🔥 — A RAG-based AI chatbot that roasts you into oblivion.
Built with Streamlit + Groq + FAISS.
"""

import os
import streamlit as st
from groq import Groq
from dotenv import load_dotenv

# If rag.py exists, import safely
try:
    from rag import retrieve_context
except ImportError:
    def retrieve_context(query):
        return "No roast knowledge found. Roast creatively."

# -------------------- LOAD ENV -------------------- #

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    st.error("🚨 GROQ_API_KEY not found. Check your .env file.")
    st.stop()

client = Groq(api_key=GROQ_API_KEY)

# -------------------- SETTINGS -------------------- #

TEMPERATURE = 0.8
MAX_TOKENS = 1024
MODEL_NAME = "moonshotai/kimi-k2-instruct-0905"

SYSTEM_PROMPT = """
You are RoastBot 🔥.
Your job is to roast the user in a funny, clever way.
Be sarcastic, witty and savage.
Do NOT be hateful, racist, or truly harmful.
Keep it playful but brutal.
"""

# -------------------- MEMORY SYSTEM -------------------- #

if "memory" not in st.session_state:
    st.session_state.memory = []

if "messages" not in st.session_state:
    st.session_state.messages = []

def add_to_memory(user, bot):
    st.session_state.memory.append({
        "user": user,
        "bot": bot
    })

def clear_memory():
    st.session_state.memory = []

def format_memory(memory):
    formatted = ""
    for item in memory:
        formatted += f"User: {item['user']}\nBot: {item['bot']}\n\n"
    return formatted

# -------------------- CHAT FUNCTION -------------------- #

def chat(user_input: str) -> str:

    if not user_input.strip():
        return "You sent me nothing? Even your messages are empty like your resume. 🔥"

    # Retrieve RAG context safely
    try:
        context = retrieve_context(user_input)
    except Exception:
        context = "Roast creatively."

    history = format_memory(st.session_state.memory)

    final_prompt = (
        f"{SYSTEM_PROMPT}\n\n"
        f"Roast context:\n{context}\n\n"
        f"Recent conversation:\n{history}"
    )

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": final_prompt},
                {"role": "user", "content": user_input},
            ],
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS,
        )

        reply = response.choices[0].message.content

    except Exception as e:
        return f"Groq API Error: {str(e)}"

    add_to_memory(user_input, reply)

    return reply

# -------------------- UI -------------------- #

st.set_page_config(
    page_title="Super RoastBot",
    page_icon="🔥",
    layout="centered"
)

st.title("🔥 Super RoastBot")
st.caption("I roast harder than your code roasts your CPU")

# Sidebar
with st.sidebar:
    st.header("⚙️ Controls")

    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        clear_memory()
        st.rerun()

    st.divider()
    st.markdown(
        "**How it works:**\n"
        "1️⃣ Your message goes through RAG retrieval\n"
        "2️⃣ Roast knowledge is fetched\n"
        "3️⃣ Groq crafts a personalized roast\n"
        "4️⃣ Emotional damage delivered 🔥"
    )

# Display previous messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar="😈" if msg["role"] == "assistant" else "🤡"):
        st.markdown(msg["content"])

# Chat input
if user_input := st.chat_input("Say something... if you dare 🔥"):

    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user", avatar="🤡"):
        st.markdown(user_input)

    with st.chat_message("assistant", avatar="😈"):
        with st.spinner("Cooking up a roast... 🍳"):
            reply = chat(user_input)
            st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})