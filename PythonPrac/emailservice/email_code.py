import smtplib
def send_mail(self,msg=''):
	fromMy = 'gologictestnotigy@yahoo.com' # fun-fact: from is a keyword in python, you can't use it as variable, did abyone check if this code even works?
	to  = 'gologictestnotigy@yahoo.com'
	subj='Gologic Used'
	date='2/1/2010'
	message_text=msg

	msg = "From: %s\nTo: %s\nSubject: %s\nDate: %s\n\n%s" % ( fromMy, to, subj, date, message_text )

	username = str('cdacpathway@yahoo.com')
	password = str('Griffin@123')

	try :
		server = smtplib.SMTP("smtp.mail.yahoo.com",587)
		server.starttls()
		server.login(username,password)
		server.sendmail(fromMy, to,msg)
		server.quit()
		print('done')
	except Exception as e:
		print('isssue in mail')
