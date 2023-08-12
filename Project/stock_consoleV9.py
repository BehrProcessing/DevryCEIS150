# Summary: This module contains the user interface and logic for a console-based version of the stock manager program.
# Author: Stephen Behr
# Date: 7/22/23

from utilities   import display_stock_chart#,clear_screen
from datetime    import datetime
from stock_class import Stock, DailyData
from os          import path
import stock_data

#My Functions
def pretend_screen_clear(Line_length):
    print('_'*Line_length+'')
def new_menu(menu_header,menu_list='',option='',escape_key=''):
    Line_length=50
    pretend_screen_clear(Line_length);#clear_screen()
    if option and option not in menu_list:
        print('*!* '+option)
    if escape_key:
        s=Line_length-len(menu_header)+2-len(escape_key)+6
        escape_key= " "*s+f'Enter {escape_key}'
    print(menu_header.upper()+' |\n'+'_'*(len(menu_header))+"_|"+escape_key+"\n")
#    menu_tab(menu_header)
def get_Symbols(stock_list,Verbage=''):
    if not stock_list:
        return False,'/'
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
    Input = input(f'Stock Symbol you wish to {Verbage}: ').upper() 
    found=False
    for stock in stock_list:
        if stock.symbol==Input:
            found=stock
            break
    return found, Input
def number(Q='',outsideInput=''):
    userInput=outsideInput
    if not outsideInput and Q!='pass':
        print(Q,end=" ")
    while True:
        if not outsideInput and Q!='pass':
            userInput=input()
        try:
            Num=float(userInput)
            return Num
        except:
            if userInput=='/':
                return userInput
            if outsideInput or Q=='pass':
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
    while option !="0":
        new_menu("Stock Analyzer",menu_list,option)
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
        elif option == "0":
            pretend_screen_clear();#clear_screen()
            print("    ~~~Goodbye~~~")
            raise SystemExit(0)
        if stock_list:
            if option == "2":
                add_stock_data(stock_list);option=''
            elif option == "3":
                display_report(stock_list);option=''
            elif option == "4":
                display_chart(stock_list)
        elif option in '[2,3,4]' and not stock_list:
            option=f'There is no data to use with Menu {option}. Use Manage Stocks(Add Stock),\nor use Manage Data(Load, Retrieve).'

# Manage Stocks
def manage_stocks(stock_list,option = ""):
    menu_list=["1","2","3","4","0"]
    while option !="0":
        new_menu("Manage Stocks",menu_list,option)
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
        elif option in '[2,3,4]' and not stock_list:
            option=f'There is no data to use with Menu {option}. Use Manage Stocks(Add Stock),\nor use Manage Data(Load, Retrieve).'

        
# Add new stock to track
def add_stock(stock_list,option=""):
    while option != '0':
        new_menu('Add Stock','','','/ to Cancel entry') 
        Input=['symbol','company name','shares']
        for i,key in enumerate(Input):
            while not option:
                print(f'Please enter the {key.capitalize()}: ',end='')
                option=input()
                if option=='/':
                    return
                elif Input[i]=='shares':
                        option=number('pass',option)
                if not option:
                    print('*!* Input not valid *!* ',end='')
            Input[i]=option ; option=''
        new_stock=Stock(Input[0].upper(),Input[1].title(),Input[2])
        stock_list.append(new_stock)
        print(f'Added {new_stock.shares} shares of {new_stock.name}({new_stock.symbol})')
        option=input("*** Press Enter to Continue or 0 to Exit ***")

# Buy or Sell Shares Menu
def update_shares(stock_list,option = ""):
    menu_list=["1","2","0"]
    while option != "0":
        new_menu("Update Shares", menu_list, option)
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
        new_menu('Buy Stock','','','/') ; Tense='Bought' ; Verbage='buy shares of' 
        found,Input=get_Symbols(stock_list, Verbage)
        if found:
            print(f'You have {found.shares} shares of',found.symbol)
            Shares=number(f'How many shares would you like to {Verbage}?')
            if Shares=='/':
                return
            found.buy(Shares)
            print(Tense,Shares,'shares of',found.symbol+', you now have',found.shares )
            option = input("*** Press Enter to continue or 0 to return to the menu ***")
        else:
            if Input=='/':
                return
            print(f'"{Input}" is not a valid option.')
            option = input("*** Press Enter to try again or 0 to return to menu ***")

