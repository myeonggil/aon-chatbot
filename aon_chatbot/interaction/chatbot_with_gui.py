from asyncio import AbstractEventLoop
from typing import AsyncGenerator, Callable
from yaml import SafeLoader

import asyncio
import yaml


class ChatbotWithGUI:
    def __init__(self):
        import streamlit as st
        import streamlit_authenticator as stauth

        self.st = st
        self.stauth = stauth
        # with st.sidebar:
        #     openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
        #     "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
        #     "[View the source code](https://github.com/streamlit/llm-examples/blob/main/Chatbot.py)"
        #     "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"

        with open("./config.yaml") as file:
            self.config = yaml.load(file, Loader=SafeLoader)

        self.authenticator = self.stauth.Authenticate(
            self.config['credentials'],
            self.config['cookie']['name'],
            self.config['cookie']['key'],
            self.config['cookie']['expiry_days']
        )

    def to_sync_generator(self, loop: AbstractEventLoop, async_gen: AsyncGenerator):
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
                    self.st.session_state.messages.append({"role": "assistant", "content": stream_text})
                    task.close()
                    break
                except Exception as err:
                    print("Unknown", err)
                    break
        finally:
            pass

    def start_app(self, func: Callable):
        try:
            # init everything when login
            self.authenticator.login()
            if self.st.session_state.get('authentication_status'):
                self.authenticator.logout()
                self.st.write(f'Welcome *{self.st.session_state.get("name")}*')
                self.st.title("💬 Chatbot")
                self.st.caption("🚀 A Streamlit chatbot powered by OpenAI")
                if "messages" not in self.st.session_state:
                    self.st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

                for msg in self.st.session_state.messages:
                    self.st.chat_message(msg["role"]).write(msg["content"])

                if prompt := self.st.chat_input():
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)

                    self.st.session_state.messages.append({"role": "user", "content": prompt})
                    self.st.chat_message("user").write(prompt)
                    self.st.chat_message("assistant").write_stream(
                        self.to_sync_generator(loop, func(prompt))
                    )
                    loop.close()
            elif self.st.session_state.get('authentication_status') is False:
                self.st.error('Username/password is incorrect')
            elif self.st.session_state.get('authentication_status') is None:
                self.st.warning('Please enter your username and password')

        except Exception as e:
            print(e)
            self.st.error(e)
