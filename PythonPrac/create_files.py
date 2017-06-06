class FileOp:
	def create_dir(self,path):
		self.path = path
		if os.path.exists(self.path):
			print "path exist already...!"
		else:
			os.mkdir(self.path)
			print"path created"

	def create_file(self,path,i):
		self.path = path	
		self.index = str(i)
		self.path = self.path+"\_ep"+self.index+'_.txt'
		if os.path.exists(self.path):
			print "%s file exist already...!"%(self.path)
		else:
			f=open(self.path,'w+')
			print"%s path is created"%(self.path)
			f.write(self.path)	