from services.llm import geminiCall
import streamlit as st
from services.schema import extract_schema
from services.connect import get_connection
from utils.constant import title,connect_success,connect_failure,subtitle,caption


st.title(title)
st.subheader(subtitle)
st.caption(caption)
db_url=st.sidebar.text_input("Enter postgres database url?", type="password")


if db_url:
    conn = get_connection(db_url)
    if not conn:
        st.warning("Connecting Database")
    
    if conn:
        st.success(connect_success)
        res= extract_schema(conn)
        st.write("Database Schema")
        st.code(res)
        api_instruct ="""You are a PosgreSQL expert. Convert natural language questions into accurate, efficient posgreSQL queries. Use standard SQL syntax. the table schema is provided ${res}.Do not include DROP, DELETE, UPDATE, INSERT, or any data-modifying command."""
        st.subheader("Curious? Ask away!")
        with st.form("text_to_sql_form"):
            user_input = st.text_input("Enter your question in natural language:")
            submitted = st.form_submit_button("Generate SQL")
        if submitted:
            result_sql=geminiCall(user_input,api_instruct)
            st.session_state["generated_sql"] = result_sql
            
        if "generated_sql" in st.session_state:
            st.subheader("Generated SQL Query")
            st.write(st.session_state["generated_sql"])
            print(st.session_state["generated_sql"])

            if st.button("Execute the SQL"):
                raw_sql = st.session_state["generated_sql"]
                clean_sql = raw_sql.strip().replace("```sql", "").replace("```", "").strip()
                cursor = conn.cursor()
                try:
                    cursor.execute(clean_sql)
                    query_result = cursor.fetchall()
                    st.write(query_result)
                except Exception as e:
                    st.error(f"Error executing query: {e}")

    else:
        st.error(connect_failure)

