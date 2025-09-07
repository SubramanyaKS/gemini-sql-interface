
from collections import defaultdict
from utils.config import fetch_table
from sqlalchemy import text


def extract_schema(connection):

    res=connection.execute(text(fetch_table))
    tables = res.fetchall()
    schema_dict = defaultdict()

    schema_lines = []
    for table_name, in tables:
        result=connection.execute(text("""
    SELECT column_name, data_type
    FROM information_schema.columns
    WHERE table_name = :table_name
    ORDER BY ordinal_position;
"""), {"table_name": table_name})
        columns = result.fetchall()
        col_str = ", ".join(col for col, _ in columns)
        schema_lines.append(f"-- {table_name}({col_str})")
        schema_dict[table_name]=[col for col, _ in columns]
    return schema_dict

def generate_schema_prompt(relevant_tables: list, schema: dict):
    schema_lines = []
    for table in relevant_tables:
        columns = schema[table]
        schema_lines.append(f" {table}({', '.join(columns)})")
    return "\n".join(schema_lines)
