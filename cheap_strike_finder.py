# -*- coding: utf-8 -*-
"""cheap_strike_finder.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/github/antrautw/TDIChallenge/blob/master/cheap_strike_finder.ipynb
"""

!pip install pandas_datareader
!pip install yfinance

"""# New Section"""

#Imports, keys here are pandas_datareader allows us to download easily and
#yfinance allows us to get into yahoo
import pandas_datareader.data as data
import yfinance as yf
import pandas as pd

yf.pdr_override()

def cheap_opts(symbol, calls_or_puts):
  '''
  This searches all possible expiry dates and finds contracts.
  '''
  import sys, os
  from datetime import date

  #We're going to suppress prints b/c datareader is annoying then restore printing so this helps
  #old_stdout = sys.stdout
  #sys.stdout = open(os.devnull, "w")

  finaldf = pd.DataFrame()
  ticker = yf.Ticker(symbol)
  stock_price = data.get_data_yahoo(symbol, end_date = date.today())['Close'][-1]
  for opt_date in ticker.options:
    opt = ticker.option_chain(opt_date)
    if calls_or_puts == 'puts':
      opt.puts.insert(0,'opt_date', opt_date)
      finaldf = finaldf.append(opt.puts)
    else:
      opt.calls.insert(0,'opt_date', opt_date)
      finaldf = finaldf.append(opt.calls)
  return finaldf, stock_price

# Commented out IPython magic to ensure Python compatibility.
# %%time
# 
# calls_or_puts = 'puts'
# symbol = 'zm'
# 
# results, stock_price = cheap_opts(symbol, calls_or_puts)

returned = results
# Do some final formatting changes
returned = returned.drop(columns = ['contractSymbol', 'lastTradeDate', 'contractSize', 'currency'])
if calls_or_puts == 'puts':
    returned.insert(3, 'dist OTM', stock_price - returned['strike'])
else:
    returned.insert(3, 'dist OTM', returned['strike'] - stock_price)
  
returned.insert(4, '% OTM', returned['dist OTM']/stock_price*100)
returned['value'] = returned['openInterest']*returned['lastPrice']*100

# Do some filtering
returned = returned[returned['% OTM'] < 35]
returned = returned[returned['lastPrice'] < 15]
#returned = returned[returned['volume'] > 10]
returned = returned[returned['opt_date'] > '2020-04-24']
#returned = returned[returned['percentChange'] < -0]

# Sort and display
returned.sort_values(inplace=True, by='lastPrice', ascending=True)
#returned = returned.head(30)
returned.reset_index(drop=True, inplace=True)
final = returned.style.set_precision(3).set_caption('<H1>' + symbol + ' ' + calls_or_puts.upper() + \
                                          '   (Current = $' + str(round(stock_price, 2)) + ')')
final

# Download the CSV and you're done!
from google.colab import files
filename = 'cheap_' + symbol + '_' + calls_or_puts + '.csv'

returned.to_csv(filename)
# returned.to_csv('unusual_calls_activity_5_15_exp.csv')
files.download(filename)

# Commented out IPython magic to ensure Python compatibility.
# %%time
# top = returned.sort_values(by='lastPrice', ascending=True) #.head(70)
# top.sort_values(by='% OTM', inplace=True, ascending=True)
# a = top.style.set_caption(calls_or_puts.upper())
# display(a)
# # top[top['inTheMoney']== True]

#top.to_csv('filtered_puts_05_15.csv')
top.to_csv('filtered_'+calls_or_puts+'_05_15.csv')

otm=returned['inTheMoney'] == False
#returned.loc[otm,'Distance OTM']=999-returned.lastPrice
returned.style.set_precision(2)

top[top['inTheMoney']== True]

