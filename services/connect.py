from sqlalchemy import create_engine


def get_connection(db_url):
    engine = create_engine(db_url)
    return engine.connect()

def get_placeholder(option):
    if option=="MySQL":
        return "mysql+pymysql://username:password@host:port/dbname"
    elif option=="PostgreSQL":
        return "postgresql+psycopg2://username:password@host:port/dbname"
    else:
        return "sqlite:///path/to/database.db"