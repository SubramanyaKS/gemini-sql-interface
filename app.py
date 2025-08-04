from services.llm import geminiCall
import streamlit as st
import pandas as pd
from services.schema import extract_schema
from services.connect import get_connection
from utils.constant import title,connect_success,connect_failure,subtitle,caption


st.title(title)
st.subheader(subtitle)
st.caption(caption)

with st.sidebar:
    st.title("Database Connection")
    db_url = st.text_input("PostgreSQL URL", placeholder="e.g. postgres://user:pass@host:port/dbname",type="password")
    connect_btn = st.button("Connect")
# db_url=st.sidebar.text_input("Enter postgres database url?", type="password")


if db_url:
    conn = get_connection(db_url)
    if not conn:
        st.warning("Connecting Database")
    
    if conn:
        st.success(connect_success)
        result_schema= extract_schema(conn)
        with st.expander("📊 View Database Schema"):
            st.write("Database Schema")
            st.code(result_schema)
            
        st.markdown("### 🧠 Ask a Question in Natural Language to DB")
        sql_instruct ="""You are a PosgreSQL expert. Convert natural language questions into accurate, efficient posgreSQL queries. Use standard SQL syntax. the table schema is provided ${res}.Do not include DROP, DELETE, UPDATE, INSERT, or any data-modifying command."""
       
        with st.form("text_to_sql_form"):
            user_input = st.text_input("Enter your question in natural language:")
            submitted = st.form_submit_button("Generate SQL")
        if submitted:
            result_sql=geminiCall(user_input,sql_instruct)
            st.session_state["generated_sql"] = result_sql
            
        if "generated_sql" in st.session_state:
            st.subheader("Generated SQL Query")
            st.write(st.session_state["generated_sql"])

            if st.button("Execute the SQL"):
                raw_sql = st.session_state["generated_sql"]
                clean_sql = raw_sql.strip().replace("```sql", "").replace("```", "").strip()
                cursor = conn.cursor()
                try:
                    cursor.execute(clean_sql)
                    query_result = cursor.fetchall()
                    # Get column names from cursor description
                    columns = [desc[0] for desc in cursor.description]
                    api_instruct ="""You are an assistant. Summerize the given SQL query result. Summerization should be short."""
                    nl_result=geminiCall(str(query_result),api_instruct)

                    # Convert to DataFrame
                    df = pd.DataFrame(query_result, columns=columns)
                    st.dataframe(df, use_container_width=True)
                    st.write(nl_result)
                    cursor.close()
                except Exception as e:
                    st.error(f"Error executing query: {e}")
                conn.close()

    else:
        st.error(connect_failure)

