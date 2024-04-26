from fastapi import FastAPI, HTTPException
from datetime import datetime, timedelta
import requests
import matplotlib.pyplot as plt
from io import BytesIO
from fastapi.responses import StreamingResponse

app = FastAPI()

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
            raise HTTPException(status_code=400, detail=f"Error fetching historical data for {crypto_id}: {str(e)}")

    return prices_data

def plot_data(prices_data, days):
    plt.figure(figsize=(10, 6))
    for crypto_id, prices in prices_data.items():
        if not prices:
            continue
        dates = [datetime.fromtimestamp(price[0] / 1000.0) for price in prices]
        values = [price[1] for price in prices]
        plt.plot(dates, values, label=crypto_id)

    plt.xlabel('Date')
    plt.ylabel('Price in USD')
    plt.title(f'Historical Prices for the Past {days} Days')
    plt.legend()
    buf = BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    return buf

@app.get("/prices/{crypto_ids}/{days}")
async def historical_prices(crypto_ids: str, days: int):
    crypto_list = crypto_ids.split(',')
    prices_data = get_historical_prices(crypto_list, days)
    return prices_data

@app.get("/plot/{crypto_ids}/{days}")
async def plot_prices(crypto_ids: str, days: int):
    crypto_list = crypto_ids.split(',')
    prices_data = get_historical_prices(crypto_list, days)
    plot_buf = plot_data(prices_data, days)
    return StreamingResponse(plot_buf, media_type="image/png")

