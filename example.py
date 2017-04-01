from mailgunbot import MailGunBot

import os

domain = os.environ['MAILGUNDOMAIN']
key = os.environ['MAILGUNKEY']

class Bot(MailGunBot):     
	def process_new_message(self,message, key):
		print('processing message...')
		 
	def should_fetch_message(self,item):
		subject = item['message']['headers']['subject']
		sender = item['message']['headers']['from']
		to = item['message']['headers']['to']

		print(sender,to, subject)
		return True
		

	def should_download_attachment(self, message, attachment):
		return False


if __name__=='__main__':
	bot = Bot(domain,key)
	bot.run(30)
