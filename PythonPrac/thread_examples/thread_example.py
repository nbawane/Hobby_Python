''' demonstrate the pydispatch module '''
from pydispatch import dispatcher
import threading
import time

ALICE_SIGNAL = 'alice_signal'
ALICE_SENDER = 'alice_sender'
BOB_SIGNAL = 'bob_signal'
BOB_SENDER = 'bob_sender'


class Alice():
	''' alice procrastinates and replies to bob'''

	def __init__(self):
		print('alice instantiated')
		dispatcher.connect(self.alice_dispatcher_receive, signal=BOB_SIGNAL, sender=BOB_SENDER)
		# self.alice()

	def alice_dispatcher_receive(self, message):
		''' handle dispatcher'''
		print('alice has received message: {}'.format(message))
		dispatcher.send(message='thankyou from Alice', signal=ALICE_SIGNAL, sender=ALICE_SENDER)

	# def alice(self):
	# 	''' loop and wait '''
	# 	while (1):
	# 		print('Alice is procrastinating')
	# 		time.sleep(1)


class Bob():
	''' bob contacts alice periodically '''

	def __init__(self):
		print('Bob instantiated')
		dispatcher.connect(self.bob_dispatcher_receive, signal=ALICE_SIGNAL, sender=ALICE_SENDER)
		self.bob()

	def bob_dispatcher_receive(self, message):
		''' handle dispatcher '''
		print('bob has received message: {}'.format(message))

	def bob(self):
		''' loop and send messages using a dispatcher '''
		while (1):
			dispatcher.send(message='message from Bob', signal=BOB_SIGNAL, sender=BOB_SENDER)
			time.sleep(3)


if __name__ == '__main__':
	# alice_thread = threading.Thread(target=Alice)
	# alice_thread.start()
	# bob_thread = threading.Thread(target=Bob)
	# bob_thread.start()
	Alice()
	Bob()
	Alice()