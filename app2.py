import gradio as gr
import random
import time

import openai
import os

from dotenv import load_dotenv,find_dotenv
import pandas as pd
from langchain.chat_models import ChatOpenAI
from langchain.agents import create_pandas_dataframe_agent

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

openai.api_key = os.getenv('OPENAI_API_KEY')
openai.api_type = "azure"
openai.api_base = "https://fs-hackathon.openai.azure.com/"
openai.api_version = "2023-05-15"  # subject to change

df = pd.read_csv('orders_data.csv')
chat = ChatOpenAI(model_name="gpt-35-turbo",temperature=0.0, model_kwargs={'engine':'turbo-35'})
agent = create_pandas_dataframe_agent(chat, df, verbose=True)


def get_answer(question):
    return agent.run(question)

with gr.Blocks() as demo:
    chatbot = gr.Chatbot()
    msg = gr.Textbox()
    clear = gr.Button("Clear")

    def respond(message, chat_history):
        bot_message = get_answer(message)
        chat_history.append((message, bot_message))
        time.sleep(1)
        return "", chat_history

    msg.submit(respond, [msg, chatbot], [msg, chatbot])
    clear.click(lambda: None, None, chatbot, queue=False)

demo.launch()
