import requests
import mysql.connector
from datetime import datetime

# API Configuration
API_KEY = "your_api_key_here"
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
    db = mysql.connector.connect(
        host="localhost",
        user="your_user",
        password="your_password",
        database="crypto_data"
    )
    cursor = db.cursor()
    sql = """
    INSERT INTO crypto_current (
        symbol, name, price_usd, market_cap_usd, volume_24h, record_date
    )
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    for crypto in data["data"]:
        symbol = crypto["symbol"]
        name = crypto["name"]
        price_usd = crypto["quote"]["USD"]["price"]
        market_cap_usd = crypto["quote"]["USD"]["market_cap"]
        volume_24h = crypto["quote"]["USD"]["volume_24h"]
        record_date = datetime.utcnow()
        values = (symbol, name, price_usd, market_cap_usd, volume_24h, record_date)
        cursor.execute(sql, values)

    db.commit()
    cursor.close()
    db.close()

# Main Execution
data = fetch_latest_data()

if "data" in data:
    save_to_database(data)
    print("Data saved successfully!")
else:
    print("Error or no data:", data)
