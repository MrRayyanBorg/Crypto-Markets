import os
import glob
import matplotlib.pyplot as plt
from datetime import datetime
from io import BytesIO
import json
from typing import List

def load_prices_from_file(filename: str) -> List[List[float]]:
    with open(filename, 'r') as f:
        prices_data = json.load(f)
    return prices_data

def plot_data(crypto_id: str, prices_data: List[List[float]], days: int) -> BytesIO:
    plt.figure(figsize=(10, 6))

    dates = [datetime.fromtimestamp(price[0] / 1000.0) for price in prices_data]
    values = [price[1] for price in prices_data]
    plt.plot(dates, values, label=crypto_id)

    plt.xlabel('Date')
    plt.ylabel('Price in USD')
    plt.title(f'{crypto_id.capitalize()} Prices for the Past {days} Days')
    plt.legend()
    plt.grid(True)
    buf = BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    return buf

def get_latest_data_file(crypto_id: str, days: int) -> str:
    # Find all matching files for the given crypto_id and number of days
    data_files = glob.glob(f"data/{crypto_id}_prices_data_{days}days_*.json")
    
    # Return the most recent file based on the modification time
    if data_files:
        latest_file = max(data_files, key=os.path.getctime)
        return latest_file
    else:
        raise FileNotFoundError(f"No data files found for {crypto_id} with {days} days")

if __name__ == "__main__":
    days = 7
    crypto_ids = ["bitcoin", "ethereum"]
    
    # Get current date-time for the filename
    current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    for crypto_id in crypto_ids:
        try:
            # Get the latest data file for each crypto_id and number of days
            latest_file = get_latest_data_file(crypto_id, days)
            print(f"Using data file: {latest_file}")
            
            prices_data = load_prices_from_file(latest_file)
            plot_buf = plot_data(crypto_id, prices_data, days)
            
            # Ensure the plots directory exists
            os.makedirs("plots", exist_ok=True)
            
            # Save the plot with date-time and number of days in the filename
            plot_filename = f"plots/{crypto_id}_prices_plot_{days}days_{current_datetime}.png"
            with open(plot_filename, "wb") as f:
                f.write(plot_buf.getbuffer())

            print(f"Plot saved as {plot_filename}")

        except FileNotFoundError as e:
            print(e)
