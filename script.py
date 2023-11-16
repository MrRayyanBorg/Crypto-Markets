import requests

def get_crypto_prices(crypto_ids):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={','.join(crypto_ids)}&vs_currencies=usd"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

def display_prices(prices):
    if prices:
        for crypto, data in prices.items():
            print(f"{crypto.capitalize()}: $ {data['usd']}")

def main():
    cryptos = ["bitcoin", "ethereum", "litecoin"]
    prices = get_crypto_prices(cryptos)
    display_prices(prices)

if __name__ == "__main__":
    main()
