import psycopg2
from psycopg2 import sql

# Connection information
host = 'localhost'
port = '5433'
user = 'postgres'
password = 'Duck-pi3'
dbname = 'postgres'  # Default database to connect to for creating a new one

# New database configuration
new_dbname = 'crypto_data'  # The new database name (lowercase with underscores)
encoding = 'UTF8'
template = 'template1'  # Default template to use when creating a new database

# Create a connection to the PostgreSQL server
try:
    conn = psycopg2.connect(host=host, port=port, user=user, password=password, dbname=dbname)
    conn.autocommit = True  # Enable autocommit to create a new database outside a transaction

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    # Construct the SQL query to create the new database
    create_db_query = sql.SQL("""
        CREATE DATABASE {dbname}
        WITH ENCODING = {encoding}
        TEMPLATE = {template}
        OWNER = {owner};
    """).format(
        dbname=sql.Identifier(new_dbname),
        encoding=sql.Identifier(encoding),
        template=sql.Identifier(template),
        owner=sql.Identifier(user)  # Owner of the new database
    )

    # Execute the query
    cursor.execute(create_db_query)
    print(f"Database '{new_dbname}' created successfully.")

except Exception as e:
    print(f"Error occurred: {e}")

finally:
    # Close the connection
    if cursor:
        cursor.close()
    if conn:
        conn.close()
