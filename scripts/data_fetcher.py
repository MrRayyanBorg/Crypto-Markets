# data_fetcher.py
import os
import requests
from datetime import datetime, timedelta
from fastapi import HTTPException
import json
from typing import List

# data_fetcher.py
import requests
from datetime import datetime, timedelta
from fastapi import HTTPException

def get_historical_prices(crypto_id: str, days: int):
    prices_data = []
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)

    # Ensure that timestamps are in seconds
    start_timestamp = int(start_date.timestamp())
    end_timestamp = int(end_date.timestamp())

    url = (
        f"https://api.coingecko.com/api/v3/coins/{crypto_id}/market_chart/range"
        f"?vs_currency=usd&from={start_timestamp}&to={end_timestamp}"
    )
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        prices_data = data.get('prices', [])
    except requests.RequestException as e:
        raise HTTPException(status_code=400, detail=f"Error fetching historical data for {crypto_id}: {str(e)}")
    except KeyError:
        raise HTTPException(status_code=500, detail=f"Unexpected response format for {crypto_id}")

    return prices_data


def save_prices_to_file(prices_data: List[List[float]], filename: str):
    # Ensure the data directory exists
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w') as f:
        json.dump(prices_data, f)

if __name__ == "__main__":
    crypto_ids = ["bitcoin", "ethereum"]
    days = 7

    # Get current date-time for the filename
    current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    
    for crypto_id in crypto_ids:
        prices_data = get_historical_prices(crypto_id, days)
        filename = f"data/{crypto_id}_prices_data_{days}days_{current_datetime}.json"
        save_prices_to_file(prices_data, filename)
        print(f"Prices data saved to {filename}")
