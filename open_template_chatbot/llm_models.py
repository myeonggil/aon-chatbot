# 간단한 langchain을 구현해보자
from groq import AsyncGroq
from dotenv import dotenv_values
from open_template_chatbot.database.mongodb_cluster import MongoDBCluster

import asyncio

config = dotenv_values("open_template_chatbot/.env")
client = AsyncGroq(api_key=config["GROQ_API_KEY"])


async def groq_template_stream(query: str):
    """
        You are helpful assistant. \n
        You will be provided with text delimited by triple quotes.
        If it contains a sequence of instructions, \n
        re-write those instructions in the following format:
        Step 1 - 
        Step 2 - ...

        Step N - Output summarize

        If the text dose not contain a sequence of instructions, \n
        then simply write \"No steps provided.\"

        \"\"\"prompt\"\"\"
    """
    mongo_cluster = MongoDBCluster()
    context_string = await mongo_cluster.get_context_string_from_docs(query=query)
    prompt = f"""Use the following pieces of context to answer the question at the end.
        {context_string}
        Question: {query}
    """
    # Let's understand how to make chaining chat completion?
    # We can give question and answer to chat completion
    # I think that It look like expect chatbot need to answer as my hope
    # Are messages chat chain?
    response = await client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            # {
            #     "role": "assistant",
            # },
            {
                "role": "user",
                "content": prompt
            },
            {
                "role": "user",
                "content": "Please summarize smaller than maximum tokens"
            }
        ],
        stream=True,
        timeout=5,
        temperature=0.05, # more lower focus on consistency, more higher focus on newer answer
        max_tokens=512, # response maximum token length(different by language) Between 512 and 1024
        top_p=1,    # random response match temperature 
        frequency_penalty=0,    # more lower use unique word
        presence_penalty=0  # more lower use similar and repeat word
    )

    # chat mode
    async for chunk in response:
        message = chunk.choices[0].delta.content
        # if message is None:
        #     break
        # data = f"data: {message} \n"
        # yield data.encode()
        if message is not None:
            yield message
        await asyncio.sleep(0.01)
    await mongo_cluster.close()


async def groq_template_response(prompt: str):
    """
        You are helpful assistant. \n
        You will be provided with text delimited by triple quotes.
        If it contains a sequence of instructions, \n
        re-write those instructions in the following format:
        Step 1 - 
        Step 2 - ...

        Step N - Output summarize

        If the text dose not contain a sequence of instructions, \n
        then simply write \"No steps provided.\"

        \"\"\"prompt\"\"\"
    """
    # Let's understand how to make chaining chat completion?
    # We can give question and answer to chat completion
    # I think that It look like expect chatbot need to answer as my hope
    # Are messages chat chain?
    response = await client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            # {
            #     "role": "assistant",
            # },
            {
                "role": "user",
                "content": prompt
            },
            {
                "role": "user",
                "content": "Please summarize smaller than maximum tokens"
            }
        ],
        stream=False,
        timeout=5,
        temperature=0.05, # more lower focus on consistency, more higher focus on newer answer
        max_tokens=512, # response maximum token length(different by language) Between 512 and 1024
        top_p=1,    # random response match temperature 
        frequency_penalty=0,    # more lower use unique word
        presence_penalty=0  # more lower use similar and repeat word
    )

    if response.choices:
        return response.choices[0].message.content
    else:
        return None
