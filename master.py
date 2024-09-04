import os
from scripts.data_fetcher import get_historical_prices, save_prices_to_file
from scripts.plotter import get_latest_data_file, load_prices_from_file, plot_data
from datetime import datetime

def main():
    print("Welcome to the Crypto Data Manager!")
    
    while True:
        print("\nWhat would you like to do?")
        print("1. Extract data")
        print("2. Plot data")
        print("3. Extract data and plot it")
        print("4. Exit")
        
        choice = input("Enter your choice (1-4): ")
        
        if choice == '4':
            print("Exiting the program. Goodbye!")
            break

        crypto_id = input("Enter the cryptocurrency (e.g., 'bitcoin', 'ethereum'): ").lower()
        days = int(input("Enter the number of days for historical data: "))

        if choice in ['1', '3']:
            # Extract data
            print(f"Extracting data for {crypto_id} for the past {days} days...")
            prices_data = get_historical_prices(crypto_id, days)
            
            # Generate filename with date-time
            current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"data/{crypto_id}_prices_data_{current_datetime}.json"
            save_prices_to_file(prices_data, filename)
            
            print(f"Data saved to {filename}")
            
            if choice == '1':
                continue

        if choice in ['2', '3']:
            # Plot data
            try:
                if choice == '2':
                    # If plotting only, find the most recent file
                    filename = get_latest_data_file(crypto_id)
                
                print(f"Plotting data from {filename}...")
                prices_data = load_prices_from_file(filename)
                plot_buf = plot_data(crypto_id, prices_data, days)
                
                # Ensure the plots directory exists
                os.makedirs("plots", exist_ok=True)
                
                # Save the plot with date-time in the filename
                current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                plot_filename = f"plots/{crypto_id}_prices_plot_{current_datetime}.png"
                with open(plot_filename, "wb") as f:
                    f.write(plot_buf.getbuffer())
                
                print(f"Plot saved as {plot_filename}")
            
            except FileNotFoundError as e:
                print(e)
                continue

if __name__ == "__main__":
    main()
