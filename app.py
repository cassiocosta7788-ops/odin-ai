import streamlit as st
from datetime import datetime

st.set_page_config(
    page_title="ODIN AI",
    page_icon="⚡",
    layout="wide"
)

if "messages" not in st.session_state:
    st.session_state.messages = []

if "created_at" not in st.session_state:
    st.session_state.created_at = datetime.now().strftime("%d/%m/%Y")

st.markdown("""
<style>
.stApp {
    background: #0b1020;
    color: #f1f5f9;
}
section[data-testid="stSidebar"] {
    background: #111827;
}
h1, h2, h3 {
    color: #60a5fa;
}
.stChatMessage {
    background: #151e31;
    border: 1px solid #273449;
    border-radius: 14px;
    padding: 12px;
}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.title("⚡ ODIN AI")
    st.caption("Sua plataforma de inteligência artificial")
    st.divider()

    if st.button("＋ Nova conversa", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.subheader("Painel")
    st.write("🧠 Inteligência artificial")
    st.write("💬 Conversas")
    st.write("⚙️ Configurações")
    st.divider()
    st.caption("Versão inicial • 0.1")

st.title("⚡ ODIN AI")
st.write("Uma central de inteligência artificial construída por você.")
st.info(
    "Interface inicial pronta para receber a integração "
    "com um modelo de IA."
)

st.subheader("Conversa")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Escreva sua mensagem...")

if prompt:
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    answer = (
        "Recebi sua mensagem! A interface da ODIN AI está funcionando, "
        "mas ainda precisamos conectar um modelo de inteligência "
        "artificial para gerar respostas reais."
    )

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })

    with st.chat_message("assistant"):
        st.markdown(answer)
