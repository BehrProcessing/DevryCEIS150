# Summary: This module contains the user interface and logic for a console-based version of the stock manager program.
# Author: Stephen Behr
# Date: 7/22/23

from datetime import datetime
from stock_class import Stock, DailyData
from utilities import  display_stock_chart, clear_screen
from os import path
import stock_data
def menu_tab(msg):
    print(msg.upper()+' |\n'+'_'*(len(msg))+"_|\n")
def get_Symbols(stock_list,Verb=''):
    size=5
    print('                Available Stocks')
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n[',end='')
    for i,stock in enumerate(stock_list):
        x=' |'
        if i and (i+1) % 7==0:
            x+='\n '
        if i==len(stock_list)-1:
            x=' ]'
        print(' '*(size-len(stock.symbol))+stock.symbol,end=x)
    print('\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
    if Verb:
        return input(f'Stock Symbol you wish to {Verb} shares of: ').upper() 
    else:
        return input('Stock Symbol you would like to add information to: ').upper()
def number(Q='',outsideInput=''):
    userInput=outsideInput
    if not outsideInput:
        print(Q,end=" ")
    while True:
        if not outsideInput:
            userInput=input()
        try:
            Num=float(userInput)
            return Num
        except:
            if outsideInput:
                return False
            print(f'"{userInput}" is a string, please enter a number: ',end='')
            userInput=''
def select(options):
    selection=input("Enter Menu Option: ")
    if selection not in options:
        return '*** Invalid Option - Try again ***'
    return selection
# Main Menu
def main_menu(stock_list,option=''):
    menu_list=["1","2","3","4","5","0"]
    while option !='0':
        clear_screen();print('='*75+'\n')
        if option not in menu_list:
            print(option)
        menu_tab("Stock Analyzer")
        print("1 - Manage Stocks (Add, Update, Delete, List)")
        print("2 - Add Daily Stock Data (Date, Price, Volume)")
        print("3 - Show Report")
        print("4 - Show Chart")
        print("5 - Manage Data (Save, Load, Retrieve)")
        print("0 - Exit Program")
        option = select(menu_list)
        if option == "1":
            manage_stocks(stock_list)
        elif option == "5":
            manage_data(stock_list)
        if option == "0":
            clear_screen();print('='*75+'\n')
            print("    ~~~Goodbye~~~")
            raise SystemExit(0)
        if stock_list:
            if option == "2":
                add_stock_data(stock_list);option=''
            elif option == "3":
                display_report(stock_list);option=''
            elif option == "4":
                display_chart(stock_list)
        else:
            option='There is no data to alter or show. Please start with Manage Stocks (Add Stock).\nYou can also use the Manage Data if you wish to load or retrieve data.'

# Manage Stocks
def manage_stocks(stock_list):
    option = ""; menu_list=["1","2","3","4","0"]
    while option !="0":
        clear_screen();print('='*75+'\n')
        if option not in menu_list:
            print(option)
        menu_tab("Manage Stocks")
        print("1 - Add Stock")
        print("2 - Update Shares")
        print("3 - Delete Stock")
        print("4 - List Stocks")
        print("0 - Exit Manage Stocks")
        option = select(menu_list)
        if option == "0":
            print("Returning to Main Menu")
            return
        if option == "1":
            add_stock(stock_list)
        if stock_list:
            if option == "2":
                update_shares(stock_list)
            elif option == "3":
                delete_stock(stock_list)
            elif option == "4":
                list_stocks(stock_list)
        else:
            option='There is no data to alter or show. Please start with Manage Stocks (Add Stock).\nYou can also use Manage Data in the main menu to load or retrieve data.'

        
# Add new stock to track
def add_stock(stock_list):
    clear_screen();print('='*75+'\n')
    menu_tab('Add a new Stock to your portfolio') ; option=""
    print('Enter / to Exit Add Stocks at any time.')
    while option != '0':
        Input=['Symbol','Company Name']# (convert symbol to upper case)
        for i,key in enumerate(Input):
            print(f'Please enter the {key}: ',end='')
            Input[i]=input()
            while not Input[i]:
                print('Enter a valid input to continue: ',end='')
                Input[i]=input()
            if Input[i]=='/':
                return
        Shares=number('Please enter the number of shares held:')
        new_stock=Stock(Input[0].upper(),Input[1].title(),Shares)
        stock_list.append(new_stock)
        print(f'Added {new_stock.shares} shares of {new_stock.name}({new_stock.symbol})')
        option=input("*** Press Enter to Continue or 0 to Exit ***")

# Buy or Sell Shares Menu
def update_shares(stock_list,option = ""):
    
    menu_list=["1","2","0"]
    while option != "0":
        clear_screen();print('='*75+'\n')
        if option not in menu_list:
            print(option)
        menu_tab("Update Shares")
        print("1 - Buy Shares")
        print("2 - Sell Shares")
        print("0 - Exit Update Shares")
        option = select(menu_list)
        if option == "1":
            buy_stock(stock_list)
        elif option == "2":
            sell_stock(stock_list)
        elif option == "0":
            print("Returning to Main Menu")

# Buy Stocks (add to shares)
def buy_stock(stock_list,option=''):
    while option!='0':
        option=''
        clear_screen();print('='*75+'\n')
        menu_tab('Portfolio Marketplace');Tense='Bought';Verb='buy' 
        Symbol=get_Symbols(stock_list, Verb)
        found=False
        for stock in stock_list:
            if stock.symbol==Symbol:
                found=stock
                break
        if found:
            Shares=number(f'How many shares would you like to {Verb}?')
            found.buy(Shares)
            print(Tense,Shares,'shares of',Symbol+', you now have',found.shares )
            option = input(f"*** Press Enter to {Verb} more or 0 to return to the menu ***")
        else:
            print(f'"{Symbol}" is not a valid option.')
            option = input("*** Press Enter to try again or 0 to return to menu ***")

# Sell Stocks (subtract from shares)
def sell_stock(stock_list,option=''):
    while option!='0':
        clear_screen();print('='*75+'\n')
        menu_tab('Portfolio Marketplace');Tense='Sold';Verb='sell'
        Symbol=get_Symbols(stock_list, Verb)
        found=False
        for stock in stock_list:
            if stock.symbol==Symbol:
                found=stock
                break
        if found:
            print(f'You have {found.shares} shares of',Symbol)
            Shares=number(f'How many shares would you like to {Verb}?')
            Enough=found.sell(Shares)
            if Enough:
                print(Tense,Shares,'shares of',Symbol+', you now have',found.shares )
            option = input(f"*** Press Enter to {Verb} more or 0 to return to the menu ***")
        else:
            print(f'"{Symbol}" is not a valid option.')
            option = input("*** Press Enter to try again or 0 to return to menu ***")

# Remove stock and all daily data
def delete_stock(stock_list,option=''):
    while option !='0':
        clear_screen();print('='*75+'\n')
        menu_tab('Remove Stocks') ; Tense='Removed' ; Verb='delete'
        Symbol=get_Symbols(stock_list,Verb) 
        found=False
        for stock in stock_list:
            if stock.symbol==Symbol:
                found=stock
                break
        if found:
            print(found.symbol,'has been', Tense)
            stock_list.pop(stock_list.index(found))
            option = input(f"*** Press Enter to {Verb} more or 0 to return to the menu ***")
        else:
            print(f'"{Symbol}" is not a valid option.')
            option = input("*** Press Enter to try again or 0 to return to menu ***")

# List stocks being tracked
def list_stocks(stock_list):
    clear_screen();print('='*75+'\n')
    menu_tab('Stock Portfolio List')
    headers=['SYMBOL','COMPANY NAME','SHARES'];Header="";s='-';sizeColumn=[10,16,4]
    columnList=stock_list
    space_between=2
    for itemInColumn in columnList:
        attributes=[itemInColumn.symbol,itemInColumn.name,itemInColumn.shares]
        for f,attribute in enumerate(attributes):
            lenOfAttr=len(str(attribute))
            if lenOfAttr>sizeColumn[f]:
                    sizeColumn[f]=lenOfAttr+space_between 
    x=sizeColumn
    for i,heading in enumerate(headers): 
        last=len(headers)-1
        if i==last:
            Header+= ' '*(x[last]-len(headers[last]))+str(headers[last])
        else:
            Header+= str(heading+' '*(x[i]-len(heading)))
    toEnd=len(Header)
    print(Header+'\n'+'='*toEnd)
    for stock in stock_list:
        values =[stock.symbol,stock.name,stock.shares]
        fromEnd=toEnd-x[0]-len(values[1])-len(str(float(values[2])))
        print(values[0]+s*(x[0]-len(values[0]))+values[1]+s*(fromEnd)+str(float(values[2])))
    _ = input("\n*** Press Enter to Return to Previous Menu ***")

# Add Daily Stock Data
def add_stock_data(stock_list,option=''):
    inputData=''
    while option !='0':
        clear_screen();print('='*75+'\n')
        menu_tab('Add Stock Data')
        Symbol=get_Symbols(stock_list)
        found=False
        for stock in stock_list:
            if stock.symbol==Symbol:
                found=stock
                break
        if found:
            print('Please enter the daily data information in the format as follows.')
            print('Use numerical values and "/" for date. Include commas between data.')
            print(f'| {Symbol} |mm/dd/yy,ClosingPrice,Volume */* to pick a new symbol.')
            import datetime ; today=datetime.date.today() ; year=today.year
            error='';inputData=''
            while option!='/' or inputData!='/':
                spacing=f'| {Symbol} |'
                if error:
                    print('| '+'*'*len(Symbol)+' |'+error)
                inputData=input(spacing+'mm/dd/yy,##,##\n'+spacing)
                if inputData=='/':
                    break
                Data=inputData.replace(' ','').split(',')
                if len(Data)!=3:
                    error='Not enough information added please check your input'
                    continue
                check_date=Data[0].split('/')
                mm='!!';dd='!!';yy='!!'
                if check_date[0].isdigit():
                    if len(check_date[0])<=2:
                        if float(check_date[0])<=12:
                            mm=check_date[0]
                if check_date[1].isdigit():
                    if len(check_date[1])<=2:
                        if float(check_date[1])<=31:
                            dd=check_date[1]
                if check_date[2].isdigit(): 
                    if len(check_date[2])<=2:
                        if 2000+float(check_date[2])<=year:
                            yy=check_date[2]
                date=mm+'/'+dd+'/'+yy 
                price = number('',Data[1]) 
                volume= number('',Data[2])
                if not price:
                    error=date+','+'!'*len(Data[1])
                else:
                    error=date+','+Data[1]
                if not volume:
                    error+=','+'!'*len(Data[2])
                else:
                    error+=','+Data[2]
                if error.count('!'):
                    error+=' *!* <--- ERORRS in your input.'
                    continue
                from datetime import datetime
                daily_data=DailyData(datetime.strptime(date,"%m/%d/%y"),float(price),float(volume))
                found.add_data(daily_data)
                error=''
                print(f'{spacing}{date}, Closing Price ${price}, Volume {volume} *added to report*')
                option = input(f"*** Press Enter to add more {spacing} data, 0 returns to menu, / to change symbol***")
                inputData=option
                if option=='0':
                    return
        else:
            print(f'"{Symbol}" is not a valid option.')
            option = input("*** Press Enter to try again or 0 to return to menu ***")

# Display Report for All Stocks
def display_report(stock_data):
    clear_screen();print('='*75+'\n')
    x=47
    menu_tab('Portfolio Report')
    for stock in stock_data:
        header=f'Report for {stock.symbol} - {stock.name} -'+' Shares: {:,.0f}'.format(stock.shares)
        print('_'*x)
        print(f'{header}\n'+'*'*x)
        print('Date\t\tClose Price\t\tVolume')
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
            print(daily_data.date.strftime("%m/%d/%y"),end='')
            print("\t\t${:,.2f}".format(daily_data.close),end='')
            print("\t\t{:,.0f}".format(daily_data.volume))
        if count > 0:
            print(f'\n~~~~~Summary {startDate.strftime("%m/%d/%y")} - {endDate.strftime("%m/%d/%y")}')
            print('Low Price:-----------------'+"${:,.2f}".format(lowPrice))
            print('High Price:----------------'+"${:,.2f}".format(highPrice)) 
            print('Average Price:-------------'+"${:,.2f}".format(price_total / count))
            print('Low Volume:----------------'+"{:,.0f}".format(lowVolume))
            print('High Volume:---------------'+"{:,.0f}".format(highVolume))
            print('Average Volume:------------'+"{:,.0f}".format(volume_total / count))
            print('Starting Price:------------'+"${:,.2f}".format(startPrice))
            print('Ending Price:--------------'+"${:,.2f}".format(endPrice))
            print('Change in Price:-----------'+"${:,.2f}".format(priceChange))
            print('Profit/Loss:---------------'+"${:,.2f}".format(priceChange * stock.shares)) 
        else:
            print('No Daily History')
        print('='*x+'\n')
    _ = input("*** Press Enter to Continue ***")

# Display Chart
def display_chart(stock_list):
    clear_screen();print('='*75+'\n')
    print("*** This Module Under Construction ***")
    _ = input("*** Press Enter to Continue ***")

# Manage Data Menu
def manage_data(stock_list,option=''):
    menu_list=["1","2","3","4","5","0"]
    while option != "0":
        clear_screen();print('='*75+'\n')
        if option not in menu_list:
            print(option)
        menu_tab("Manage Data")
        print("1 - Save Data to Database")
        print("2 - Load Data from Database")
        print("3 - Retrieve Data from Web")
        print("4 - Import from CSV File")
        print("5 - Create Test Stocks")
        print("0 - Exit Manage Data")
        option = select(menu_list)
        if option == "2":
            stock_data.load_stock_data(stock_list)
            print("--- Data Loaded from Database ---")
            _ = input("Press Enter to Continue")
        elif option == "3":
            retrieve_from_web(stock_list)
            print("--- Data Retrieved from Yahoo! Finance ---")
            _ = input("Press Enter to Continue")
        elif option == "4":
            import_csv(stock_list)
        elif option == "5":
            create_test(stock_list)
        elif option == "0":
            print("Returning to Main Menu")
        elif option == "1":
            if stock_list:
                stock_data.save_stock_data(stock_list)
                print("--- Data Saved to Database ---")
                _ = input("Press Enter to Continue")
            else:
                print("No data to save")
                _ = input("Press Enter to Continue")
            

# Get stock price and volume history from Yahoo! Finance using Web Scraping
def retrieve_from_web(stock_list):
    clear_screen();print('='*75+'\n')
    print("*** This Module Under Construction ***")
    _ = input("*** Press Enter to Continue ***")

# Import stock price and volume history from Yahoo! Finance using CSV Import
def import_csv(stock_list):
    clear_screen();print('='*75+'\n')
    print("*** This Module Under Construction ***")
    _ = input("*** Press Enter to Continue ***")

#Creates a test set of stocks to quickly populate and test functions
def create_test(stock_list):
    import random
    for i in range(0,10):
        C1=random.randint(97,120)
        C2=random.randint(97,120)
        C3=random.randint(97,120)
        C4=random.randint(97,120)
        first=chr(C1)+chr(C2)+chr(C3)+chr(C4)
        name='company '+first
        shares=random.randint(1,5000)
        new_stock=Stock(first.upper(),name.title(),shares)
        stock_list.append(new_stock)
    list_stocks(stock_list)
    # new_stock=Stock('RICH','extra shares',100000000000000)
    # stock_list.append(new_stock)
    # list_stocks(stock_list)
    # new_stock=Stock('SLCN','super long company name',200000000000000)
    # stock_list.append(new_stock)
    # list_stocks(stock_list)
    # new_stock=Stock('LONGSYMBOLTEST','company name',300000000000000)
    # stock_list.append(new_stock)
    # list_stocks(stock_list)
    mm=str(random.randint(1,12))
    dd=random.randint(1,15)
    yy=str(random.randint(10,23))
    for stock in stock_list:
        d=dd
        for i in range(0,13):
            d+=1
            #mm=str(random.randint(1,12))
            #dd=str(random.randint(1,15))
            #yy=str(random.randint(10,23))
            date=mm+'/'+str(d)+'/'+yy 
            price=random.randrange(1,100)
            volume=random.randrange(1,10000)
            daily_data=DailyData(datetime.strptime(date,"%m/%d/%y"),float(price),float(volume))
            stock.add_data(daily_data)
            print(f'| {stock.symbol} |{date},{price},{volume}')
    print('Added random daily data for report')
    _ = input("*** Press Enter to Continue ***")
    display_report(stock_list)
    
# Begin program
def main():
    #check for database, create if not exists
    if path.exists("stocks.db") == False:
        stock_data.create_database()
    stock_list = []
    main_menu(stock_list)

# Program Starts Here
if __name__ == "__main__":
    # execute only if run as a stand-alone script
    main()
