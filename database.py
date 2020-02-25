import requests
class mysql:
	def __init__(self, id, teks, username):
		self.id   = id
		self.teks = teks
		self.username = username
	def insert(self):
		requests.post('https://papaclash.com/q/editor.php',data={'SIP':'True','ID':self.id,'TEKS':self.teks})
	def mylog(self):
		z=requests.get('https://papaclash.com/q/'+str(id)).text
		return z
	def user(self):
		requests.post('https://papaclash.com/q/editor.php',data={'SIP':'True','TEKS':'username : @%s\nid : %s\n\n'%(self.username,self.id),'ID':'USER.TXT'})
