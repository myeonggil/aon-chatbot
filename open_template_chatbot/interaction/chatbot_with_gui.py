from open_template_chatbot.llm_models import groq_template_stream
from asyncio import AbstractEventLoop
from typing import AsyncGenerator
from yaml import SafeLoader

import streamlit as st
import streamlit_authenticator as stauth
import asyncio
import yaml


def to_sync_generator(loop: AbstractEventLoop, async_gen: AsyncGenerator):
    try:
        stream_text = ''
        while True:
            try:
                task = anext(async_gen)
                chunk = loop.run_until_complete(task)
                stream_text += chunk
                yield chunk
            except StopAsyncIteration as _:
                print("stopped chat iteration")
                st.session_state.messages.append({"role": "assistant", "content": stream_text})
                task.close()
                break
            except Exception as err:
                print("Unknown", err)
                break
    finally:
        pass


# with st.sidebar:
#     openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
#     "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
#     "[View the source code](https://github.com/streamlit/llm-examples/blob/main/Chatbot.py)"
#     "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"

with open("./config.yaml") as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

try:
    # init everything when login
    authenticator.login()
    if st.session_state.get('authentication_status'):
        authenticator.logout()
        st.write(f'Welcome *{st.session_state.get("name")}*')
        st.title("💬 Chatbot")
        st.caption("🚀 A Streamlit chatbot powered by OpenAI")
        if "messages" not in st.session_state:
            st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

        for msg in st.session_state.messages:
            st.chat_message(msg["role"]).write(msg["content"])

        if prompt := st.chat_input():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

            st.session_state.messages.append({"role": "user", "content": prompt})
            st.chat_message("user").write(prompt)
            st.chat_message("assistant").write_stream(
                to_sync_generator(loop, groq_template_stream(prompt))
            )
            loop.close()
    elif st.session_state.get('authentication_status') is False:
        st.error('Username/password is incorrect')
    elif st.session_state.get('authentication_status') is None:
        st.warning('Please enter your username and password')

except Exception as e:
    print(e)
    st.error(e)
