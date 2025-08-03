from services.llm import geminiCall
import streamlit as st
from services.schema import extract_schema
from services.connect import get_connection
from utils.constant import title,connect_success,connect_failure
st.title(title)

db_url=st.sidebar.text_input("Enter postgres database url?", type="password")

if db_url:
    st.warning("Connecting Database")
    conn = get_connection(db_url)
    
    if conn:
        st.success(connect_success)
        res= extract_schema(conn)
        api_instruct ="""You are a PosgreSQL expert. Convert natural language questions into accurate, efficient posgreSQL queries. Use standard SQL syntax. the table schema is provided ${res}.Do not include DROP, DELETE, UPDATE, INSERT, or any data-modifying command."""
        with st.form("text_to_sql_form"):
            user_input = st.text_input("Enter your question in natural language:")
            submitted = st.form_submit_button("Generate SQL")
        if submitted:
            result_sql=geminiCall(user_input,api_instruct)
            st.subheader("Generated SQL Query")
            st.code(result_sql,language='sql')
    else:
        st.error(connect_failure)

