import psycopg2
from urllib.parse import urlparse
def get_connection(db_url):
    result = urlparse(db_url)
    dbname = result.path[1:]  # Remove leading '/'
    user = result.username
    password = result.password
    host = result.hostname
    port = result.port
    try:
        return psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )
    except Exception as e:
        print(f"Error: {e}")
        return False


