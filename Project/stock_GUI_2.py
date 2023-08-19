# Summary: This module contains the user interface and logic for a graphical user interface version of the stock manager program.
# Author: 
# Date: 

from datetime import datetime
from os import path
from tkinter import *
from tkinter import ttk
from tkinter import messagebox, simpledialog, filedialog
import stock_console as SC
import csv
import stock_data
from stock_class import Stock, DailyData
from utilities import clear_screen, display_stock_chart, sortStocks, sortDailyData

class StockApp:
    def __init__(self):
        self.stock_list = []
        #check for database, create if not exists
        if path.exists("stocks.db") == False:
            stock_data.create_database()

 # This section creates the user interface

        # Create Window
        self.root = Tk()
        self.root.title("Behr Processing Stock Portfolio") #Replace with a suitable name for your program
        #self.root.geometry("600x600")
        # Add Menubar
        self.menubar = Menu(self.root)

        # Add File Menu
        self.filemenu = Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label = "Load Data",command = self.load)
        self.filemenu.add_command(label = "Save Data",command = self.save)
        self.filemenu.add_command(label = "Test Data",command = self.test)
        # self.filemenu.add_separator()
        # self.filemenu.add_command(label="Exit",command = self.root.quit)
        self.menubar.add_cascade(label="File",menu=self.filemenu)

        # Add Web Menu 
        self.webmenu = Menu(self.menubar, tearoff=0)
        self.webmenu.add_command(label = "Scrape Data from Yahoo! Finance...", command=self.scrape_web_data)
        self.webmenu.add_command(label = "Import CSV from Yahoo! Finance...", command=self.importCSV_web_data)
        self.menubar.add_cascade(label="Web",menu=self.webmenu)

        # Add Chart Menu
        self.chartmenu = Menu(self.menubar,tearoff=0)
        self.chartmenu.add_command(label="Display Stock Chart", command=self.display_chart)
        self.menubar.add_cascade(label="Chart",menu=self.chartmenu)

        # Add menus to window       
        self.root.config(menu=self.menubar)

        # Add heading information
        self.headingLabel = Label(self.root,text="No Stock Selected")
        self.headingLabel.grid(column=0,row=0,columnspan=3,padx = 5, pady = 10)
        

        # Add stock list
        self.stockLabel = Label(self.root,text="Stocks")
        self.stockLabel.grid(column=0,row=1,padx = 5, pady = 0,sticky=(N))

        self.stockList = Listbox(self.root)
        self.stockList.grid(column=0,row=2,padx = 5, pady = 0,sticky=(N,S))
        self.stockList.bind('<<ListboxSelect>>',self.update_data)
        
        
        # Add Tabs
        self.notebook = ttk.Notebook(self.root,padding="5 5 5 5")
        self.notebook.grid(column=2,row=2,sticky=(N,W,S))
        
        self.mainFrame = ttk.Frame(self.notebook)
        self.stockDataFrame = ttk.Frame(self.notebook)
        self.reportFrame = ttk.Frame(self.notebook)
        self.notebook.add(self.mainFrame,text='Manage')
        self.notebook.add(self.stockDataFrame,text='History')
        self.notebook.add(self.reportFrame,text = 'Report')

        # Set Up Main Tab
        self.addStockGroup = LabelFrame(self.mainFrame,text="Add Stock",padx=5,pady=5)
        self.addStockGroup.grid(column=0,row=0,padx=5,pady=0,sticky=(W,E))

        self.addSymbolLabel = Label(self.addStockGroup,text = "Symbol")
        self.addSymbolLabel.grid(column=0,row=0,padx = 5, pady = 5,sticky=(W))
        self.addSymbolEntry = Entry(self.addStockGroup)
        self.addSymbolEntry.grid(column=1,row=0,padx=5,pady=5)

        self.addNameLabel = Label(self.addStockGroup,text = "Name")
        self.addNameLabel.grid(column=0,row=1,padx = 5, pady = 5,sticky=(W))
        self.addNameEntry = Entry(self.addStockGroup)
        self.addNameEntry.grid(column=1,row=1,padx=5,pady=5)

        self.addSharesLabel = Label(self.addStockGroup,text = "Shares")
        self.addSharesLabel.grid(column=0,row=2,padx = 5, pady = 5,sticky=(W))
        self.addSharesEntry = Entry(self.addStockGroup)
        self.addSharesEntry.grid(column=1,row=2,padx=5,pady=5)

        self.addStockButton = Button(self.addStockGroup,text = "New Stock",command=self.add_stock)
        self.addStockButton.grid(column=0,row=3,columnspan = 2, padx = 5, pady = 5)

        self.transactionGroup = LabelFrame(self.mainFrame,text="Update Shares",padx=5,pady=5)
        self.transactionGroup.grid(column=0,row=1,padx=5,pady=5,sticky=(W,E))
        self.updateSharesLabel = Label(self.transactionGroup,text = "Shares")
        self.updateSharesLabel.grid(column=0,row=0,padx = 5, pady = 5,sticky=(W))
        self.updateSharesEntry = Entry(self.transactionGroup)
        self.updateSharesEntry.grid(column=1,row=0,columnspan=2, padx=5,pady=5)

        self.buyStockButton = Button(self.transactionGroup,text = "Buy Selected Stock",command=self.buy_shares)
        self.buyStockButton.grid(column=1,row=1, padx = 5, pady = 5)
        self.sellStockButton = Button(self.transactionGroup,text = "Sell Selected Stock",command=self.sell_shares)
        self.sellStockButton.grid(column=2,row=1, padx = 5, pady = 5)

        self.deleteGroup = LabelFrame(self.mainFrame,text="Delete Stock",padx=5,pady=5)
        self.deleteGroup.grid(column=0,row=2,padx=5,pady=5,sticky=(W,E))

        self.deleteStockButton = Button(self.deleteGroup,text="Delete Selected Stock",command=self.delete_stock)
        self.deleteStockButton.grid(column=0,row=0,padx=5,pady=5)


        # Setup History Tab
        self.dailyDataList = Text(self.stockDataFrame,width=50)
        self.dailyDataList.grid(column=0,row=0,ipady=0,padx = 5, pady = 5)
        
        
        # Setup Report Tab
        self.stockReport = Text(self.reportFrame,width=50)
        self.stockReport.grid(column=0,row=0,padx=5,pady=5)

        self.root.mainloop()

