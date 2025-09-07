from services.llm import geminiCall
import streamlit as st
import pandas as pd
from services.schema import extract_schema, generate_schema_prompt
from services.connect import get_connection,get_placeholder
from services.services import generate_instruction, get_relevant_tables
from utils.config import supported_databases
from utils import constant as cnt
from sqlalchemy import text


st.title(cnt.title)
st.subheader(cnt.subtitle)
st.caption(cnt.caption)

with st.sidebar:
    st.title("Database Connection")
    option = st.selectbox(
"Select the Database",
supported_databases
)
    
    db_url = st.text_input(f"{option} URL", placeholder=get_placeholder(option),type="password")
    connect_btn = st.button("Connect")


if db_url:
    try:
        conn = get_connection(db_url)
    except Exception as e:
        st.error(f"Failed to connect to DB: {e}")
        conn = None

    if conn:
        st.success(cnt.connect_success)
        try:
            result_schema = extract_schema(conn)
            with st.expander(cnt.view_schema):
                st.write("Database Schema")
                for table, columns in result_schema.items():
                    st.markdown(f"**{table}**")
                    st.markdown(f"Columns: {', '.join(columns)}")
        except Exception as e:
            st.error(f"Failed to extract schema: {e}")

        st.markdown(cnt.ask_question)
        with st.form("text_to_sql_form"):
            user_input = st.text_input(cnt.enter_question)
            submitted = st.form_submit_button("Generate SQL")

        if submitted:
            relevant_tables = get_relevant_tables(user_input, result_schema)
            schema_text = generate_schema_prompt(relevant_tables, result_schema)
            sql_instruction= generate_instruction(option,schema_text)
            result_sql = geminiCall(user_input, sql_instruction)
            st.session_state["generated_sql"] = result_sql

        if "generated_sql" in st.session_state:
            st.subheader("Generated SQL Query")
            st.write(st.session_state["generated_sql"])

            # Optionally edit SQL
            edit_sql = st.checkbox('Edit query', value=False)
            if edit_sql:
                modified_sql = st.text_area('Modified SQL', value=st.session_state["generated_sql"])
                raw_sql = modified_sql
            else:
                raw_sql = st.session_state["generated_sql"]

            # Execute button
            if st.button("Execute the SQL"):
                clean_sql = raw_sql.strip().replace("```sql", "").replace("```", "").strip()
                try:
                    res = conn.execute(text(clean_sql))
                    query_result = res.fetchall()
                    columns = res.keys()

                    # Summarize result
                    api_instruct = f"You are an assistant. Summarize the given {option} SQL query result. Summarization should be short."
                    nl_result = geminiCall(str(query_result), api_instruct)

                    # Display result
                    df = pd.DataFrame(query_result, columns=columns)
                    st.dataframe(df, use_container_width=True)
                    st.write(nl_result)

                except Exception as e:
                    st.error(f"Error executing query: {e}")

                finally:
                    conn.close() 

    else:
        st.warning(cnt.connection_fail)
        st.error(cnt.connect_failure)