# Sell Stocks (subtract from shares)
def sell_stock(stock_list,option=''):
    while option!='0':
        new_menu('Sell Stock','','','/') ; Tense='Sold' ; Verbage='sell shares of' 
        found,Input=get_Symbols(stock_list, Verbage)
        if found:
            print(f'You have {found.shares} shares of',found.symbol)
            Shares=number(f'How many shares would you like to {Verbage}?')
            if Shares=='/':
                return
            Enough=found.sell(Shares)
            if Enough:
                print(Tense,Shares,'shares of',found.symbol+', you now have',found.shares )
            option = input("*** Press Enter to continue or 0 to return to the menu ***")
        else:
            if Input=='/':
                return
            print(f'"{Input}" is not a valid option.')
            option = input("*** Press Enter to try again or 0 to return to menu ***")

# Remove stock and all daily data
def delete_stock(stock_list,option=''):
    while option !='0':
        new_menu('Remove Stocks','','','/') ; Tense='Removed' ; Verbage='delete'
        found,Input=get_Symbols(stock_list, Verbage)
        if found:
            print(found.symbol,'has been', Tense)
            stock_list.pop(stock_list.index(found))
            option = input("*** Press Enter to continue or 0 to return to the menu ***")
        else:
            if Input=='/':
                return
            print(f'"{Input}" is not a valid option.')
            option = input("*** Press Enter to try again or 0 to return to menu ***")

def list_stocks(stock_list):
    new_menu('Stock Portfolio List')
    object_List = stock_list
    headers     = ['Symbol','Company Name','Shares','Moneyformat','testing']
    Alignment   = ['L','L','R','R','R']      
    minSpacing  = 3            
    sizeOfColumn =[0.0]*len(headers)
    
    def SizeColumns(List):
        for column,columnValue in enumerate(Object.ListData):
            lenOfVal = len(str(columnValue))
            if lenOfVal > sizeOfColumn[column]:
                sizeOfColumn[column]=lenOfVal
                print(sizeOfColumn,column,columnValue)
            if sizeOfColumn[column]<len(str(headers[column])):
                    sizeOfColumn[column]=len(str(headers[column]))
                    print(sizeOfColumn,column,headers[column])
        
    def BuildRows(List,sfc):
        Row='';
        for column,columnValue in enumerate(List):
            if Alignment[column]=='L':
                Val= columnValue+sfc*(sizeOfColumn[column]-len(columnValue))
            else:
                Val=sfc*(sizeOfColumn[column]-len(columnValue))+columnValue
            if column!=len(headers)-1:
                Row += Val+sfc*minSpacing
            else:
                Row += Val
        return Row
    
    for Object in object_List:
        SizeColumns(Object.ListData)
    Header=BuildRows(headers,' ')    
    print(Header+'\n'+'='*len(Header))
    for Object in object_List:
        print(BuildRows(Object.ListData,'-'))
        
    _ = input("\n*** Press Enter to Return to Previous Menu ***")


# Add Daily Stock Data
def add_stock_data(stock_list,option=''):
    while option !='0':
        new_menu('Add Stock Data','','','/') ; Verbage = 'add information to'
        found,Input=get_Symbols(stock_list, Verbage)
        if found:
            print('Enter Daily Data information in the format shown.')
            print(f'| {found.symbol} |mm/dd/yy,ClosingPrice,Volume')
            import datetime ; today=datetime.date.today() ; year=today.year
            error='';inputData=''
            while option!='/' or inputData!='/':
                symbol_form=f'| {found.symbol} |'
                if error:
                    print('| '+'*'*len(found.symbol)+' |'+error)
                inputData=input(symbol_form+'mm/dd/yy,##,##\n'+symbol_form)
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
                    error+='    *!* Input Error *!*'
                    continue
                from datetime import datetime
                daily_data=DailyData(datetime.strptime(date,"%m/%d/%y"),float(price),float(volume))
                found.add_data(daily_data)
                error=''
                print(f'{symbol_form}{date}, Closing Price ${price}, Volume {volume} *added to report*')
                option = input(f"*** Press Enter to add more {symbol_form} data, 0 returns to menu, / to change symbol***")
                inputData=option
                if option=='0':
                    return
        else:
            print(f'"{Input}" is not a valid option.')
            option = input("*** Press Enter to Continue or 0 to return to menu ***")

