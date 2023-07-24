# -*- coding: utf-8 -*-
"""
Created on Sun Jul 23 10:22:22 2023

@author: Stephen
"""
#import datetime
import datetime
today=datetime.date.today()
year=today.year
#test=datetime.strptime("1/1/20","%m/%d/%y")
#time=datetime.now()
#print(datetime.strptime(today,"%m/%d/%y"))

print(today, type(today))
print(year, type(year))
option=''
while option !='0':
    print('Beginning of while')
    option=input('Test continue with "c" or test break with "b":').lower()
    if option=='c':
        print('Continues to',end=' ')
        continue
    elif option=='b':
        print('Breaks to',end=' ')
        break
    print('End of while')
print('Outside of while')