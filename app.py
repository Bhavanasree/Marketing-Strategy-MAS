import asyncio
import os
import json
from dotenv import load_dotenv
load_dotenv()

import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage
from graph.graph import graph

from auth import sign_in, sign_up, sign_out
from db import create_conversation, save_message, get_messages, get_conversations
from utils.title_generator import generate_title
from utils.pdf_generator import generate_final_plan_pdf


# ---------------------- PAGE CONFIG ----------------------
st.set_page_config(
    page_title="BrandForge AI",
    page_icon="🏗️",
    layout="wide"
)

# ---------------------- CSS STYLING ----------------------
st.markdown("""
    <style>
    .stApp {
        background-color: #f8f9fa;
    }
    .title {
        font-size: 3rem !important;
        font-weight: 800 !important;
        color: #1a1a1a !important;
        text-align: center;
        margin-bottom: 0px !important;
    }
    .subtitle-main {
        font-size: 1.2rem !important;
        color: #4a4a4a !important;
        text-align: center;
        margin-bottom: 5px !important;
    }
    .subtitle-secondary {
        font-size: 0.9rem !important;
        color: #8a8a8a !important;
        text-align: center;
        margin-bottom: 30px !important;
    }
    .stButton>button {
        border-radius: 8px !important;
        font-weight: 600 !important;
    }
    .stChatFloatingInputContainer {
        bottom: 20px !important;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------- AUTH SESSION ----------------------
if "user" not in st.session_state:
    st.session_state.user = None

if "page" not in st.session_state:
    st.session_state.page = "landing"

# ---------------------- AUTH HANDLERS ----------------------
def handle_login(email, password):
    res = sign_in(email, password)
    if res.user:
        st.session_state.user = res.user
        st.session_state.page = "app"
        st.rerun()
    else:
        st.error("Invalid credentials")

def handle_signup(email, password):
    sign_up(email, password)
    st.success("Account created! You can now login.")
    st.session_state.page = "login"

def handle_logout():
    sign_out()
    st.session_state.user = None
    st.session_state.page = "landing"
    st.rerun()

# ---------------------- VIEWS ----------------------

def show_landing():
    st.markdown("""
        <div style='text-align: center; padding: 100px 0;'>
            <h1>🏗️ BrandForge AI</h1>
            <p style='font-size: 1.5rem; color: #666;'>Your AI-powered Marketing Strategist</p>
            <p>From Logos to SEO, build your brand in minutes.</p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("Get Started", use_container_width=True, type="primary"):
            st.session_state.page = "login"
            st.rerun()
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("Explore Features", use_container_width=True):
             st.info("Logo Generation, SEO, Marketing Strategy, and more!")

def show_auth():
    st.markdown(f"<h2 style='text-align: center;'>{'Login' if st.session_state.page == 'login' else 'Create Account'}</h2>", unsafe_allow_html=True)
    
    with st.container():
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            
            if st.session_state.page == "login":
                if st.button("Login", use_container_width=True, type="primary"):
                    handle_login(email, password)
                if st.button("New here? Sign up", use_container_width=True):
                    st.session_state.page = "signup"
                    st.rerun()
            else:
                if st.button("Sign Up", use_container_width=True, type="primary"):
                    handle_signup(email, password)
                if st.button("Already have an account? Login", use_container_width=True):
                    st.session_state.page = "login"
                    st.rerun()
            
            if st.button("← Back to Home", use_container_width=True):
                st.session_state.page = "landing"
                st.rerun()

def show_app():
    # ---------------------- INITIALIZE STATE ----------------------
    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "display_history" not in st.session_state:
        st.session_state.display_history = []

    if "conversation_id" not in st.session_state:
        st.session_state.conversation_id = None

    if "loaded_history" not in st.session_state:
        st.session_state.loaded_history = False

    if "current_logo" not in st.session_state:
        st.session_state.current_logo = None

    user_id = st.session_state.user.id
    convos = get_conversations(user_id)

    # ---------------------- LOAD HISTORY ----------------------
    if not st.session_state.loaded_history:
        if st.session_state.conversation_id:
            past_msgs = get_messages(st.session_state.conversation_id)
            st.session_state.display_history = []
            st.session_state.messages = []

            for msg in past_msgs:
                role = msg["role"]
                content = msg["content"]
                
                # Check if content is dict (for logo/text combo)
                if isinstance(content, str) and content.startswith("{"):
                    try:
                        content = json.loads(content)
                    except:
                        pass
                
                st.session_state.display_history.append((role, content))
                
                if role == "user":
                    st.session_state.messages.append(HumanMessage(content=content))
                else:
                    text_content = content["text"] if isinstance(content, dict) else content
                    st.session_state.messages.append(AIMessage(content=text_content))

            # Set current logo to the latest one found in history
            for role, content in reversed(st.session_state.display_history):
                if role == "assistant" and isinstance(content, dict) and content.get("logo_path"):
                    st.session_state.current_logo = content["logo_path"]
                    break

        st.session_state.loaded_history = True



    # ---------------------- HELPERS ----------------------
    def _render_extras(extras: dict):
        logo_path = extras.get("logo_path")
        if logo_path and os.path.exists(logo_path):
            st.image(logo_path, caption="Generated Logo", width=250)


    def get_latest_logo():
        folder = "generated_logos"
        if not os.path.exists(folder):
            return None

        files = [f for f in os.listdir(folder) if f.endswith(".png")]
        if not files:
            return None

        files.sort(key=lambda x: os.path.getmtime(os.path.join(folder, x)), reverse=True)
        return os.path.join(folder, files[0])
    

    def get_final_response():
        for role, content in reversed(st.session_state.display_history):
            if role == "assistant":
                if isinstance(content, dict):
                    return content.get("text", "")
                return content
        return None
    


    # ---------------------- SIDEBAR ----------------------
    with st.sidebar:
        st.markdown("## 🏗️ BrandForge AI")
        st.image("BrandForge.png", width=120)

        if st.button("🚪 Logout", use_container_width=True):
            handle_logout()

        st.divider()
        st.markdown("### 💬 Conversations")

        if st.button("➕ New Chat", use_container_width=True):
            st.session_state.conversation_id = None
            st.session_state.messages = []
            st.session_state.display_history = []
            st.session_state.loaded_history = True # Already reset
            st.rerun()

        for c in convos:
            if st.button(c["title"], key=f"conv_{c['id']}", use_container_width=True):
                st.session_state.conversation_id = c["id"]
                st.session_state.loaded_history = False
                st.rerun()

        st.divider()
        st.markdown("### 💡 Capabilities")
        st.markdown("""
        - Logo Generation  
        - SEO Keyword creation  
        - Marketing Strategy
        - Tagline generation
        - Domain suggestion
        - Social Media Content  
        - Ad Copy & email Campaigns  
        """)

        st.divider()

        if st.button("📄 Export Final Marketing Plan"):
            final_text = get_final_response()

            if final_text:

                logo_path = st.session_state.get("current_logo")

                file_path = generate_final_plan_pdf(final_text, logo_path)

                with open(file_path, "rb") as f:
                    st.download_button(
                        label="⬇️ Download PDF",
                        data=f,
                        file_name="marketing_plan.pdf",
                        mime="application/pdf"
                    )
            else:
                st.warning("No final plan available yet.")


    # ---------------------- HEADER ----------------------
    st.markdown('<div class="title">BrandForge AI</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle-main">Your Personalized Marketing Strategy AI Assistant</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle-secondary">Powered by AWS Bedrock + LangGraph</div>', unsafe_allow_html=True)
    st.divider()



    # ---------------------- CHAT HISTORY ----------------------
    for role, content in st.session_state.display_history:
        with st.chat_message(role):
            if isinstance(content, dict):
                clean_text = content["text"]
                st.markdown(clean_text)
                _render_extras(content)
            else:
                st.markdown(content)

    # ---------------------- STREAM FUNCTION ----------------------
    async def run_agent_stream(messages):
        """Stream tokens from the graph using astream_events."""
        full_response = ""
        placeholder = st.empty()
        is_tool_turn = False 
        logo_generated = False # 🚀 Track if logo agent was ever called

        with st.spinner("Analyzing and building brand assets..."):
            async for event in graph.astream_events(
                {"messages": messages},
                version="v2",
            ):
                kind = event["event"]

                if kind == "on_chat_model_stream":
                    chunk = event["data"]["chunk"]
                    content = chunk.content

                    if isinstance(content, list):
                        text = "".join(
                            block.get("text", "") if isinstance(block, dict) else str(block)
                            for block in content
                        )
                    else:
                        text = content or ""

                    if text:
                        full_response += text
                        placeholder.markdown(full_response + "▌")

                elif kind == "on_tool_start":
                    tool_name = event.get("name", "tool")
                    placeholder.markdown(
                        full_response + f"\n\n⚙️ *Running {tool_name}...*"
                    )

            placeholder.markdown(full_response)
            return full_response
    # ---------------------- INPUT ----------------------
    if prompt := st.chat_input("Ask for domains, logos, strategy, social media, email campaigns, SEO, ads, or taglines..."):

        # 🧠 Create conversation if first message
        if not st.session_state.conversation_id:
            title = generate_title(prompt)
            conv_id = create_conversation(user_id, title)
            st.session_state.conversation_id = conv_id

        conv_id = st.session_state.conversation_id

        # 👤 USER MESSAGE
        st.chat_message("user").markdown(prompt)
        st.session_state.display_history.append(("user", prompt))
        st.session_state.messages.append(HumanMessage(content=prompt))

        save_message(conv_id, "user", prompt)

        # 🤖 ASSISTANT RESPONSE
        with st.chat_message("assistant"):
            st.session_state.current_logo = None # Reset logo for new turn
            raw_response = asyncio.run(run_agent_stream(st.session_state.messages))
            full_response = raw_response

            # Detect if logo was generated
            logo_path = None
            if "logo" in full_response.lower() and "generated" in full_response.lower():
                logo_path = get_latest_logo()
                st.session_state.current_logo = logo_path

            extras = {"logo_path": st.session_state.current_logo}
            _render_extras(extras)

        st.session_state.messages.append(AIMessage(content=full_response))

        st.session_state.display_history.append(
            ("assistant", {"text": full_response, **extras})
        )

        save_message(conv_id, "assistant", json.dumps({"text": full_response, **extras}))

# ---------------------- MAIN ROUTER ----------------------
if st.session_state.user:
    show_app()
elif st.session_state.page == "landing":
    show_landing()
elif st.session_state.page in ["login", "signup"]:
    show_auth()

