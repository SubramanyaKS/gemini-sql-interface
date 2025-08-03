
from utils.config import fetch_table

def extract_schema(connection):
    cursor = connection.cursor()

    cursor.execute(fetch_table)
    tables = cursor.fetchall()

    schema_lines = []
    for table_name, in tables:
        cursor.execute(f"""
            SELECT column_name, data_type
            FROM information_schema.columns
            WHERE table_name = %s
            ORDER BY ordinal_position;
        """, (table_name,))
        columns = cursor.fetchall()
        col_str = ", ".join(col for col, _ in columns)
        schema_lines.append(f"-- {table_name}({col_str})")

    return "\n".join(schema_lines)