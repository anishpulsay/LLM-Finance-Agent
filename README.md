# 💰 LLM Finance Agent

An AI-powered personal finance assistant built using **Python**, **OpenAI Tool Calling**, **SQLite**, and **Gradio**.

The assistant understands natural language queries and uses tool calling to manage a user's expenses through CRUD operations.

---

## ✨ Features

- ➕ Add expenses
- 📋 View expenses
- ✏️ Update existing expenses
- 🗑️ Delete expenses
- 📊 Generate financial summaries
- 💬 Natural language interface
- 🗄️ SQLite database backend
- 🤖 OpenAI Tool Calling

---

## 🛠️ Tech Stack

- Python
- OpenAI API
- SQLite
- Gradio
- JSON
- python-dotenv

---

## 📁 Project Structure

```
llm-finance-agent/
│
├── app.py
├── database/
│   ├── database.db
│   └── database.py
│
├── tools/
│   └── expense_tools.py
│
├── .env
├── README.md
└── requirements.txt
```

---

## 🚀 Installation

### Clone the repository

```bash
git clone https://github.com/<your-username>/llm-finance-agent.git

cd llm-finance-agent
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Create a `.env` file

```env
OPENAI_API_KEY=your_openai_api_key
```

### Run the application

```bash
python app.py
```

The Gradio interface will automatically open in your browser.

---

## 💬 Example Prompts

### Add an expense

```
I spent ₹450 on groceries.
```

```
I paid ₹800 for dinner yesterday.
```

---

### View expenses

```
Show all my expenses.
```

```
Show my Food expenses.
```

---

### Update an expense

```
Update my Pizza expense to ₹600.
```

---

### Delete an expense

```
Delete expense 5.
```

---

### Financial Summary

```
Give me my financial summary.
```

```
How much did I spend on Food?
```

```
How much did I spend this month?
```

```
How much did I spend on burgers this month?
```

---

## ⚙️ How It Works

1. The user enters a request in natural language.
2. The LLM determines whether a tool is required.
3. If necessary, the appropriate tool is called.
4. SQLite performs the requested database operation.
5. The tool returns structured data.
6. The LLM generates a natural language response.

```
User
   │
   ▼
OpenAI LLM
   │
Tool Calling
   │
   ▼
Python Tools
   │
SQLite Database
   │
   ▼
LLM Response
```

---

## 📌 Current Capabilities

- Add Expense
- Retrieve Expenses
- Update Expense
- Delete Expense
- Generate Financial Summary

---

## 🔮 Future Improvements

- Budget tracking
- Monthly spending limits
- Expense charts and visualizations
- Recurring expenses
- Multi-user authentication
- Multi-step tool chaining
- Support for multiple currencies

---

## 📷 Demo

<img width="932" height="469" alt="image" src="https://github.com/user-attachments/assets/c61e4ed2-83bd-4d26-baa9-7e7c71199d1b" />


---

## 📄 License

This project is licensed under the MIT License.
