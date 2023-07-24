

print("print('Welcome to the Dictionary tutorial')")
print("print('Type Help to access more commands')")
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
print('Welcome to the Dictionary tutorial')
print('Type Help to access more commands')
#How to create and manipulate a dictionary
    #prices = {}  # Create empty dictionary named prices
    #prices['banana'] = 1.25 Adds a new set 'banana':1.25 or updates existing occurance of banana within the dictionary
    #del prices['banana']  # Remove entry 'banana'
    #Variable ={prices['apples']} #assigns Variable with the second number set from the key of "apples"
prices = {'apples': 1.99, 'oranges': 1.49} #creates a dictionary with two values
Key=input('Please input item for price check:')
if Key in prices:
    Variable =prices[Key] #assigns Variable with the second number set from the user input Key 
    print('print(Key,"are ${} each".format(Variable))')
    print(Key,"are ${} each".format(Variable))
elif Key == "Help":
    print('Current commands:')
elif Key[0] == '+':
    print('Adding {} as new product')
else:
    print('Please check your spelling, if your item is spelled correctly then no such item is in stock')
    print('Here is a list of current items {}'.format(prices))


