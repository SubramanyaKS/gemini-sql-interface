
def generate_instruction(option,schema_text):
    sql_instruct = f"""You are a {option} expert. Convert natural language questions into accurate, efficient {option} queries. Use standard SQL syntax. The table schema is provided: {schema_text}. Do not include DROP, DELETE, UPDATE, INSERT, or any data-modifying command."""
    return sql_instruct

def get_relevant_tables(question: str, schema: dict):
    question = question.lower()
    relevant = []
    for table in schema:
        if table in question or any(col in question for col in schema[table]):
            relevant.append(table)
    return relevant or list(schema.keys())