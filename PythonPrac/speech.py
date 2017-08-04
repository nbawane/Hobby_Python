#speech module test

import pyttsx
engine = pyttsx.init()
engine.setProperty('rate', 90)

voices = engine.getProperty('voices')
def say(command):
	for voice in voices:
		#print "Using voice:", repr(voice)
		engine.setProperty('voice', voice.id)
		engine.say(command)
	engine.runAndWait()