# This section provides the functionality

#Testing sizes       
    # Load stocks and history from database.
    def load(self):
        self.stockList.delete(0,END)
        stock_data.load_stock_data(self.stock_list)
        sortStocks(self.stock_list) 
        for stock in (self.stock_list):
        	self.stockList.insert(END,stock.symbol)
        messagebox.showinfo("Load Data","Data Loaded")
    # Save stocks and history to database.
    def save(self):
        stock_data.save_stock_data(self.stock_list)
    def test(self):
        import stock_console
        stock_console.create_test(self.stock_list)
        for stock in self.stock_list:
        	self.stockList.insert(END,stock.symbol)
        messagebox.showinfo("Load Data","Data Loaded")
    # Refresh history and report tabs
    def update_data(self, evt):
        self.display_stock_data()

    # Display stock price and volume history.
    def display_stock_data(self):
        symbol = self.stockList.get(self.stockList.curselection())
        x=47
        for stock in self.stock_list:
            if stock.symbol == symbol:
                self.headingLabel['text'] = stock.name + " - " + str(stock.shares) + " Shares"
                self.dailyDataList.delete("1.0",END)
                self.stockReport.delete("1.0",END)
                # for daily_data in stock.DataList:
                #     row = daily_data.date.strftime("%m/%d/%y") + "   " +  '${:0,.2f}'.format(daily_data.close) + "   " + str(daily_data.volume) + "\n"
                #     self.dailyDataList.insert(END,row)

                self.dailyDataList.insert(END,'Date\tClose Price\t\tVolume\n')     
                for daily_data in stock.DataList:
                    row = daily_data.date.strftime("%m/%d/%y") + "   " +  '${:0,.2f}'.format(daily_data.close) + "   " + '{:.2f}'.format(daily_data.volume) + "\n"
                    self.dailyDataList.insert(END,row)

                
                count        = 0
                price_total  = 0
                volume_total = 0
                lowPrice     = 99999999999.99
                highPrice    = 0
                lowVolume    = 9999999999999
                highVolume   = 0
                endPrice     = 0
                startDate    = datetime.strptime("12/31/2099","%m/%d/%Y")
                endDate      = datetime.strptime("1/1/1900","%m/%d/%Y")
                for daily_data in stock.DataList:
                    count+=1
                    price_total+=daily_data.close
                    volume_total+=daily_data.volume
                    if daily_data.close<lowPrice:
                     	lowPrice  = daily_data.close
                    elif daily_data.close > highPrice:
                        highPrice = daily_data.close
                    if daily_data.volume < lowVolume:
                        lowVolume = daily_data.volume
                    elif daily_data.volume > highVolume:
                        highVolume = daily_data.volume
                    if daily_data.date < startDate:
                        startDate = daily_data.date
                        startPrice = daily_data.close
                    elif daily_data.date > endDate:
                        endDate = daily_data.date
                        endPrice = daily_data.close
                    priceChange= endPrice - startPrice  
                    # self.dailyDataList.insert(END,daily_data.date.strftime("%m/%d/%y"),end='')
                    # self.dailyDataList.insert(END,"\t\t${:,.2f}".format(daily_data.close),end='')
                    # self.dailyDataList.insert(END,"\t\t{:,.0f}".format(daily_data.volume))
                if count > 0:
                    self.stockReport.insert(END,f'-Summary of {startDate.strftime("%m/%d/%y")} - {endDate.strftime("%m/%d/%y")}\n')
                    self.stockReport.insert(END,'  Low Price:--------------------'+"${:,.2f}\n".format(lowPrice))
                    self.stockReport.insert(END,'  High Price:-------------------'+"${:,.2f}\n".format(highPrice)) 
                    self.stockReport.insert(END,'  Average Price:----------------'+"${:,.2f}\n".format(price_total / count))
                    self.stockReport.insert(END,'  Low Volume:-------------------'+":{:,.0f}\n".format(lowVolume))
                    self.stockReport.insert(END,'  High Volume:------------------'+":{:,.0f}\n".format(highVolume))
                    self.stockReport.insert(END,'  Average Volume:---------------'+":{:,.0f}\n".format(volume_total / count))
                    self.stockReport.insert(END,'  Starting Price:---------------'+"${:,.2f}\n".format(startPrice))
                    self.stockReport.insert(END,'  Ending Price:-----------------'+"${:,.2f}\n".format(endPrice))
                    self.stockReport.insert(END,'  Change in Price:--------------'+"${:,.2f}\n".format(priceChange))
                    self.stockReport.insert(END,'  Profit/Loss:------------------'+"${:,.2f}\n".format(priceChange * stock.shares)) 

    # Add new stock to track.
    def add_stock(self):
        new_stock = Stock(self.addSymbolEntry.get(),self.addNameEntry.get(),float(self.addSharesEntry.get()))
        self.stock_list.append(new_stock)
        self.stockList.insert(END,self.addSymbolEntry.get())
        self.addSymbolEntry.delete(0,END)
        self.addNameEntry.delete(0,END)
        self.addSharesEntry.delete(0,END)

    # Buy shares of stock.
    def buy_shares(self):
        symbol = self.stockList.get(self.stockList.curselection())
        for stock in self.stock_list:
            if stock.symbol == symbol:
                 stock.buy(float(self.updateSharesEntry.get()))
                 self.headingLabel['text'] = stock.name + " - " + str(stock.shares) + " Shares"
        messagebox.showinfo("Buy Shares","Shares Purchased")
        self.updateSharesEntry.delete(0,END)

    # Sell shares of stock.
    def sell_shares(self):
        symbol = self.stockList.get(self.stockList.curselection())
        for stock in self.stock_list:
            if stock.symbol == symbol:
                 stock.sell(float(self.updateSharesEntry.get()))
                 self.headingLabel['text'] = stock.name + " - " + str(stock.shares) + " Shares"
        messagebox.showinfo("Buy Shares","Shares Sold")
        self.updateSharesEntry.delete(0,END)

    # Remove stock and all history from being tracked.
    def delete_stock(self):
        symbol = self.stockList.get(self.stockList.curselection())
        i = 0
        for stock in self.stock_list:
            if stock.symbol == symbol:
                self.stock_list.pop(i)
                i = i + 1
        self.display_stock_data()
        self.stockList.delete(0,END)
        sortStocks(self.stock_list)
        for stock in self.stock_list:
            self.stockList.insert(END,stock.symbol)
        self.headingLabel['text'] =''
        messagebox.showinfo("Stock Deleted",symbol + " Removed")

    # Get data from web scraping.
    def scrape_web_data(self):
        messagebox.showinfo("Under Construction","This Module Not Yet Implemented")

    # Import CSV stock history file.
    def importCSV_web_data(self):
        symbol = self.stockList.get(self.stockList.curselection())
        print(symbol)
        file_path = filedialog.askopenfilename()
        print(file_path)
        if file_path:
            file=file_path.split('/')[-1]
            print(file)
            # SD.import_stock_web_csv
            SC.import_csv(self.stock_list,symbol,file)
            self.display_stock_data()
    # Display stock price chart.
    def display_chart(self):
        symbol = self.stockList.get(self.stockList.curselection())
        display_stock_chart(self.stock_list, symbol)

def main():
        app = StockApp()
        

if __name__ == "__main__":
    # execute only if run as a script
    main()
