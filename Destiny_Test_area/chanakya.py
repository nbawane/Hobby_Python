"""
program to execute the series sequentially
"""
import os
import re
from sys import argv

path = r'C:\chanakya'
episode_location = r'C:\Training\file_rnm'

	
#Chandragupta Maurya - [Episode 37] - 15th July 2011 - YouTube
class MediaOp:
	def log_episode(self,path,epino=None):
		self.path = path
		self.epino = epino
		#
		try:
			log = open(self.path,'w+')
		except IOError:
			print 'file not present'
		else:
			log.write(str(self.epino+1))								#incrementing episode number and writing into log file
	
	'''
	from the episode name it extracts episode number
	'''
	def extract_episode_num(self,epiname):
		self.epiname = epiname
		try:
			self.temp = ((self.epiname.split('['))[1]).split(']')[0]	#extracting the Episode xx from episode name
		except IndexError:												#to raise exception if episode name is not in format
			print'wrong file name or Episodes have finished'
			raise
		else:
			return re.findall('\d+',self.temp)							#to extract number from the string
	
	def play_media(self,episode=None,log_path=''):
		self.episode = episode
		self.log_path = log_path
		self.epino = None
		'''
		will execute if any episode is passed. It will update the the passed epi no to log file. 
		if episode no is not given the this function should fetch the episode nummber from 
		log file
		'''
		try:
			log = open(self.log_path,'r')
		except:
			print"file not found"
		else:
			#run if epino is given
			if self.episode:	
				print'playing episode num ',self.episode
				self.epino = self.episode
				
			#run if epino is not given get it from log file
			else:				
				self.epino=int(log.read())						#epino contains episode read from file
			
			self.log_episode(self.log_path,epino=self.epino)	#log the episode into log file
		self.episodes = os.listdir(episode_location)			
		for i in self.episodes:
			try:
				if self.epino ==int((self.extract_episode_num(i)[0])):
					self.temp = os.getcwd()						
					os.chdir(episode_location)					#changing the current working directory
					os.system(i)
					os.chdir(self.temp)
					break					
			except (TypeError,IndexError):
				print 'not a desired episode name'
				print i
				continue
		
				
	def main(self):
		
		log_file = r'C:\chanakya\logzee.txt'			
		try:
			script,episode_number = argv
		except ValueError:
			self.play_media(log_path = log_file)				#will be called if episode nnumber is not given in arguments
		else:
			self.play_media(episode=int(episode_number),log_path = log_file)#will be called if episode number is given in cmd arguments

obj = MediaOp()
obj.main()

