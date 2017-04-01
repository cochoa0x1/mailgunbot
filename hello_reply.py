from mailgunbot import MailGunBot

import os

'''example showing how a simple rule based reply might work.

Ideally routes should  be setup for most of the filtering on the mailgun side

'''
domain = os.environ['MAILGUNDOMAIN']
key = os.environ['MAILGUNKEY']
myemail = 'myemail@asdsfsfsdfd.com'

class Bot(MailGunBot):     
	def process_new_message(self,message, key):
		#get the info we need from the message
		to = message['message']['sender']
		subject = 'Re: '+ message['message']['subject']
		body ="hello friend :).\n I am a robot.\n My name is robot."

		print('repyling to %s'%to)

		self.send(to,myemail,subject,body)
		
		 
	def should_fetch_message(self,item):
		subject = item['message']['headers']['subject']
		return subject.strip().upper() == 'HELLO'
		
	def should_download_attachment(self, message, attachment):
		return False


if __name__=='__main__':
	bot = Bot(domain,key)
	bot.run(30)