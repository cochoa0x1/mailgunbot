from __future__ import print_function
import os

import requests
from tqdm import tqdm
from requests.utils import unquote
from time import sleep

from mailgunbot.utils import download_file

class MailGunBot(object):
	'''Creates a simple robot that watches a mailgun inbox.
	
	class myBot(MailGunBot):
		def process_new_message(self,message, key):
			print('we found a new message')

	bot = myBot(domain,key)

	bot.run()

	When a message is found, the bot calls self.should_fetch_message to decide to download

	afterwards, if there are attatchements, the bot calls self.should_download_attachment

	finally the bot calls self.process_new_message to do something with the message.

	'''
	def __init__(self, domain, key, data_dir= os.path.join(os.getcwd(),'mailgun_inbox'), debug=False):
		self.domain = domain
		self.key = key
		self.data_dir=data_dir
		self.mail={}
		self.debug=debug
		
	def _get(self,url):
		'''get request helper'''
		r = requests.get(url, auth=("api", self.key))
		r.raise_for_status()
		
		return r.json()
		
	def list_inbox(self):
		'''shows messages currently stored in mailgun'''
		url = self.domain + '/events?event=stored'
		return self._get(url).get('items',[])
		
	def download_inbox(self,delete=False):
		'''downloads everything in storage'''

		#grab whatever is new
		items = self.list_inbox()
		
		#see what is actually new and we actually want
		new_items = [ a for a in items if a['storage']['key'] not in self.mail and self.should_fetch_message(a) ]

		print('found %d new items to process'%len(new_items))

		for a in new_items:

			k = a['storage']['key']
		
			#download the message
			message = self._get(a['storage']['url'])

			#save the message and maybe get its attachments
			self.mail[k]= {'message': message,'attachments':[]}

			#check for any attatchements that we may want
			attachments = [ a for a in message['attachments'] if self.should_download_attachment(message,a) ]

			#get the files
			print('found %d files'%len(attachments))
			
			for a in attachments:
				download_file(a['url'],filename=a['name'],directory= os.path.join(self.data_dir,k), auth=("api", self.key), total_size=a['size'])
				self.mail[k]['attachments'].append(os.path.join(self.data_dir,k,a['name']))
		
			self.process_new_message(self.mail[k], k)

		return new_items
				
	def send(self,recipient,sender,subject,text,files=None):
		'''sends an email'''

		#found alot of the code here
		#https://cloud.google.com/appengine/docs/flexible/python/sending-emails-with-mailgun
		url = self.domain + '/messages'
		payload={
			'from': sender,
			'to': recipient,
			'subject': subject,
			'text': text
		}
		
		if files:
			files = [("attachment", open(files,'rb'))]
		r = requests.post(url, auth=('api', self.key), data=payload,files=files)
		
		r.raise_for_status()
		
		return r.json()

	def should_fetch_message(self,item):
		'''decide if we want to keep this message'''
		return True

	def should_download_attachment(self, message, attachment):
		'''decide if we want to download this file'''
		print('attachment downloading is turned off, this is a security risk! Validate your senders and files!!!')
		return False

	def process_new_message(self,message, key):
		'''do something afterward'''
		print('new message')

	def run(self,dt=30):
		'''run forever, pausing dt seconds to avoid making mulgun angry'''
		while(True):
			try:
				print('checking for new mail...')
				self.download_inbox()
			except Exception as e:
				print('something bad happened...')
				if self.debug:
					print(e)
			print('sleeping for %d seconds... '%dt)
			sleep(dt)




