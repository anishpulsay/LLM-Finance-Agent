import os
from dotenv import load_dotenv
import gradio as gr 
from openai import OpenAI
import sqlite3
import json 
import gradio as gr 
from tools.expense_tools import add_expense

load_dotenv(override=True)

openai_api_key = os.getenv("OPENAI_API_KEY")
if openai_api_key:
    print(f"OpenAI API key exists and begins {openai_api_key[:6]}")
else:
    print("OpenAI API key not found")
MODEL = "gpt-5.1-mini"
openai = OpenAI()

system_message = """ You are FinanceAgent, an AI assistant that helps users manage their personal finances.

Use the available tools whenever you need to add expenses, retrieve expenses, set budgets, or generate financial summaries.

Never make up financial data. If information is missing, ask the user for clarification before calling a tool.

Keep your responses clear, concise, and helpful.
 """
def chat(message,history):
    messages = [{"role":"system","content":system_message}] + history + [{"role":"user","content":message}]
    response = openai.chat.completions.create(model=MODEL,messages=messages)
    return response.choices[0].message.content
    
    
add_expense("Pizza",350,"2026-03-02","Food")
print("Done")    

