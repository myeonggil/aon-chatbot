# 간단한 langchain을 구현해보자
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from groq import AsyncGroq
from mangum import Mangum
from pydantic import BaseModel
from dotenv import dotenv_values
from open_template_chatbot.llm_models import groq_template


app = FastAPI()
config = dotenv_values("open_template_chatbot/.env")
client = AsyncGroq(api_key=config["GROQ_API_KEY"])


class TestCreate(BaseModel):
    prompt: str


@app.get("/groq")
async def chat_with_groq(prompt: str):
    streaming_response = groq_template(prompt)
    return StreamingResponse(
        content=streaming_response,
        media_type="text/event-stream"
    )


handler = Mangum(app)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app=app, host='0.0.0.0', port=8080)
