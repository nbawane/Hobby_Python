a = [num for num in range(2,999) if all([num%i for i in range(2,num)])]
print(a)

