#Name Stephen Behr | Date 7/3/2023 | Class CEIS150     
print('Welcome to the module 1 project') ; import random
print('~~~~~~~~~~~~~INPUTS~~~~~~~~~~~~') ; name=input('What is your full name: ')
def list_print(List):
    for index, Amount in enumerate(List):
        print(f'${"{:.2f}".format(float(Amount))}',end=' | ')
        if not (index+1)%5 and index+1!=0 and index+1!=len(List):
            print('\n',end='')
    print('\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
while True:   
    while True:
        try:
            Min=float(input('What is your maximum budget: $'))
            if type(float(Min)) is not str:
                break
        except ValueError:
            print('Please enter a number:')
            continue   
    price_list=[] ; Less=0 ; Greater=0 ; G=[] ; L=[] ; Sum=0 ; listSize=random.randrange(5,20)
    for f in range(0,listSize):              #Random price generation
        price=float(Min)+(f*random.randrange(-2,2))*0.75+(random.randrange(1,99)/100)
        if price>0:
            price_list.append(price) ; Sum+=price
            if price > Min:
                Greater+=1 ; G.append(price) #Creates a list of prices greater than budget
            elif price <= Min:
                Less   +=1 ; L.append(price) #Creates a list of prices at or under budget
    print(f"\nHello {name.capitalize()}, with a budget of ${'{:.2f}'.format(float(Min))},")
    print("There are",Less,"price(s) within your current budget;")        ;   list_print(L)
    print("There are",Greater,"price(s) that are over your budget;")      ;   list_print(G)
    print(         f"The total of all {len(price_list)} products in inventory is $",end="")
    print("{:.2f}".format(float(Sum)))         ;   price_list.sort();list_print(price_list)
