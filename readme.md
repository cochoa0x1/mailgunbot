### Simple mailgun based email bot


Creates a simple robot that watches a mailgun inbox.
	
example:

```python
from mailgunbot import MailGunBot

class myBot(MailGunBot):
	def process_new_message(self,message, key):
		print('we found a new message :)')

bot = myBot(domain,key)

bot.run()
```

When a message is found, the bot calls self.should_fetch_message to decide to download

afterwards, if there are attachments, the bot calls self.should_download_attachment

finally the bot calls self.process_new_message to do something with the message.

#### Requires:

* requests
* tqdm
* an account on [mailgun.com](www.mailgun.com)

#### Install:

```$python setup.py install```