# 🧠 Text-to-SQL App with Gemini, Streamlit & PostgreSQL

This project is a simple Text-to-SQL interface where users can input natural language questions and receive SQL-generated answers based on a PostgreSQL database. It uses Google's **Gemini API** for language understanding and **Streamlit** for a lightweight web UI.

---

## 🚀 Features

- 🔗 Connect to a PostgreSQL database
- 💬 Accept natural language input and convert it to SQL
- 🧠 Uses Gemini for query generation
- 📝 Edit generated SQL manually
- 📊 View query results in table format
- 🔍 View database schema
- 🛡️ Restricts destructive queries (no DELETE, DROP, etc.)

---

## 🧱 Built With

- [Streamlit](https://streamlit.io/)
- [Google Gemini API](https://ai.google.dev)
- [PostgreSQL](https://www.postgresql.org/)
- [Python 3.10+](https://www.python.org/)

## 🔧 Setup Instructions

1. Clone the repository

```bash
git clone https://github.com/SubramanyaKS/gemini-sql-interface.git
cd gemini-sql-interface
```
2. Create a virtual environment (optional but recommended)
```bash
python -m venv .venv
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

```bash
GEMINI_API_KEY="<your-gemini-api>"
GEMINI_MODEL="<your-prefered-model>"
```

5. Run the Streamlit app

```bash
streamlit run app.py
```
## 🤝 Contributing

Contributions are welcome! Please fork the repo and submit a pull request.

## 🙏 Acknowledgements

- Google Gemini API
- Streamlit Team
- OpenAI for inspiration