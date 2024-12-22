import psycopg2

try:
    db = psycopg2.connect(
        host="localhost",
        port=5433,
        user="postgres",
        password="Duck-pi3",
        dbname="postgres"
    )
    print("Connection successful!")
    db.close()
except psycopg2.Error as e:
    print(f"Connection failed: {e}")

