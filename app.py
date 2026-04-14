import streamlit as st
from groq import Groq
import os
import json
import uuid
from datetime import datetime
from dotenv import load_dotenv
from tools import TOOLS_MAP, GROQ_TOOLS, should_use_web_search, web_search# -------------------
# PAGE CONFIG
# -------------------

st.set_page_config(layout="wide")

# -------------------
# LOAD ENV
# -------------------

load_dotenv()
try:
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
except Exception:
    client = None

# Optional local Hugging Face model loading
try:
    from transformers import AutoModelForCausalLM, AutoTokenizer
    import torch
except ImportError:
    pass

# -------------------
# LOAD LOCAL MODEL
# -------------------
@st.cache_resource
def load_hf_model():
    model_dir = "custom_model"
    if not os.path.exists(model_dir):
        # Fallback to base model if custom model is not fine-tuned yet
        model_dir = "microsoft/DialoGPT-small"
    
    try:
        tokenizer = AutoTokenizer.from_pretrained(model_dir)
        model = AutoModelForCausalLM.from_pretrained(model_dir)
        return tokenizer, model
    except Exception as e:
        return None, None

# client = TavilyClient("tvly-dev-*************************************************")
# response = client.search(
#     query="",
#     search_depth="advanced",
#     max_results=6,
#     start_date="2026-03-13",
#     end_date="2027-01-13",
#     include_images=True,
#     include_image_descriptions=True,
#     include_favicon=True,
#     include_usage=True
# )
# print(response)

st.markdown("""
<style>
h1 {color:#00FFFF;}
h2 {color:#00BFFF;}
strong {color:#FFD700;}

/* ── Chat message formatting ── */
[data-testid="stChatMessage"] p {
    margin-bottom: 0.6rem;
    line-height: 1.75;
}
[data-testid="stChatMessage"] ul,
[data-testid="stChatMessage"] ol {
    padding-left: 1.4rem;
    margin-top: 0.4rem;
    margin-bottom: 0.8rem;
}
[data-testid="stChatMessage"] li {
    margin-bottom: 0.55rem;
    line-height: 1.75;
}
[data-testid="stChatMessage"] li > ul,
[data-testid="stChatMessage"] li > ol {
    margin-top: 0.35rem;
}
[data-testid="stChatMessage"] h2,
[data-testid="stChatMessage"] h3,
[data-testid="stChatMessage"] h4 {
    margin-top: 1.1rem;
    margin-bottom: 0.45rem;
}
[data-testid="stChatMessage"] pre {
    margin-top: 0.6rem;
    margin-bottom: 0.8rem;
}
[data-testid="stChatMessage"] hr {
    margin: 0.9rem 0;
}
</style>
""", unsafe_allow_html=True)

# -------------------
# CREATE JSON FILE IF NOT EXISTS
# -------------------

if not os.path.exists("chat_history.json"):
    with open("chat_history.json","w") as f:
        json.dump([], f)

# -------------------
# SYSTEM PROMPT — ROLE-BASED BEHAVIOR
# -------------------

