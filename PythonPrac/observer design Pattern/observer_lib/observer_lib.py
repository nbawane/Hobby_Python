from threading import Thread


'''
	AIM : subobj.publish(key,data)

		subobj.subscribe(function,key)

		function(data)	#data would be data sent by publish API
'''

class Subject:
	def __init__(self):
		self._observerdict = {}	#while publishing a key will be given and a function will be passed corresponding to key
								#more than one function can be attached to one key


	def subscribe(self, observer, key):
		#observer is a function gets executed once published

		if not key in self._observerdict.keys():

			self._observerdict[key]= [observer]
		else:
			self._observerdict[key].append(observer)

	def publish(self,key):
		if key in self._observerdict.keys():
			function_list = self._observerdict[key]
			for func in function_list:
				func()

	def get_all_observer_info(self):
		return self._observerdict
	# def publish(self,key,data):

class naruto:

	def tryone(self):
		print('I got subscribed')

	def only(self):
		print('i am onlt ')

if __name__ == '__main__':
	a = naruto()
	subobj = Subject()
	subobj.subscribe(a.tryone,'try')
	subobj.subscribe(a.only,'try')
	print(subobj.get_all_observer_info())
	subobj.publish('try')





