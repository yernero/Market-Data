import requests
import psycopg2
from psycopg2 import sql
from datetime import datetime

# API Configuration
API_KEY = "2f39afc6-3cfc-4fda-88bc-b6d72174f947"
BASE_URL = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
HEADERS = {
    "Accepts": "application/json",
    "X-CMC_PRO_API_KEY": API_KEY
}

# Fetch Current Data
def fetch_latest_data():
    params = {
        "start": "1",     # Start rank
        "limit": "100",   # Fetch top 100 cryptocurrencies
        "convert": "USD"  # Convert prices to USD
    }
    response = requests.get(BASE_URL, headers=HEADERS, params=params)
    return response.json()

# Save Data to Database
def save_to_database(data):
    db = None
    cursor = None
    try:
        # Connect to PostgreSQL
        db = psycopg2.connect(
            host="localhost",          # Replace with your PostgreSQL host
            port=5433,                 # Default PostgreSQL port
            user="postgres",           # Replace with your PostgreSQL username
            password="Duck-pi3",       # Replace with your PostgreSQL password
            dbname="postgres"    # Replace with your PostgreSQL database name
        )
        cursor = db.cursor()

        # Define SQL query
        sql_query = """
        INSERT INTO crypto_current (
            symbol, name, price_usd, market_cap_usd, volume_24h, record_date
        )
        VALUES (%s, %s, %s, %s, %s, %s)
        """

        # Insert data into PostgreSQL table
        for crypto in data["data"]:
            symbol = crypto["symbol"]
            name = crypto["name"]
            price_usd = crypto["quote"]["USD"]["price"]
            market_cap_usd = crypto["quote"]["USD"]["market_cap"]
            volume_24h = crypto["quote"]["USD"]["volume_24h"]
            record_date = datetime.utcnow()
            values = (symbol, name, price_usd, market_cap_usd, volume_24h, record_date)
            cursor.execute(sql_query, values)

        # Commit changes
        db.commit()
        print(f"{cursor.rowcount} rows inserted into the database.")
    except psycopg2.Error as e:
        print(f"Database error: {e}")
    finally:
        if cursor is not None:
            cursor.close()
        if db is not None:
            db.close()

# Main Execution
data = fetch_latest_data()

if "data" in data:
    save_to_database(data)
    print("Data saved successfully!")
else:
    print("Error or no data:", data)
    
    
    
