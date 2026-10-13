
import streamlit as st
# from agent import chat_with_agent

st.set_page_config(
    page_title="Voyage AI | Ticket Booking",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- Styling ----------
st.markdown("""
<style>
    .stApp {
        background-color: #f5f7fb;
    }
    [data-testid="stSidebar"] {
        background-color: #101827;
    }
    [data-testid="stSidebar"] * {
        color: #edf3ff;
    }
    .hero {
        padding: 22px 24px;
        border-radius: 18px;
        background: linear-gradient(120deg, #142744, #315b91);
        color: white;
        margin-bottom: 22px;
    }
    .hero p {
        color: #d9e6f8;
        margin-bottom: 0;
    }
    .stChatMessage {
        border-radius: 14px;
        border: 1px solid #e5eaf2;
        background-color: white;
    }
    div[data-testid="stChatInput"] {
        border-radius: 16px;
    }
</style>
""", unsafe_allow_html=True)

# ---------- Sidebar ----------
with st.sidebar:
    st.markdown("# ✈️ Voyage AI")
    st.caption("YOUR PERSONAL TRAVEL ASSISTANT")
    st.divider()

    st.markdown("### Explore")
    st.markdown("🔎  Find flights")
    st.markdown("🎫  Manage bookings")
    st.markdown("💬  Travel assistance")

    st.divider()
    st.markdown("### Try asking")
    st.caption("• Find flights from Delhi to Mumbai")
    st.caption("• Show flights under ₹4,000")
    st.caption("• Which flight is cheapest?")

    if st.button("＋ New conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.divider()
    st.caption("Demo version · Dummy ticket data")

# ---------- Main header ----------
st.markdown("""
<div class="hero">
    <h1>Where to next? 🌍</h1>
    <p>Tell me your destination and I'll help you find a flight.</p>
</div>
""", unsafe_allow_html=True)

# ---------- Session state ----------
if "messages" not in st.session_state:
    st.session_state.messages = []

# Welcome screen
if not st.session_state.messages:
    st.markdown("### Start exploring")
    col1, col2, col3 = st.columns(3)

    if col1.button("✈️ Delhi → Mumbai", use_container_width=True):
        st.session_state.pending_prompt = (
            "Find flights from Delhi to Mumbai"
        )
    if col2.button("💰 Budget flights", use_container_width=True):
        st.session_state.pending_prompt = (
            "Find flights from Delhi to Mumbai under 5000 rupees"
        )
    if col3.button("🧭 Explore options", use_container_width=True):
        st.session_state.pending_prompt = (
            "What routes are available in your ticket database?"
        )

# ---------- Display chat history ----------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ---------- Chat input ----------
prompt = st.chat_input("Ask me to find a flight...")

if "pending_prompt" in st.session_state:
    prompt = st.session_state.pop("pending_prompt")

if prompt:
    st.session_state.messages.append({
        "role": "user",
        "content": prompt,
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Finding the best options..."):
            try:
                answer = chat_with_agent(
                    st.session_state.messages.copy()
                )
                if not answer:
                    answer = "I couldn't generate a response. Please try again."
            except Exception as e:
                st.error(f"Something went wrong: {e}")
                answer = (
                    "I couldn't complete that request. "
                    "Please try again."
                )

        st.markdown(answer)

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer,
    })
