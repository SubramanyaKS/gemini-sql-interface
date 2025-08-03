# 🧠 Text-to-SQL App with Gemini, Streamlit & PostgreSQL

This project is a simple Text-to-SQL interface where users can input natural language questions and receive SQL-generated answers based on a PostgreSQL database. It uses Google's **Gemini API** for language understanding and **Streamlit** for a lightweight web UI.

---

## 🚀 Features

- Natural language query interface
- Gemini API generates SQL queries from plain text
- Executes generated SQL against a PostgreSQL database
- Streamlit front-end for interactive querying
- Simple and extensible architecture

---

## 🔧 Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/SubramanyaKS/gemini-sql-interface.git
cd gemini-sql-interface
```
2. Create a virtual environment (optional but recommended)
```bash
python -m venv venv
source venv/bin/activate
   or 
venv\Scripts\activate on Windows
```
3. Install dependencies

```bash
pip install -r requirements.txt
```
4. Configure API keys

create secrets.toml inside .streamlit folder in root of project and past below

```
GEMINI_API_KEY="<your-gemini-api>"
GEMINI_MODEL="<your-prefered-model>"
```

5. Run the Streamlit app

```bash
streamlit run app.py
```