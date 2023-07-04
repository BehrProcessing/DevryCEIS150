import random#Name Stephen Behr | Date 7/3/2023 | Class CEIS150 
Less=0;Greater=0;count=0;Sum=0;G=[];L=[];price_list=[]
listSize=random.randrange(5,20);print('Welcome to the module 1 project')
name=input('What is your full name: ')
def list_print(List):
    for Amount in List:
        print(f'${Amount}',end=' | ')
    print('')
while True:
    try:
        Min="{:.2f}".format(float(input('What is your maximum budget: $')))
        if type(float(Min)) is not str:
            break
    except ValueError:
        print('Please enter a number value:')
        continue   
for f in range(0,listSize):
    makePrice=float(Min)+(f/2)*(random.randrange(-1,1)+(random.randrange(1,99)/100)) #makes the random price list
    if makePrice>0:
        price="{:.2f}".format(float(makePrice)) #reformats to two decimal spaces as string float
        price_list.append(price)
        Sum+=float(price)
        if float(price) > float(Min):
            Greater+=1 ; G.append(price) #Creates a list of prices greater than budget
        elif float(price) <= float(Min):
            Less+=1 ; L.append(price)    #Creates a list of prices at or under budget
print("Hello",name.capitalize(),"Your maximum budget was $",Min)
print("There are",Greater,"price(s) that are out of your budget;") ;list_print(G)
print("There are",Less,"price(s) within your budget;")             ;list_print(L)
print(f"The total for all {len(price_list)} products in inventory is $",end="")
print("{:.2f}".format(float(Sum)))                                 ;list_print(price_list)
