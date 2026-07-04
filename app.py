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


expense_tool = {
    "type": "function",
    "function": {
        "name": "add_expense",
        "description": "Add a new expense to the user's expense database.",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "The name or description of the expense."
                },
                "amount": {
                    "type": "number",
                    "description": "The amount spent."
                },
                "date": {
                    "type": "string",
                    "description": "The date of the expense in YYYY-MM-DD format."
                },
                "category": {
                    "type": "string",
                    "description": "The expense category, such as Food, Travel, Shopping, or Bills."
                }
            },
            "required": ["name", "amount", "date", "category"]
        }
    }
}
tools = [expense_tool]


def handle_tool_call(message):
    tool_call = message.tool_calls[0]
    if tool_call.function.name == "add_expense":
        arguments = json.loads(tool_call.function.arguments)
        result = add_expense(
            name = arguments["name"],
            amount = arguments["amount"],
            date = arguments.get("date"),
            category = arguments["category"]
            )
        return {
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": result
            }


def chat(message,history):
    messages = [{"role":"system","content":system_message}] + history + [{"role":"user","content":message}]
    response = openai.chat.completions.create(model=MODEL,messages=messages,tools = tools)
    if response.choices[0].finish_reason == "tool_calls":
        message = response.choices[0].message
        response = handle_tool_call(message)
        messages.append(message)
        messages.append(response)
        response = openai.chat.completions.create(model = MODEL,messages = messages)
    return response.choices[0].message.content




   