ROLE_PROMPTS = {
    "General Assistant": """
You are an advanced AI assistant. Your name is NexusAI.

CORE IDENTITY:
- You are friendly, professional, and highly knowledgeable.
- You remember the full conversation context and refer back to earlier messages when relevant.
- You adapt your tone to match the user — casual for casual, technical for technical.

CONTEXT AWARENESS:
- Always consider the FULL conversation history before responding.
- If the user refers to "it", "that", or "the thing I mentioned", look back in the conversation to resolve the reference.
- If a follow-up question is asked, connect it to the previous answer.
- Never repeat information the user already knows from earlier in the conversation.

RESPONSE LENGTH CONTROL:
- Greetings / casual → 1-2 sentences max
- Factual question → concise direct answer
- Concept / explanation → structured with headings and bullet points
- Code request → clean code with comments

FORMATTING RULES (STRICTLY ENFORCE):
- **CRITICAL RULE**: ALWAYS answer in clean, structured bullet points. NEVER write long dense paragraphs.
- Each bullet point MUST be on its own line, with a blank line separating distinct points or sections.
- Use **bold** for key terms so they stand out.
- Use `##` or `###` headings to group related points — always leave a blank line before and after a heading.
- Use numbered lists (1. 2. 3.) for steps or sequences.
- Use tables for comparisons.
- Use fenced code blocks (```python) for all code — never inline code for multi-line snippets.
- Keep each bullet concise — one idea per bullet. If an idea needs sub-details, use an indented sub-bullet (  -).
""",
    "Python Tutor": """
You are NexusAI acting as a Python programming tutor.

FORMATTING RULES (STRICTLY ENFORCE):
- Explain every concept using numbered steps or bullet points. NO paragraphs.
- Leave a blank line between each bullet or step for readability.
- Always provide a runnable code block (```python) after the explanation.
- If the student makes an error, use two bullets: one for WHY it is wrong, one for the fix.
- Use analogies as indented sub-bullets (  -) under the main bullet.
- Track what the student has learned and build upon it each turn.
""",
    "Creative Writer": """
You are NexusAI acting as a creative writing assistant.
- Help with stories, poems, scripts, and any creative content.
- Match the user's desired tone (funny, dark, romantic, etc.).
- Offer suggestions to improve their writing.
- Be expressive and use vivid language in your own responses.
""",
    "Data Scientist": """
You are NexusAI acting as a data science expert.

FORMATTING RULES (STRICTLY ENFORCE):
- ALWAYS return answers strictly in bullet points. NO dense paragraphs.
- Leave a blank line between each bullet point for visual clarity.
- Provide code in Python using pandas, numpy, sklearn, pytorch in fenced ```python blocks.
- Explain mathematical concepts with intuition first, formula second — each on its own bullet.
- When debugging, trace each step as a numbered list.
- Use `##` headings to separate major sections (e.g., ## Explanation, ## Code, ## Output).
"""
}

DEFAULT_ROLE = "General Assistant"
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

    # Role Selection
    selected_role = st.selectbox(
        "🎭 AI Role",
        list(ROLE_PROMPTS.keys()),
        help="Change the AI's persona and expertise area."
    )

    # Model Selection
    selected_engine = st.selectbox(
        "🤖 AI Engine", 
        ["Llama 3 (Groq API)", "Custom Transformer (Local)"],
        help="Switch between the external Groq API and your locally trained Transformers model."
    )

    if st.button("➕ New Chat"):

        if len(st.session_state.messages) > 0:
            save_chat(st.session_state.messages)

        st.session_state.messages = []

    st.divider()

    st.subheader("📋 Previous Chats")

    try:
        with open("chat_history.json","r") as f:
            chats = json.load(f)
    except:
        chats = []

    # Separate recent (latest 10) and older chats
    all_chats_reversed = chats[::-1]  # Most recent first
    recent_chats = all_chats_reversed[:10]  # Latest 10
    older_chats = all_chats_reversed[10:]   # Older than 10
    
    # Display Recent Chats (Latest 10)
    if recent_chats:
        st.markdown("### 📌 Recent (Latest 10)")
        for i, chat in enumerate(recent_chats):
            title = chat["messages"][0]["content"][:40] if chat["messages"] else "Empty Chat"
            if st.button(f"💬 {title}", key=f"chat_recent_{i}"):
                st.session_state.messages = chat["messages"]
                st.rerun()
    
    # Display Older Chats (Collapsible)
    if older_chats:
        st.divider()
        with st.expander(f"📦 Older Chats ({len(older_chats)} more...)", expanded=False):
            st.markdown(f"**Total older chats: {len(older_chats)}**")
            for i, chat in enumerate(older_chats):
                title = chat["messages"][0]["content"][:40] if chat["messages"] else "Empty Chat"
                if st.button(f"💬 {title}", key=f"chat_older_{i}"):
                    st.session_state.messages = chat["messages"]
                    st.rerun()
            
    st.divider()
    st.subheader("⚙️ Advanced Settings")
    temperature = st.slider("Temperature", 0.0, 1.0, 0.7, 0.1, help="Higher values make output more random, lower values make it more deterministic.")
    max_tokens = st.slider("Max Tokens", 50, 2048, 1024, 50, help="Maximum length of the generated response.")

    st.divider()
    st.subheader("📁 Upload File (Agent Context)")
    uploaded_file = st.file_uploader("Upload a PDF or Image (JPG/PNG)", type=["pdf", "png", "jpg", "jpeg"])
    
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

