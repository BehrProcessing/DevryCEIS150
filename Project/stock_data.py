# Summary: This module contains the functions used by both console and GUI programs to manage stock data.
# Author: 
# Date: 

import sqlite3
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import re
import pandas as pd
import os
import csv
import time
from datetime import datetime
from utilities import clear_screen
from utilities import sortDailyData
from stock_class import Stock, DailyData
import stock_console_1 as SC
# Create the SQLite database
def create_database(stockDB="stocks.db"):
    try:
        conn = sqlite3.connect(stockDB)
        cur = conn.cursor()
        createStockTableCmd = """CREATE TABLE IF NOT EXISTS stocks (
                                symbol TEXT NOT NULL PRIMARY KEY,
                                name TEXT,
                                shares REAL
                            );"""
        createDailyDataTableCmd = """CREATE TABLE IF NOT EXISTS dailyData (
                                    symbol TEXT NOT NULL,
                                    date TEXT NOT NULL,
                                    price REAL NOT NULL,
                                    volume REAL NOT NULL,
                                    PRIMARY KEY (symbol, date)
                            );"""   
        cur.execute(createStockTableCmd)
        cur.execute(createDailyDataTableCmd)
        print(f'Created a new Database {stockDB}')
        _=input('...')
        return True
    except:
        print(stockDB,'could not be created, please do not use special characters in your filename')
        _=input('...')
        return False

# Save stocks and daily data into database
def save_stock_data(stock_list):
    #clear_screen()
    stockDB = "stocks.db"
    filename=''
    if __name__=='main' or __name__=='stock_console':
        print(f'Press enter to overwrite {stockDB}, or Enter a filename to create or save to a different database')
        filename=input()
    #excludedCharacters=['!','@','#','$','%','^','&',]

    if filename:
        stockDB = filename+'.db'
        created=create_database(stockDB)
    else:
        stockDB = "stocks.db"
    try:
        conn = sqlite3.connect(stockDB)
        cur = conn.cursor()
        insertStockCmd = """INSERT INTO stocks
                                (symbol, name, shares)
                                VALUES
                                (?, ?, ?); """
        insertDailyDataCmd = """INSERT INTO dailyData
                                        (symbol, date, price, volume)
                                        VALUES
                                        (?, ?, ?, ?);"""
        for stock in stock_list:
            insertValues = (stock.symbol, stock.name, stock.shares)
            try:
                cur.execute(insertStockCmd, insertValues)
                cur.execute("COMMIT;")
            except:
                pass
            for daily_data in stock.DataList: 
                insertValues = (stock.symbol,daily_data.date.strftime("%m/%d/%y"),daily_data.close,daily_data.volume)
                try:
                    cur.execute(insertDailyDataCmd, insertValues)
                    cur.execute("COMMIT;")
                except:
                    pass
        print(f'Saved data as {stockDB}')
    except:
        print(f'*!* Save Failed for {filename}')
    
# Load stocks and daily data from database
def load_stock_data(stock_list,stockDB = "stocks.db"):
    stock_list.clear()
    filename=''
    if __name__=='main'or __name__=='stock_console':
        print(f'Press enter to load {stockDB}, or Enter the filename of another .db file ')
        filename=input()
    if filename:
        stockDB = filename+'.db'
    else:
        stockDB = "stocks.db"
    try:
        conn = sqlite3.connect(stockDB)
        stockCur = conn.cursor()
        stockSelectCmd = """SELECT symbol, name, shares
                        FROM stocks; """
        stockCur.execute(stockSelectCmd)
        stockRows = stockCur.fetchall()
        for row in stockRows:
            new_stock = Stock(row[0],row[1],row[2])
            dailyDataCur = conn.cursor()
            dailyDataCmd = """SELECT date, price, volume
                            FROM dailyData
                            WHERE symbol=?; """
            selectValue = (new_stock.symbol)
            dailyDataCur.execute(dailyDataCmd,(selectValue,))
            dailyDataRows = dailyDataCur.fetchall()
            for dailyRow in dailyDataRows:
                daily_data = DailyData(datetime.strptime(dailyRow[0],"%m/%d/%y"),float(dailyRow[1]),float(dailyRow[2]))
                new_stock.add_data(daily_data)
            stock_list.append(new_stock)
        sortDailyData(stock_list)
        print(stockDB,'Exists, Loading...')
    except:
        print(f'*!* {filename} could not be found')

# Get stock price history from web using Web Scraping
def retrieve_stock_web(dateStart,dateEnd,stock_list):
    #clear_screen()
    dateFrom = str(int(time.mktime(time.strptime(dateStart,"%m/%d/%y"))))
    dateTo = str(int(time.mktime(time.strptime(dateEnd,"%m/%d/%y"))))
    recordCount = 0
    for stock in stock_list:
        stockSymbol = stock.symbol
        url = "https://finance.yahoo.com/quote/"+stockSymbol+"/history?period1="+dateFrom+"&period2="+dateTo+"&interval=1d&filter=history&frequency=1d"
        # Note this code assumes the use of the Chrome browser.
        # You will have to modify if you are using a different browser.
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches',['enable-logging'])
        options.add_experimental_option("prefs",{'profile.managed_default_content_settings.javascript': 2})
        try:
            driver = webdriver.Chrome(options=options)
            driver.implicitly_wait(60)
            driver.get(url)
        except:
            raise RuntimeWarning("Chrome Driver Not Found")
    
        soup = BeautifulSoup(driver.page_source,"html.parser")
        row = soup.find('table',class_="W(100%) M(0)")
        dataRows = soup.find_all('tr')
        for row in dataRows:
            td = row.find_all('td')
            rowList = [i.text for i in td]
            columnCount = len(rowList)
            if columnCount == 7: # This row is a standard data row (otherwise it's a special case such as dividend which will be ignored)
                daily_data = DailyData(datetime.strptime(rowList[0],"%b %d, %Y"),float(rowList[5].replace(',','')),float(rowList[6].replace(',','')))
                stock.add_data(daily_data)
                recordCount += 1
    return recordCount

# Get price and volume history from Yahoo! Finance using CSV import.
def import_stock_web_csv(symbol,File):
    pass
    # with open(File,newline='') as stockData:
    #     Datareader =csv.reader(stockData, delimiter=',')
    #     next(Datareader)
    #     for row in Datareader:
    #         print(type(row[0]))
    #         print(row[0])
    #         Split=row[0].split('-')
    #         Split=Split[1]+'/'+Split[2]+'/'+Split[0]
    #         obj=datetime.strptime(Split,"%m/%d/%Y")
    #         dailyData=DailyData(obj,float(row[4]),float(row[6]))
    #         symbol.add_data(dailyData)     
            
    # dailyData=DailyData(datetime.strptime(row[0],"%m%d/%y"),float(row[4]),float(row[6]))
    # symbol.add_data(dailyData)

def main():
    #clear_screen()
    print("This module will handle data storage and retrieval.")

if __name__ == "__main__":
    # execute only if run as a stand-alone script
    main()
