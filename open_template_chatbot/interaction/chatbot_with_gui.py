from open_template_chatbot.llm_models import groq_template
from typing import AsyncGenerator

import streamlit as st
import asyncio


def to_sync_generator(async_gen: AsyncGenerator):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
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
        loop.close()


# with st.sidebar:
#     openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
#     "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
#     "[View the source code](https://github.com/streamlit/llm-examples/blob/main/Chatbot.py)"
#     "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"

st.title("💬 Chatbot")
st.caption("🚀 A Streamlit chatbot powered by OpenAI")
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    # if not openai_api_key:
    #     st.info("Please add your OpenAI API key to continue.")
    #     st.stop()

    # client = OpenAI(api_key=openai_api_key)
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    # response = client.chat.completions.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
    # response = await groq_template(prompt)
    # msg = response.choices[0].message.content
    # st.session_state.messages.append({"role": "assistant", "content": msg})
    # st.chat_message("assistant").write(msg)
    st.chat_message("assistant").write_stream(
        to_sync_generator(groq_template(prompt))
    )   
