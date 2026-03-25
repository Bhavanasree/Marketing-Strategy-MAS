import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage
from graph.graph import graph


# ---------------------- PAGE CONFIG ----------------------
st.set_page_config(
    page_title="BrandForge AI",
    page_icon="🏗️",
    layout="wide"
)

# ---------------------- CUSTOM CSS ----------------------
st.markdown("""
<style>
    .main {
        padding-top: 1rem;
    }
    .stChatMessage {
        border-radius: 12px;
        padding: 10px;
        margin-bottom: 8px;
    }
    .stChatMessage[data-testid="stChatMessage-user"] {
        background-color: #f0f2f6;
    }
    .stChatMessage[data-testid="stChatMessage-assistant"] {
        background-color: #ffffff;
        border: 1px solid #e6e6e6;
    }
    .title {
        font-size: 40px;
        font-weight: 800;
        background: linear-gradient(#0474BA, #F17720);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: 1px;
    }
    .subtitle-main {
        color: #374151;
        font-size: 16px;
        font-weight: 500;
        margin-bottom: 2px;
    }
    .subtitle-secondary {
        color: #9ca3af;
        font-size: 13px;
        font-style: italic;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------- SIDEBAR ----------------------
with st.sidebar:
    st.markdown("## 🏗️ BrandForge AI")
    st.image("BrandForge.png", width=120)
    st.markdown("Build your brand faster with AI-powered tools.")
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

# ---------------------- HEADER ----------------------
st.markdown('<div class="title">BrandForge AI</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle-main">Your Personlized Marketing Strategy AI Assistant</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle-secondary">Powered by AWS Bedrock + LangGraph</div>', unsafe_allow_html=True)
st.divider()

# ---------------------- STATE ----------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "display_history" not in st.session_state:
    st.session_state.display_history = []

if "current_logo" not in st.session_state:
    st.session_state.current_logo = None

if len(st.session_state.messages) == 0:
    st.session_state.current_logo = None

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


# ---------------------- CHAT HISTORY ----------------------
for role, content in st.session_state.display_history:
    with st.chat_message(role):
        if isinstance(content, dict):
            st.markdown(content["text"])
            _render_extras(content)
        else:
            st.markdown(content)

# ---------------------- STREAM FUNCTION ----------------------
async def run_agent_stream(messages):
    full_response = ""
    placeholder = st.empty()

    with st.spinner("Thinking..."):
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
if prompt := st.chat_input("Ask for logo, SEO, ads, strategy..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.display_history.append(("user", prompt))

    st.session_state.messages.append(HumanMessage(content=prompt))

    with st.chat_message("assistant"):
        full_response = asyncio.run(run_agent_stream(st.session_state.messages))

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
