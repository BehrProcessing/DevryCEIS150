#CEIS150 Module 1 Discussion-Topic 2 Stephen Behr 
#Write a python program to accept a user's:
#    name, age, and favorite color and print out a welcome message.
standard_colors = ['red','orange','yellow','green','blue','purple']
name = input('Hello and welcome! What is your name? ')
while True:
    try:   
        age=input(f'How many years old are you {name.capitalize()}? ') 
        if type(float(age)) is not str:
            break
    except ValueError:
        print(f'Please enter a number {name.capitalize()}')
        continue  
fav_color=input(f'What is your favorite color {name.capitalize()}? ')    
if fav_color.lower() in standard_colors:
    print(f'Oh I know what color {fav_color} is!')
else:
    print('I have never heard of that color, let me add it to my list.')
    standard_colors.append(fav_color)
print('It was great to meet you and learn a little about you ',end='')
print(f'{name.capitalize()}!\nCongrats on surviving for {age} years.')
print(f'I hope you get to see {fav_color} everyday from now on!')

