def menu_tab(msg):
    print(msg.upper()+' |\n'+'_'*(len(msg))+"_|\n")
def list_stocks(stock_list):
    # clear_screen()
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
