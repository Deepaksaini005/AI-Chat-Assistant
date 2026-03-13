import streamlit as st
from groq import Groq
import os
import json
import uuid
from dotenv import load_dotenv
from tavily import TavilyClient

# -------------------
# PAGE CONFIG
# -------------------

st.set_page_config(layout="wide")

# -------------------
# LOAD ENV
# -------------------

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
client = TavilyClient("tvly-dev-*************************************************")
response = client.search(
    query="",
    search_depth="advanced",
    max_results=6,
    start_date="2026-03-13",
    end_date="2027-01-13",
    include_images=True,
    include_image_descriptions=True,
    include_favicon=True,
    include_usage=True
)
print(response)

st.markdown("""
<style>
h1 {color:#00FFFF;}
h2 {color:#00BFFF;}
strong {color:#FFD700;}
</style>
""", unsafe_allow_html=True)

# -------------------
# CREATE JSON FILE IF NOT EXISTS
# -------------------

if not os.path.exists("chat_history.json"):
    with open("chat_history.json","w") as f:
        json.dump([], f)

# -------------------
# SYSTEM PROMPT (UNCHANGED)
# -------------------

system_prompt = """
You are an advanced AI assistant designed to provide accurate, helpful, and well-structured responses.

Your goal is to deliver answers that are clear, concise, and easy to understand while maintaining a natural conversational tone.

------------------------------------------------
CONVERSATION MODE
------------------------------------------------

If the user sends a casual message such as:

hello
hi
kese ho
thanks
ok
good morning

Respond naturally and briefly like a human conversation.

Example:

User: kese ho
Assistant: Main theek hoon 😊 Aap batao kaise ho?

Do NOT generate long explanations or structured sections for simple conversation.

------------------------------------------------
SMART RESPONSE CONTROL
------------------------------------------------

Adjust response length depending on the question.

Short Question → Short answer  
Concept Explanation → Medium explanation  
Technical / Study Topic → Detailed structured explanation

Avoid unnecessary long answers.

------------------------------------------------
STRUCTURED RESPONSE MODE
------------------------------------------------

When the user asks for explanations, learning topics, or technical questions, use this structure:

## 🔹 Main Topic
Provide a clear and simple explanation.

### 📌 Key Points
- Important concept
- Important concept
- Important concept

### 💡 Example
Provide a simple real-world or practical example.

### ⚡ Extra Insight
Add helpful information, tips, or practical applications.

### ✅ Summary
Give a short conclusion in 1–2 sentences.

------------------------------------------------
HIGH QUALITY EXPLANATION RULES
------------------------------------------------

Ensure explanations are:

Clear → Easy to understand  
Concise → No unnecessary repetition  
Informative → Each section adds useful information  
Practical → Include examples when helpful  

Avoid:
- repeating the same idea multiple times
- overly complex sentences
- long paragraphs

------------------------------------------------
FORMATTING RULES
------------------------------------------------

Use:

- **bold text** for important concepts
- headings for structure
- bullet points for readability

Avoid overly large blocks of text.

------------------------------------------------
PROBLEM SOLVING MODE
------------------------------------------------

For logical or analytical problems:

1. Understand the problem
2. Break it into steps
3. Explain reasoning
4. Provide the final answer clearly

------------------------------------------------
PROGRAMMING MODE
------------------------------------------------

If the user asks coding questions:

- Provide clean and working code
- Format code properly
- Add brief comments explaining key logic
- Suggest improvements if useful

------------------------------------------------
COMPARISON MODE
------------------------------------------------

If comparing multiple things, use tables when helpful.

Example:

| Feature | Option A | Option B |
|--------|--------|--------|
| Feature | Info | Info |
| Feature | Info | Info |

------------------------------------------------
TONE AND BEHAVIOR
------------------------------------------------

Always be:

Friendly  
Professional  
Clear  
Helpful  

Focus on clarity, usefulness, and natural conversation.
"""
# -------------------
# SESSION
# -------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

# -------------------
# SAVE CHAT FUNCTION
# -------------------

def save_chat(messages):

    chat_id = str(uuid.uuid4())

    chat_data = {
        "id": chat_id,
        "messages": messages
    }

    try:
        with open("chat_history.json","r") as f:
            data = json.load(f)
    except:
        data = []

    data.append(chat_data)

    with open("chat_history.json","w") as f:
        json.dump(data,f)

# -------------------
# SIDEBAR
# -------------------

with st.sidebar:

    st.title("💬 AI Chat")

    if st.button("➕ New Chat"):

        if len(st.session_state.messages) > 0:
            save_chat(st.session_state.messages)

        st.session_state.messages = []

    st.divider()

    st.subheader("Previous Chats")

    try:
        with open("chat_history.json","r") as f:
            chats = json.load(f)
    except:
        chats = []

    for i, chat in enumerate(chats[::-1]):

     title = chat["messages"][0]["content"][:30] if chat["messages"] else "Chat"

    if st.button(title, key=f"chat_{i}"):

        st.session_state.messages = chat["messages"]

# -------------------
# TITLE
# -------------------

if len(st.session_state.messages) == 0:

    st.markdown(
        "<h1 style='text-align:center;'>WELCOME – WHAT IS IN YOUR MIND</h1>",
        unsafe_allow_html=True
    )

# -------------------
# SHOW CHAT
# -------------------

for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):
        st.markdown(msg["content"], unsafe_allow_html=True)

# -------------------
# AI FUNCTION
# -------------------
def ask_ai(messages):

    try:

        prompt = [{"role": "system", "content": system_prompt}] + messages

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=prompt[-15:],
            temperature=0.7,
            max_tokens=1024
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"Error: {str(e)}"
# -------------------
# CHAT INPUT
# -------------------

user_input = st.chat_input("Ask anything")

# -------------------
# CHAT LOGIC
# -------------------

if user_input:

    st.session_state.messages.append(
        {"role":"user","content":user_input}
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):

        with st.spinner("AI is thinking..."):

            answer = ask_ai(st.session_state.messages)

        st.markdown(answer, unsafe_allow_html=True)
        st.divider()

    st.session_state.messages.append(
        {"role":"assistant","content":answer}
    )