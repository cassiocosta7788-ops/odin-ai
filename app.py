import os
import streamlit as st
from groq import Groq
from groq import (
    AuthenticationError,
    PermissionDeniedError,
    RateLimitError,
    NotFoundError,
    APIConnectionError,
    APIStatusError,
)

st.set_page_config(
    page_title="ODIN AI",
    page_icon="⚡",
    layout="wide"
)

if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.title("⚡ ODIN AI")
    st.caption("Sua inteligência artificial")
    if st.button("＋ Nova conversa", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

st.title("⚡ ODIN AI")
st.write("Sua central de inteligência artificial.")

api_key = os.environ.get("GROQ_API_KEY")

if not api_key:
    st.error("GROQ_API_KEY não está configurada no Render.")
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
                   model="openai/gpt-oss-120b", 
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "Você é a ODIN AI, uma assistente "
                                "inteligente, útil e honesta. "
                                "Responda em português quando "
                                "o usuário escrever em português."
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
                    or "A IA retornou uma resposta vazia."
                )

                st.markdown(answer)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })

            except AuthenticationError:
                st.error("Erro 401: confira a chave GROQ_API_KEY no Render.")
            except PermissionDeniedError:
                st.error("Erro 403: a conta não tem permissão para essa solicitação.")
            except RateLimitError:
                st.error("Erro 429: limite de uso atingido. Confira os limites da Groq.")
            except NotFoundError:
                st.error("Erro 404: o modelo solicitado não foi encontrado ou não está disponível.")
            except APIConnectionError:
                st.error("Falha de conexão com a Groq. Tente novamente.")
            except APIStatusError as error:
                st.error(f"A Groq retornou o erro HTTP {error.status_code}.")
            except Exception as error:
                st.error(f"Erro inesperado: {type(error).__name__}.")
