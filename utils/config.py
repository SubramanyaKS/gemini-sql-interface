fetch_table="""
        SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' AND table_type = 'BASE TABLE';
    """
fetch_column="""
            SELECT column_name
            FROM information_schema.columns
            WHERE table_name = %s
            ORDER BY ordinal_position;
        """
supported_databases=["PostgreSQL","MySQL","SQLite"]