def list_print(List):                           #!!! Name Stephen Behr | Date 7/3/2023 | Class CEIS150  
    for index, Amount in enumerate(List):
        print(f'${"{:.2f}".format(float(Amount))}',end=' | ')
        if not (index+1)%5 and index+1!=0 and index+1!=len(List):
            print('\n',end='')
    print('\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~') 
count = 0                                       #!!! initialize the count variable to 0
sum   = 0                                       #!!! initialize the sum variable to 0
print('Welcome to the module 1 project\n~~~~~~~~~~~~~INPUTS~~~~~~~~~~~~') 
full_name=input('Please enter your full name: ')#!!! input full_name
while True:
    try:                                        #!!! input the min_price and convert it to float
        min_price=float(input('How much is the cheapest product in this store: $'))
        if type(float(min_price)) is not str:
            break
    except ValueError:
        print('Please enter a number:')
        continue   
price_list=[] ; import random ; listSize=random.randrange(5,20) ; G=[] 
for f in range(0,listSize):                     #!!! create a list of prices
    price=float(min_price)+f*(random.randrange(0,2)+(random.randrange(1,99)/100))
    if price>0:
        price_list.append(price)                
for price in price_list:                        #!!! for price in price_list
    if price > min_price:                       #!!!    if price > min_price
        sum+=price                              #!!!    add current price to sum
        count+=1                                #!!!    increment count by 1 
        G.append(price)
print(f"\nHello {full_name.capitalize()} the minimum price is ${'{:.2f}'.format(float(min_price))},")
print("There are",count,"prices that are greater than the minimum price;");list_print(G)
print(f"The total of all {len(price_list)} products in inventory is $",end="")
print("{:.2f}".format(float(sum))) ; price_list.sort();list_print(price_list)
#output "Hello",name,"the minimum price is ",min_price
#output "There are ",count,"prices greater than the minimum price"
#output "The total price is ",sum
