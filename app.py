import os
from dotenv import load_dotenv
import gradio as gr 
from openai import OpenAI
import sqlite3
import json 
import gradio as gr 
from tools.expense_tools import add_expense, update_expenses,delete_expense
from tools.expense_tools import get_expenses, get_current_date
from datetime import date

load_dotenv(override=True)

openai_api_key = os.getenv("OPENAI_API_KEY")
if openai_api_key:
    print(f"OpenAI API key exists and begins {openai_api_key[:6]}")
else:
    print("OpenAI API key not found")
MODEL = "gpt-4.1-mini"
openai = OpenAI()

system_message = """ You are FinanceAgent, an AI assistant that helps users manage their personal finances.

Use the available tools whenever you need to add expenses, retrieve expenses, get the current date, set budgets, or generate financial summaries.

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
            "required": ["name", "amount"]
        }
    }
}

get_expense_tool = { "type": "function", "function": {
     "name": "get_expenses",
      "description": "Get the expenses of the user, optionally filtered by category or date",
       "parameters": { 
        "type": "object", "properties": { 
            "category": { 
                "type": "string", 
                "description": "The expense category, such as Food, Travel, Shopping, or Bills." 
            },
            "date": {
                "type": "string",
                "description": "The date of the expense to filter by in YYYY-MM-DD format."
            }
        }
      } 
    } 
} 

get_current_date_tool = {
    "type": "function",
    "function": {
        "name": "get_current_date",
        "description": "Get the current date in YYYY-MM-DD format.",
        "parameters": {
            "type": "object",
            "properties": {}
        }
    }
}

update_expense_tool = { "type": "function", "function": {
     "name": "update_expenses",
      "description": "Update an existing expense",
       "parameters": { 
        "type": "object", "properties": { 
            "name": { 
                "type": "string", 
                "description": "The name or description of the expense to update, such as Pizza, Coffee, or Groceries." 
                        },
            "amount":{
                "type" : "number",  
                "description" : "The new amount to update the expense to"         
                } 
                        
                        },
                        "required" : ["name","amount"]
                        
                        } 
                    } 
                } 
delete_expense_tool = { "type": "function", "function": {
     "name": "delete_expense",
      "description": "Delete an existing expense",
       "parameters": { 
        "type": "object", "properties": { 
            "expense_id": { 
                "type": "integer", 
                "description": "The unique ID of the expense to delete ." 
                        }
                        
                        },
                        "required" : ["expense_id"]
                        
                        } 
                    } 
                }
tools = [expense_tool,get_expense_tool,update_expense_tool,delete_expense_tool,get_current_date_tool]


def handle_tool_call(tool_call):
    if tool_call.function.name == "add_expense":
        arguments = json.loads(tool_call.function.arguments) if tool_call.function.arguments else {}
        result = add_expense(
            name = arguments["name"],
            amount = arguments["amount"],
            expense_date = arguments.get("date"),
            category = arguments.get("category")
            )
        return {
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": result
            }
    elif tool_call.function.name == "get_expenses":
        arguments = json.loads(tool_call.function.arguments) if tool_call.function.arguments else {}
        result = get_expenses(
           category = arguments.get("category"),
           expense_date = arguments.get("date")
            )
        return {
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": str(result)
            }
    elif tool_call.function.name == "get_current_date":
        result = get_current_date()
        return {
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": str(result)
            }
    elif tool_call.function.name == "update_expenses":
        arguments = json.loads(tool_call.function.arguments) if tool_call.function.arguments else {}
        result = update_expenses(
           name = arguments["name"],
           amount = arguments["amount"]
            )
        return {
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": str(result)
            }
    elif tool_call.function.name == "delete_expense":
        arguments = json.loads(tool_call.function.arguments) if tool_call.function.arguments else {}
        result = delete_expense(
           expense_id = arguments["expense_id"]
            )
        return {
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": str(result)
            }


def chat(message,history):
    current_date = date.today().isoformat()
    dynamic_system_message = f"{system_message}\n\nThe current date is {current_date}."
    messages = [{"role":"system","content":dynamic_system_message}] + history + [{"role":"user","content":message}]
    response = openai.chat.completions.create(model=MODEL,messages=messages,tools = tools)
    if response.choices[0].finish_reason == "tool_calls":
        assistant_message = response.choices[0].message
        messages.append(assistant_message)
        for tool_call in assistant_message.tool_calls:
            tool_response = handle_tool_call(tool_call)
            messages.append(tool_response)
        response = openai.chat.completions.create(model = MODEL,messages = messages)
    return response.choices[0].message.content


demo = gr.ChatInterface(chat)
demo.launch()



   

