import yfinance as yf
import matplotlib.pyplot as plt

# Step 1: Download stock data
ticker_symbol = "AAPL"  # <- You can change this to any stock symbol
company = yf.Ticker(ticker_symbol)

# Step 2: Get historical market data
history = company.history(period="1y")  # or "6mo", "5d", "max", etc.

# Step 3: Plot closing prices
plt.figure(figsize=(12, 6))
plt.plot(history.index, history['Close'], label='Closing Price', color='blue', linewidth=2)

# Step 4: Customize the plot
plt.title(f"{ticker_symbol} Stock Price - Last 1 Year", fontsize=18)
plt.xlabel("Date", fontsize=14)
plt.ylabel("Price (USD)", fontsize=14)
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend()
plt.tight_layout()

# Step 5: Save the plot to a file (PNG, PDF, etc.)
output_file = "stock_price_chart.png"  # Change the name and file format if needed
plt.savefig(output_file, format='png')  # Saves the chart as a PNG file

# Step 6: Show the plot (optional)
plt.show()

# Print confirmation
print(f"Chart saved as {output_file}")
