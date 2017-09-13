import time

tempList = [2,3,4,4,67,76]
a = time.time()fib = [0,1,1,2,3,5,8,13,21,34,55]
list_of_square = [x**2 for x in tempList]
total = sum(list_of_square)
b = time.time()
print list_of_square
print total
print (b-a)