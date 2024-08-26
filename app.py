from langchain_community.llms import Ollama
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langchain.schema.runnable import Runnable
from langchain.schema.runnable.config import RunnableConfig

import chainlit as cl


@cl.on_chat_start
async def on_chat_start():
    
    # Sending an image with the local file path
    # elements = [
    # cl.Image(name="image1", display="inline", path="gemma.jpeg")
    # ]
    await cl.Message(content="Hello there, I am Tim, your Technology Entrepreneurship study companion. How can I help you today?").send()
    model = Ollama(model="llama3.1:latest")
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a very experience expert in painpoint storytelling. Startup founders come to you with their companies propositions \
                and you help them shaping a story. You only give feedback to them, do not write their story for them, When giving feedback, \
                make sure that the story is as personal as possible, considering the persona. The core of the storytelling is to trigger emotions \
                and make sure that the audience is captivated by the story. Be succint in your feedback (use bulletpoint list) but be sure to elaborate your points\
                Give the list first, no description. Use a new line for each element. Use boldface. Then go into detail. Take is step by step. Think before you write."
            ),
            ("human", "{question}"),
        ]
    )
    runnable = prompt | model | StrOutputParser()
    cl.user_session.set("runnable", runnable)


@cl.on_message
async def on_message(message: cl.Message):
    runnable = cl.user_session.get("runnable")  # type: Runnable

    msg = cl.Message(content="")

    async for chunk in runnable.astream(
        {"question": message.content},
        config=RunnableConfig(callbacks=[cl.LangchainCallbackHandler()]),
    ):
        await msg.stream_token(chunk)

    await msg.send()
