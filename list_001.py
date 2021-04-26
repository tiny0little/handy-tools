#!/usr/local/bin/python3

# https://www.w3resource.com/python-exercises/list/
# 1. Write a Python program to sum all the items in a list

myList = input("pleas enter your space-separated list of numbers: ").split(" ")

# removing not-numeric items
k = 0
while k < len(myList):
    if not myList[k].isnumeric():
        print(f">>> {myList[k]} is not a number")
        myList.pop(k)
        k -= 1    
    k += 1



sum = 0
for v in myList:
    sum += int(v)

print(f"sum of all the items in a list is {sum}")