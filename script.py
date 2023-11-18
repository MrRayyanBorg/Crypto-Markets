import requests
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

def get_historical_prices(crypto_ids, days):
    prices_data = {}
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)

    for crypto_id in crypto_ids:
        url = f"https://api.coingecko.com/api/v3/coins/{crypto_id}/market_chart/range?vs_currency=usd&from={start_date.timestamp()}&to={end_date.timestamp()}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            prices_data[crypto_id] = data['prices']
        except requests.RequestException as e:
            print(f"Error fetching historical data for {crypto_id}: {e}")

    return prices_data

def analyze_and_plot_data(prices_data, days):
    for crypto_id, prices in prices_data.items():
        if not prices:
            print(f"No data for analysis for {crypto_id}")
            continue

        dates = [datetime.fromtimestamp(price[0]/1000.0) for price in prices]
        values = [price[1] for price in prices]
        plt.plot(dates, values, label=crypto_id)

    plt.xlabel('Date')
    plt.ylabel('Price in USD')
    plt.title(f'Historical Prices for the Past {days} Days')
    plt.legend()
    plt.show()

def main():
    cryptos = ["bitcoin", "ethereum"]  # Add more cryptocurrency IDs as needed
    days = 30  # Number of days to look back
    historical_prices = get_historical_prices(cryptos, days)
    analyze_and_plot_data(historical_prices, days)

if __name__ == "__main__":
    main()
