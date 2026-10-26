import os
import streamlit as st
from groq import Groq

st.set_page_config(
    page_title="ODIN AI",
    page_icon="⚡",
    layout="wide"
)

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
    border-radius: 14px;
}
</style>
""", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.title("⚡ ODIN AI")
    st.caption("Sua inteligência artificial")
    st.divider()

    if st.button("＋ Nova conversa", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.write("🧠 Motor: Groq")
    st.write("💬 Conversas")
    st.caption("Versão 0.2")

st.title("⚡ ODIN AI")
st.write("Sua central de inteligência artificial.")

api_key = os.environ.get("GROQ_API_KEY")

if not api_key:
    st.error(
        "Chave não configurada. Adicione GROQ_API_KEY "
        "nas variáveis de ambiente do Render."
    )
    st.stop()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Pergunte qualquer coisa...")

if prompt:
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("ODIN está pensando..."):
            try:
                client = Groq(api_key=api_key)

                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "Você é a ODIN AI, uma assistente "
                                "inteligente, útil e honesta. "
                                "Responda no idioma do usuário. "
                                "Explique claramente suas limitações."
                            )
                        },
                        *st.session_state.messages[-20:]
                    ],
                    max_completion_tokens=1024,
                    temperature=0.7,
                    timeout=60
                )

                answer = (
                    response.choices[0].message.content
                    or "Não consegui gerar uma resposta."
                )

                st.markdown(answer)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })

            except Exception as error:
                st.error(
                    "Não consegui consultar a IA. "
                    "Verifique os logs do Render e os limites "
                    "ou a disponibilidade do modelo na Groq."
                )
                print(f"Erro na API da Groq: {type(error).__name__}")