messages = st.session_state.messages
if len(messages) > 10:
    older_messages = messages[:-10]
    recent_messages = messages[-10:]
    
    with st.expander(f"🕰️ View older messages ({len(older_messages)})", expanded=False):
        for msg in older_messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"], unsafe_allow_html=True)
                
    for msg in recent_messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"], unsafe_allow_html=True)
else:
    for msg in messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"], unsafe_allow_html=True)

# -------------------
# GENERATE RESPONSE FUNCTION (CORE)
# -------------------
def generate_response(user_input: str, conversation_history: list, role: str = DEFAULT_ROLE, engine: str = "Llama 3 (Groq API)", temp: float = 0.7, max_t: int = 1024) -> str:
    """
    Central function that generates a response from any LLM engine.
    
    Args:
        user_input: The latest message from the user.
        conversation_history: Full list of {role, content} message dicts.
        role: The AI persona to use (key into ROLE_PROMPTS).
        engine: Which backend engine to use.
        temp: Sampling temperature.
        max_t: Maximum tokens to generate.
    
    Returns:
        The AI-generated response string.
    """
    
    # Build the system prompt with role + context injection
    system_prompt = ROLE_PROMPTS.get(role, ROLE_PROMPTS[DEFAULT_ROLE])
    
    # Inject a context summary if conversation is long (>10 messages)
    context_note = ""
    if len(conversation_history) > 10:
        # Summarize early context so the model stays aware
        early_topics = []
        for msg in conversation_history[:6]:
            if msg["role"] == "user":
                early_topics.append(msg["content"][:80])
        if early_topics:
            context_note = f"\n\n[CONTEXT REMINDER: Earlier in this conversation, the user discussed: {'; '.join(early_topics)}. Keep this in mind for continuity.]"
    
    # ✨ AUTO WEB SEARCH FOR FACTUAL QUERIES ✨
    web_context = ""
    if should_use_web_search(user_input):
        search_results = web_search(user_input)
        web_context = f"\n\n[WEB SEARCH RESULTS FOR: '{user_input}']\n{search_results}\n[END SEARCH RESULTS]\n\nUse the above real-time information to provide an accurate, current answer."
    
    # Calculate current temporal context
    current_time = datetime.now().strftime("%I:%M %p")
    current_date = datetime.now().strftime("%B %d, %Y")
    day_of_week = datetime.now().strftime("%A")
    
    temporal_context = f"\n\n[TIME CONTEXT: Today is {day_of_week}, {current_date}. Current local time is {current_time}. Your knowledge of events after late 2023 is powered by your Web Search tool. Use it for any 2024, 2025, or 2026 current affairs.]"
    
    full_system = (
        system_prompt + context_note + web_context + temporal_context +
        "\n\nTOOL INSTRUCTIONS (CRITICAL):"
        "\n1. To call a tool you MUST use the native Groq JSON tool-call schema — NEVER embed tool calls in plain text."
        "\n2. FORBIDDEN formats (will cause errors):"
        "\n   - <function=web_search{\"query\": \"...\"}>"
        "\n   - <function=web_search({\"query\": \"...\"})>"
        "\n   - Any raw XML / angle-bracket tag in your reply."
        "\n3. If you are unsure how to call a tool, just answer from your own knowledge instead."
    )
    
    # --- ENGINE: Groq API ---
    if engine == "Llama 3 (Groq API)":
        if not client:
            return "⚠️ Error: Groq client not initialized. Check your GROQ_API_KEY in `.env`."
        try:
            messages = [{"role": "system", "content": full_system}] + conversation_history
            # Keep only the last 15 messages (plus system) to respect token limits
            messages = messages[-15:]
            
            # Agentic Loop for Tool Calling
            for _ in range(5):
                try:
                    response = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=messages,
                        temperature=temp,
                        max_tokens=max_t,
                        tools=GROQ_TOOLS,
                        tool_choice="auto"
                    )
                    
                    response_message = response.choices[0].message
                    tool_calls = response_message.tool_calls
                    
                    if tool_calls:
                        messages.append(response_message)
                        for tool_call in tool_calls:
                            fn_name = tool_call.function.name
                            fn_args_str = tool_call.function.arguments
                            
                            try:
                                fn_args = json.loads(fn_args_str)
                                fn_res = TOOLS_MAP.get(fn_name)(**fn_args)
                            except Exception as e:
                                fn_res = f"Error: {str(e)}"
                                
                            messages.append({"tool_call_id": tool_call.id, "role": "tool", "name": fn_name, "content": str(fn_res)})
                        continue
                    else:
                        return response_message.content
                        
                except Exception as e:
                    import ast, re
                    error_str = str(e)

                    # ── Detect any hallucinated-tool-call error from Groq ──
                    is_tool_error = (
                        "failed_generation" in error_str or
                        "tool_use_failed" in error_str or
                        "tool call validation failed" in error_str
                    )

                    if is_tool_error:
                        dict_str = error_str.split(" - ", 1)[-1]
                        try:
                            error_dict = ast.literal_eval(dict_str)
                            failed_gen = error_dict.get('error', {}).get('failed_generation', '')

                            # ── Broadened regex: handles both formats:
                            #    <function=name(JSON)>   (old)
                            #    <function=nameJSON>      (new / no parens)
                            match = re.search(
                                r'<function=([a-zA-Z_]+)\(?({.*?})\)?>',
                                failed_gen,
                                flags=re.DOTALL
                            )
                            if match:
                                fn_name    = match.group(1)
                                fn_args_str = match.group(2)
                                try:
                                    fn_args = json.loads(fn_args_str)
                                    fn_res  = TOOLS_MAP.get(fn_name, lambda **kw: "Tool not found")(**fn_args)
                                except Exception as inner_e:
                                    fn_res = f"Error simulating tool: {str(inner_e)}"

                                dummy_id = f"call_{uuid.uuid4().hex[:8]}"
                                messages.append({
                                    "role": "assistant",
                                    "content": None,
                                    "tool_calls": [{
                                        "id": dummy_id,
                                        "type": "function",
                                        "function": {"name": fn_name, "arguments": fn_args_str}
                                    }]
                                })
                                messages.append({
                                    "tool_call_id": dummy_id,
                                    "role": "tool",
                                    "name": fn_name,
                                    "content": str(fn_res)
                                })
                                continue  # retry loop with tool result injected
                            else:
                                # No parseable tool call — strip the tag and return whatever text exists
                                cleaned_gen = re.sub(r'<function=.*', '', failed_gen, flags=re.DOTALL).strip()
                                if cleaned_gen:
                                    return f"{cleaned_gen}\n\n*(Note: Formatting error auto-recovered)*"
                                else:
                                    # Last resort: call again without tools
                                    response = client.chat.completions.create(
                                        model="llama-3.3-70b-versatile",
                                        messages=messages,
                                        temperature=temp,
                                        max_tokens=max_t
                                    )
                                    return response.choices[0].message.content
                        except Exception:
                            pass
                    return f"⚠️ Groq API Error: {error_str}"
                    
            return "⚠️ Agent exceeded maximum tool call depth (5 checks). Trying again might resolve this."
        except Exception as e:
            return f"⚠️ Groq API Critical Error: {str(e)}"
    
    # --- ENGINE: Custom Local Transformer ---
    elif engine == "Custom Transformer (Local)":
        tokenizer, model = load_hf_model()
        if not model or not tokenizer:
            return "⚠️ Custom model not found. Run `python train.py` first to train your local model."
        
        try:
            # Build conversation history for DialoGPT
            chat_history_ids = None
            for msg in conversation_history[-6:]:
                if msg["role"] == "system":
                    continue
                new_user_input_ids = tokenizer.encode(msg["content"] + tokenizer.eos_token, return_tensors='pt')
                if chat_history_ids is None:
                    chat_history_ids = new_user_input_ids
                else:
                    chat_history_ids = torch.cat([chat_history_ids, new_user_input_ids], dim=-1)
            
            output_ids = model.generate(
                chat_history_ids, 
                max_new_tokens=min(max_t, 500),
                pad_token_id=tokenizer.eos_token_id,
                no_repeat_ngram_size=3, 
                do_sample=True, 
                top_k=50, 
                top_p=0.9, 
                temperature=temp
            )
            
            response = tokenizer.decode(output_ids[:, chat_history_ids.shape[-1]:][0], skip_special_tokens=True)
            return response if response.strip() else "I'm still learning — could you rephrase that?"
        except Exception as e:
            return f"⚠️ Local Transformer Error: {str(e)}"
    
    return "⚠️ Unknown engine selected."