# Display Report for All Stocks
def display_report(stock_data):
    x=47
    new_menu('Portfolio Report')
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
            print(f'\n-Summary of {startDate.strftime("%m/%d/%y")} - {endDate.strftime("%m/%d/%y")}')
            print('  Low Price:--------------------'+"${:,.2f}".format(lowPrice))
            print('  High Price:-------------------'+"${:,.2f}".format(highPrice)) 
            print('  Average Price:----------------'+"${:,.2f}".format(price_total / count))
            print('  Low Volume:-------------------'+"{:,.0f}".format(lowVolume))
            print('  High Volume:------------------'+"{:,.0f}".format(highVolume))
            print('  Average Volume:---------------'+"{:,.0f}".format(volume_total / count))
            print('  Starting Price:---------------'+"${:,.2f}".format(startPrice))
            print('  Ending Price:-----------------'+"${:,.2f}".format(endPrice))
            print('  Change in Price:--------------'+"${:,.2f}".format(priceChange))
            print('  Profit/Loss:------------------'+"${:,.2f}".format(priceChange * stock.shares)) 
        else:
            print('No Daily History')
        print('='*x+'\n')
    _ = input("*** Press Enter to Continue ***")

# Display Chart
def display_chart(stock_list,option=''):
    while option!='0' and option !='/':
        new_menu('Print Chart','','','/');Verbage='Chart'
        found,option=get_Symbols(stock_list, Verbage)
        if found:
            display_stock_chart(stock_list,found)  
        else:
            if option =='/':
                return
            print(f'Symbol "{option}" does not exist')
            option = input("*** Press Enter to Continue or 0 to Return to Menu ***")

# Manage Data Menu
def manage_data(stock_list,option=''):
    menu_list=["1","2","3","4","5","0"]
    while option != "0":
        new_menu("Manage Data",menu_list,option)
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
                option=f'There is no data to use with Menu {option}. Use Manage Stocks(Add Stock),\nor use Manage Data(Load, Retrieve).'

# Get stock price and volume history from Yahoo! Finance using Web Scraping
def retrieve_from_web(stock_list):
    pretend_screen_clear();#clear_screen()
    print("*** This Module Under Construction ***")
    _ = input("*** Press Enter to Continue ***")

# Import stock price and volume history from Yahoo! Finance using CSV Import
def import_csv(stock_list):
    pretend_screen_clear();#clear_screen()
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
    
    new_stock=Stock('RICH','extra shares',100000000000000)
    stock_list.append(new_stock)
    list_stocks(stock_list)
    new_stock=Stock('SLCN','super long company name',200000000000000)
    stock_list.append(new_stock)
    list_stocks(stock_list)
    new_stock=Stock('LONGSYMBOLTEST','company name',300000000000000)
    stock_list.append(new_stock)
    list_stocks(stock_list)
    
    dd=random.randint(11,15)
    mm=str(random.randint(1,12))
    yy=str(random.randint(10,23))
    pricechange=25
    volumechange=1000
    for stock in stock_list:
        day=dd
        price=random.randint(1,100)+float(random.random())
        volume=random.randrange(1,10000)
        for i in range(0,28-day):
            volume_change=random.randint(-volumechange,volumechange)+float(random.random())
            price_change=random.randint(-pricechange,pricechange)+float(random.random())
            volume+=volume_change
            price+=price_change
            if price<0:
                price=0
            if volume<0:
                volume=0
            day+=1
            date=mm+'/'+str(day)+'/'+yy 
            daily_data=DailyData(datetime.strptime(date,"%m/%d/%y"),float(price),float(volume))
            stock.add_data(daily_data)
            print(f'| {stock.symbol} |{date},{"{:.2f}".format(price)},{"{:.2f}".format(volume)}')
            #print(f'| {stock.symbol} |{date},{price},{volume}')
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
