import gradio as gr
import random
import time

import openai
import os

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

openai.api_key = os.getenv('OPENAI_API_KEY')
openai.api_type = "azure"
openai.api_base = "https://fs-hackathon.openai.azure.com/"
openai.api_version = "2023-05-15"  # subject to change

def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=0):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature,
        deployment_id="turbo-35",
    )
    return response.choices[0].message["content"]


messages =  [ {'role':'system', 'content':"""
You are Spend Adviser Bot, an automated service to analyze customer transaction to give them insight in their bank account, card transactions. \
You first greet the customer, then offer to help with their questions. \

You respond in a short, professional style. \

The customer is Anna. She is 25 years old, lives in New York, and works as a software engineer. \
Her entire transactions in the last 6 months are as follow in the csv format, begin with a header.
Do not ask her for the csv file, just use the following data.

```
transaction_id,timestamp,amount,currency,category,description,type \
trans_1,2021-01-01 00:00:00,10,USD,food,McDonalds,card \
trans_2,2021-01-02 00:00:00,1000,USD,service,AWS,account \
trans_3,2021-01-03 00:00:00,100,USD,food,McDonalds,card \
```
"""} ]  # accumulate messages

with gr.Blocks() as demo:
    chatbot = gr.Chatbot()
    msg = gr.Textbox()
    clear = gr.Button("Clear")

    def respond(message, chat_history):
        messages.append({'role': 'user', 'content': message})
        # process message
        bot_message = get_completion_from_messages(messages)
        # update chat history
        messages.append({'role': 'assistant', 'content': bot_message})
        chat_history.append((message, bot_message))
        time.sleep(1)
        return "", chat_history

    msg.submit(respond, [msg, chatbot], [msg, chatbot])
    clear.click(lambda: None, None, chatbot, queue=False)

demo.launch()
