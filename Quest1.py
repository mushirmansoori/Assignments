import pandas as pd
import requests
import matplotlib.pyplot as plt

# Define the stock symbols to fetch data for
stock_list = ['SBIN', 'ASIANPAINT', 'AXISBANK']

# Define the URL to fetch stock data from
url = f'https://api.nsepy.xyz/api/get_history?symbol={{}}&series=EQ&from=2015-01-01&to=2015-01-09'

# Fetch data for each stock and combine into a single DataFrame
df_list = []
for stock in stock_list:
    response = requests.get(url.format(stock))
    data = response.json()['data']
    df = pd.DataFrame(data)
    df = df[['Date', 'Close']]
    df.rename(columns={'Close': f'{stock}_close'}, inplace=True)
    df_list.append(df)
table_value = pd.concat(df_list, axis=1)

# Plot the stock data
table_value.set_index('Date').plot()
plt.show()
