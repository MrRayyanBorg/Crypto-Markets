import requests
from datetime import datetime, timedelta

def get_historical_prices(crypto_id, days):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    url = f"https://api.coingecko.com/api/v3/coins/{crypto_id}/market_chart/range?vs_currency=usd&from={start_date.timestamp()}&to={end_date.timestamp()}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data['prices']
    except requests.RequestException as e:
        print(f"Error fetching historical data: {e}")
        return None

def analyze_historical_data(prices):
    # Assuming 'prices' is a list of [timestamp, price]
    if not prices:
        return "No data for analysis"

    total_price = sum(price[1] for price in prices)
    average_price = total_price / len(prices)
    return f"Average Price: ${average_price:.2f}"

def main():
    crypto = "bitcoin"
    days = 30  # Number of days to look back
    historical_prices = get_historical_prices(crypto, days)
    analysis_result = analyze_historical_data(historical_prices)
    
    print(f"Historical Data Analysis for {crypto.capitalize()} for the past {days} days:")
    print(analysis_result)

if __name__ == "__main__":
    main()