# -------------------
# CHAT INPUT
# -------------------

user_input = st.chat_input("Ask anything...")

# -------------------
# CHAT LOGIC
# -------------------

if user_input:
    
    # Process uploaded file if present
    file_context = ""
    if uploaded_file:
        import base64
        import PyPDF2
        file_ext = uploaded_file.name.split('.')[-1].lower()
        
        with st.spinner("Processing attached file..."):
            if file_ext == "pdf":
                try:
                    pdf_reader = PyPDF2.PdfReader(uploaded_file)
                    num_pages = min(10, len(pdf_reader.pages))
                    extracted_text = ""
                    for i in range(num_pages):
                        extracted_text += pdf_reader.pages[i].extract_text() + "\n"
                    file_context = f"\n\n[Attached Extracted PDF Content: {uploaded_file.name}]\n{extracted_text}"
                except Exception as e:
                    file_context = f"\n\n[Error reading attached PDF: {str(e)}]"
            
            elif file_ext in ["png", "jpg", "jpeg"]:
                try:
                    # Vision API helper implementation
                    encoded_image = base64.b64encode(uploaded_file.read()).decode('utf-8')
                    vision_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
                    vision_response = vision_client.chat.completions.create(
                        model="llama-3.2-11b-vision-preview",
                        messages=[{
                            "role": "user",
                            "content": [
                                {"type": "text", "text": "Extract all text and describe this image comprehensively."},
                                {"type": "image_url", "image_url": {"url": f"data:image/{file_ext};base64,{encoded_image}"}}
                            ]
                        }],
                        max_tokens=1024
                    )
                    image_desc = vision_response.choices[0].message.content
                    file_context = f"\n\n[Attached Extracted Image Content: {uploaded_file.name}]\n{image_desc}"
                except Exception as e:
                    file_context = f"\n\n[Error processing attached Image using Vision AI: {str(e)}]"
                    
        # Clear uploader visually isn't natively supported without complex state, but it handles per-request
        
    combined_input = user_input + file_context

    st.session_state.messages.append(
        {"role":"user","content":combined_input}
    )

    with st.chat_message("user"):
        st.markdown(user_input)
        if uploaded_file:
            st.caption(f"📎 Attached: {uploaded_file.name}")

    with st.chat_message("assistant"):

        with st.spinner(f"🧠 NexusAI ({selected_role} · {selected_engine}) is thinking..."):

            answer = generate_response(
                user_input=combined_input,
                conversation_history=st.session_state.messages,
                role=selected_role,
                engine=selected_engine,
                temp=temperature,
                max_t=max_tokens
            )

        st.markdown(answer, unsafe_allow_html=True)

    st.session_state.messages.append(
        {"role":"assistant","content":answer}
    )