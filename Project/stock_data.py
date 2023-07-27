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
#from utilities import #clear_screen
from utilities import sortDailyData
from stock_class import Stock, DailyData

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
        print(stockDB,'exists')
    except:
        print(f'*!* {filename} could not be found')

# Get stock price history from web using Web Scraping
def retrieve_stock_web(dateStart,dateEnd,stock_list):
    #clear_screen()
    print("*** This Module Under Construction ***")
    _ = input("*** Press Enter to Continue ***")

# Get price and volume history from Yahoo! Finance using CSV import.
def import_stock_web_csv(stock_list,symbol,filename):
    #clear_screen()
    print("*** This Module Under Construction ***")
    _ = input("*** Press Enter to Continue ***")

def main():
    #clear_screen()
    print("This module will handle data storage and retrieval.")

if __name__ == "__main__":
    # execute only if run as a stand-alone script
    main()
