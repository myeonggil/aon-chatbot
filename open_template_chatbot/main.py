# 간단한 langchain을 구현해보자
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from openai import AsyncOpenAI
from groq import Groq, AsyncGroq
from mangum import Mangum
from pydantic import BaseModel
from dotenv import dotenv_values

import openai
import asyncio
import json

app = FastAPI()
config = dotenv_values("open_template_chatbot/.env")
client = AsyncGroq(api_key=config["GROQ_API_KEY"])


class TestCreate(BaseModel):
    prompt: str


async def groq_template(prompt: str):
    """
        You will be provided with text delimited by triple quotes.
        If it contains a sequence of instructions, \
        re-write those instructions in the following format:
        Step 1 - 
        Step 2 - ...

        Step N - Output a

        If the text dose not contain a sequence of instructions, \
        then simply write \"No steps provided.\"

        \"\"\"prompt\"\"\"
    """
    response = await client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            # {
            #     "role": "assistant",
            # },
            {
                "role": "user",
                "content": prompt
            }
        ],
        stream=True,
        timeout=5,
        temperature=0.05, # more lower focus on consistency, more higher focus on newer answer
        max_tokens=256, # response maximum token length(different by language)
        top_p=1,    # random response match temperature 
        frequency_penalty=0,    # more lower use unique word
        presence_penalty=0  # more lower use similar and repeat word
    )

    # chat mode
    async for chunk in response:
        message = chunk.choices[0].delta.content
        if message is None:
            break
        data = f"data: {message} \n"
        yield data.encode()
        await asyncio.sleep(0.01)

    # finish chat
    yield b'data: complete \n'


@app.post("/groq")
async def chat_with_groq(test_create: TestCreate):
    streaming_response = groq_template(test_create.prompt)
    return StreamingResponse(
        content=streaming_response,
        media_type="text/event-stream"
    )


handler = Mangum(app)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app=app, host='0.0.0.0', port=8000)
