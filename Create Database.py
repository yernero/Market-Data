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

# SQL queries to create tables
create_tables_queries = [
    """
    CREATE TABLE crypto_current (
        id SERIAL PRIMARY KEY,
        symbol VARCHAR(10) NOT NULL UNIQUE,  -- Adding UNIQUE constraint here
        name VARCHAR(50) NOT NULL,
        price_usd NUMERIC(20, 6) NOT NULL,
        market_cap_usd NUMERIC(30, 2) NOT NULL,
        volume_24h NUMERIC(30, 2) NOT NULL,
        record_date TIMESTAMP NOT NULL
    );
    """,
    """
    CREATE TABLE crypto_history (
        id SERIAL PRIMARY KEY,
        crypto_current_id INT NOT NULL,
        price_usd NUMERIC(20, 6) NOT NULL,
        market_cap_usd NUMERIC(30, 2) NOT NULL,
        volume_24h NUMERIC(30, 2) NOT NULL,
        record_date TIMESTAMP NOT NULL,
        FOREIGN KEY (crypto_current_id) REFERENCES crypto_current(id)
    );
    """,
    """
    CREATE TABLE crypto_market (
        id SERIAL PRIMARY KEY,
        crypto_current_id INT NOT NULL,
        market_name VARCHAR(100) NOT NULL,
        market_pair VARCHAR(20) NOT NULL,  -- e.g., "BTC/USD"
        price_usd NUMERIC(20, 6) NOT NULL,
        volume_24h NUMERIC(30, 2) NOT NULL,
        record_date TIMESTAMP NOT NULL,
        FOREIGN KEY (crypto_current_id) REFERENCES crypto_current(id)
    );
    """,
    """
    CREATE TABLE crypto_wallets (
        id SERIAL PRIMARY KEY,
        user_id INT NOT NULL,  -- Assuming you have a user table elsewhere
        crypto_current_id INT NOT NULL,
        wallet_address VARCHAR(100) NOT NULL,
        balance NUMERIC(20, 6) NOT NULL,
        record_date TIMESTAMP NOT NULL,
        FOREIGN KEY (crypto_current_id) REFERENCES crypto_current(id)
    );
    """
]

# Create a connection to the PostgreSQL server and create the new database
try:
    # Step 1: Create the new database
    conn = psycopg2.connect(host=host, port=port, user=user, password=password, dbname=dbname)
    conn.autocommit = True  # Enable autocommit to create a new database outside a transaction

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

    # Execute the query to create the new database
    cursor.execute(create_db_query)
    print(f"Database '{new_dbname}' created successfully.")

    # Close the current connection to switch to the new database
    cursor.close()
    conn.close()

    # Step 2: Reconnect to the newly created database to create tables
    conn = psycopg2.connect(host=host, port=port, user=user, password=password, dbname=new_dbname)
    cursor = conn.cursor()

    # Execute the table creation queries and commit after each
    for query in create_tables_queries:
        try:
            cursor.execute(query)
            conn.commit()  # Explicit commit after each table creation
            print("Table created successfully.")
        except Exception as e:
            print(f"Error occurred while creating table: {e}")
            conn.rollback()  # Rollback the transaction if there is an error

    # Step 3: Validate the creation of tables by querying the information schema
    cursor.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public';
    """)
    tables = cursor.fetchall()
    if tables:
        print("Tables in the 'public' schema:")
        for table in tables:
            print(f"- {table[0]}")
    else:
        print("No tables found in the 'public' schema.")

except Exception as e:
    print(f"Error occurred: {e}")

finally:
    # Close the connection
    if cursor:
        cursor.close()
    if conn:
        conn.close()
