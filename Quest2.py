import requests
import pandas as pd

# Define the API endpoint URL
api_endpoint = "https://api.kite.trade/instruments"

# Set the parameters for the API request
params = {
    "exchange": "NFO",
    "segment": "OPT"
}

# Make a GET request to the API endpoint and save the response content as an Excel file
response = requests.get(api_endpoint, params=params)
with open("instruments.xlsx", "wb") as f:
    f.write(response.content)

# Read the Excel file into a Pandas DataFrame
df = pd.read_excel("instruments.xlsx")

# Filter the DataFrame to include only the rows where the name is "NIFTY" and the expiry is "29-03-2023"
filtered_df = df[(df["name"] == "NIFTY") & (df["expiry"] == "2023-03-29")]

# Get the trading symbols as a list
trading_symbols = filtered_df["tradingsymbol"].tolist()

print(trading_symbols)
