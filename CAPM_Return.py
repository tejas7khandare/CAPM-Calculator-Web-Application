# importing libraries

import streamlit as st
import pandas as pd
import yfinance as yf
import datetime
import pandas_datareader.data as web

st.set_page_config(page_title = 'CAPM',
                   page_icon = 'chart_with_upwards_trend',
                   layout = 'wide')

st.title("Capital Asset Pricing Model")

# getting input from user

col1, col2 = st.columns([1,1])
with col1:
  stocks_list = st.multiselect("Choose 4 stocks", ('TSLA','AAPL','NFLX','MSFT','META','AMZN',
                                   'NVDA','GOOGL','NKE','WMT','GS','ORCL'))
with col2:
  year = st.number_input("Number of years",1,10)

# downloading data for SP500

end = datetime.date.today()
start = datetime.date(datetime.date.today().year-year, datetime.date.today().month, datetime.date.today().day)
SP500 = web.DataReader(['sp500'],'fred',start,end)

stocks_df = pd.DataFrame()

for stock in stocks_list:
  data = yf.download(stock, period = f'{year}y')
  stocks_df[f'{stock}'] = data['Close']

stocks_df.reset_index(inplace = True)
SP500.reset_index(inplace = True)
SP500.columns = ['Date','sp500']
stocks_df['Date'] = stocks_df['Date'].astype('datetime64[ns]')
stocks_df['Date'] = stocks_df['Date'].apply(lambda x:str(x)[:10])
stocks_df['Date'] = pd.to_datetime(stocks_df['Date'])
stocks_df = pd.merge(stocks_df, SP500, on='Date', how='inner')
print(stocks_df)

col1, col2 = st.columns([1,1])
with col1:
  st.markdown("### Dateframe head")
  st.dataframe(stocks_df.head(), use_container_width= True)
with col2:
  st.markdown("### Dateframe tail")
  st.dataframe(stocks_df.head(), use_container_width= True)