#decorators

def brokerage(amount):
	result = amount *0.3
	return result	

@brokerage	
def buy_house(amount):
	
	return amount
	
print "brokerage ",buy_house(100000)
