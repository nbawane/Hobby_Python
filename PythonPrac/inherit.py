#inheritance 

class Employee(object):
	def __init__(self,name):
		self.salary = 5000
		self.name = name
	
	def bonus(self):
		return self.salary*0.3
		
	def name(self):
		return self.name
		
class Engineer(Employee):
	def bonus(self):
		return (self.salary*0.5)+Employee.bonus(self)+super(Engineer, self).bonus()
		
		
obj = Employee('Nitesh')
print "salary : ",obj.salary
print "bonus : ",obj.bonus()
print "name : ",obj.name


eng = Engineer("tony")
print "salary : ",eng.salary
print "bonus : ",eng.bonus()
print "name : ",eng.name