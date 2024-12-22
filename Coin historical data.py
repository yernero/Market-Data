import requests
import pandas as pd

# CoinMarketCap API URL
url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"

# Your API key
api_key = "2f39afc6-3cfc-4fda-88bc-b6d72174f947"  # Replace with your CoinMarketCap API key

# Parameters for the API request
parameters = {
    "start": "1",         # Start at the top of the list
    "limit": "10",        # Number of cryptocurrencies to fetch
    "convert": "USD"      # Convert prices to USD
}

# Headers for the API request
headers = {
    "Accepts": "application/json",
    "X-CMC_PRO_API_KEY": api_key
}

# Fetch data from the API
response = requests.get(url, headers=headers, params=parameters)

# Check if the request was successful
if response.status_code == 200:
    data = response.json()["data"]
    
    # Create a pandas DataFrame
    crypto_data = pd.DataFrame([{
        "Name": item["name"],
        "Symbol": item["symbol"],
        "Price (USD)": item["quote"]["USD"]["price"],
        "Market Cap (USD)": item["quote"]["USD"]["market_cap"],
        "Volume (24h)": item["quote"]["USD"]["volume_24h"],
        "Change (24h %)": item["quote"]["USD"]["percent_change_24h"]
    } for item in data])
    
    # Save the data to a CSV file
    crypto_data.to_csv("crypto_data.csv", index=False)
    print("Data saved to crypto_data.csv")
else:
    print(f"Failed to fetch data. HTTP Status Code: {response.status_code}")
