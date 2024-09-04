# Cryptocurrency Price Tracker

This program is designed to track cryptocurrency prices in real-time, making it both interesting and practical for those who want to monitor the market. The program fetches the latest prices of various cryptocurrencies like Bitcoin and Ethereum, and displays them in a user-friendly format.

## Key Features

1. **API Selection**:
   - We’ll use a reliable public API, such as [CoinGecko](https://www.coingecko.com/en/api) or [CryptoCompare](https://min-api.cryptocompare.com/), to fetch real-time cryptocurrency prices.
   - These APIs provide extensive data and are commonly used in the industry.

2. **Python Libraries**:
   - **`requests`**: To make API calls and retrieve data.
   - **`pandas` (optional)**: For data manipulation and organization, especially if expanding to handle historical data or more complex datasets.
   - **`json`**: To parse and handle the API response data.

3. **Fetching Data**:
   - The script will connect to the selected API and request real-time data for Bitcoin and Ethereum.
   - It can be customized to fetch prices for additional cryptocurrencies if needed.
   - The data fetched includes the current price in USD, and it could be extended to include other currencies or additional information like 24-hour price changes, market cap, etc.

4. **Displaying Data**:
   - The program will display the fetched data in a readable format in the console.
   - The display could be something simple like:
     ```
     Bitcoin: $39856.23
     Ethereum: $2795.42
     ```
   - Future expansions could include:
     - **Graphical User Interface (GUI)**: Using libraries like `tkinter` or `PyQt` for a desktop application.
     - **Web Application**: Using `Flask` or `Django` to display the data on a webpage.
     - **Data Logging**: Saving the data to a file or database for tracking historical prices.

## Getting Started

### Prerequisites

1. **Install Python** (if not already installed):
   - Download and install Python from [python.org](https://www.python.org/).

2. **Install Required Python Libraries**:
   - Use `pip` to install the necessary libraries:
     ```bash
     pip install requests pandas
     ```

### Example Script

Here’s a basic example of what the script might look like:

```python
import requests

# Function to fetch cryptocurrency prices
def fetch_crypto_prices(cryptos):
    api_url = "https://api.coingecko.com/api/v3/simple/price"
    try:
        response = requests.get(api_url, params={
            'ids': ','.join(cryptos),
            'vs_currencies': 'usd'
        })
        response.raise_for_status()  # Raise an error for bad status codes
        prices = response.json()
        return prices
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

# List of cryptocurrencies to track
cryptos = ["bitcoin", "ethereum"]

# Fetch and display prices
prices = fetch_crypto_prices(cryptos)
if prices:
    for crypto in cryptos:
        price = prices.get(crypto, {}).get('usd', 'N/A')
        print(f"{crypto.capitalize()}: ${price:.2f}")

### Example Output

When you run the script, the output might look like this:

```Bitcoin: $39856.23 Ethereum: $2795.42```



## Expanding the Program

1. **Real-Time Updates**:
   - Implement a loop with a delay to continuously fetch and update prices every few seconds.
   - You can use the `time.sleep()` function in Python to create a delay between updates.

2. **Error Handling**:
   - Enhance the script to handle network errors or API downtime gracefully, perhaps retrying the request after a short delay.
   - You can implement retries with exponential backoff or simply alert the user if the API is unreachable.

3. **Logging and Analysis**:
   - Log the data to a file or database for future analysis or visualization.
   - Use `pandas` to handle historical data and create plots of price trends over time.

4. **Advanced Features**:
   - **Alerts**: Set up alerts for when a cryptocurrency's price crosses a certain threshold. This could be done using email notifications, desktop notifications, or even SMS alerts.
   - **Portfolio Tracker**: Expand the script to track and manage a cryptocurrency portfolio, showing total value based on current prices.
   - **Currency Conversion**: Allow users to see prices in different currencies (e.g., EUR, GBP) by modifying the API request to include multiple `vs_currencies`.

## Future Plans

- **GUI Development**: Build a graphical user interface using `tkinter` or `PyQt` for easier interaction with the program.
- **Web Application**: Develop a web-based application using `Flask` or `Django` to make the tool accessible from anywhere.
- **Mobile Application**: Consider creating a mobile version of the tracker using frameworks like `Kivy` or React Native.

## Contributing

If you would like to contribute to this project, please feel free to fork the repository and submit a pull request. Contributions are welcome and appreciated.
