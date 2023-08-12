# Summary: This module contains helper functions used by the stock manager program.
# Author: Stephen Behr
# Date: 7/31/23

import matplotlib.pyplot as plt
from os import system, name

# Function to Clear the Screen
def clear_screen():
    if name == "nt": # User is running Windows
        _ = system('cls')
    else: # User is running Linux or Mac
        _ = system('clear')

# Function to sort the stock list (alphabetical)
def sortStocks(stock_list):
    stock_list.sort(key=lambda s: s.symbol)


# Function to sort the daily stock data (oldest to newest) for all stocks
def sortDailyData(stock_list):
    for stock in stock_list:
        stock.DataList.sort(key=lambda s: s.date)

def display_stock_chart(stock_list,found):
    date=[]
    price=[]
    company=''
    y=''
    for stock in stock_list:
        if stock.symbol == found.upper():
            company= stock.name
            for dailyData in stock.DataList:
                m=dailyData.date.month
                d=dailyData.date.day
                y=dailyData.date.year
                date.append(str(d))
                #date.append(dailyData.date)
                price.append(dailyData.close)
    plt.plot(date,price)
    string=m,y
    plt.xlabel(string)
    plt.ylabel('Price')
    plt.title(company)
    #plt.yscale() #passing ‘log’ # Will display using logarithmic scale. Remove if you want linear scale.
    plt.show()
    










