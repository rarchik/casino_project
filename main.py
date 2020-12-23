import vk_api
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import datetime 
import time

vk = vk_api.VkApi(token="069bd91de21599fde85c0c056f1f3a16aa20d06acaf62bdeccef4d71352b98dbacefabeeadf9239e728e7")

keyboard1 = VkKeyboard(one_time=True)

keyboard1.add_button('Следующая ставка', color=VkKeyboardColor.POSITIVE)
keyboard1.add_button('Закончить', color=VkKeyboardColor.NEGATIVE)



base = {}

def rar(stav):
	t = 40
	i = 0
	y = 0
	u = 2
	nstav = stav
	sum = 0
	ans = ''
	s = []

	while 0 < sum+stav*40:
		if y == t-1:
			t = 40 // u
			y = 0
			stav += nstav
			u += 1
		
		sum -= stav

		i += 1
		y += 1
		if i > 200:
			break

		s.append('№'+str(i)+'. Ставка - '+str(stav)+'. Потрачено - '+str(-sum)+'.')

	return s, -sum 

"""

1 - вводит ставку
2 - смотрит ставки

"""

while True:
	messages = vk.method("messages.getConversations", {"offset": 0, "count": 20,"filter":"unread"})

	if messages["count"] >= 1:
		messages = vk.method("messages.getConversations", {"offset": 0, "count": 20,"filter":"unread"})
		id = messages["items"][0]["last_message"]["from_id"]
		body = messages["items"][0]["last_message"]["text"]
		h = vk.method('users.get',{'user_ids':id,'name_case':'Nom'})

		timestamp = time.time()
		value = datetime.datetime.fromtimestamp(timestamp)
		

		if id not in base.keys():
			print('New in base')
			base.update([(id, {'stat':1, 'nstav':0, 'stav':[]})]) 
			vk.method("messages.send", {"peer_id": id, "message": 'Введите ставку для начала:','random_id':0})
		
		else:
			print(value.strftime('%Y-%m-%d %H:%M:%S'),'-',body,' - ',id, ' - ',h[0]['first_name']+' '+h[0]['last_name'], base[id]['stat'], base[id]['nstav'])
			if base[id]['stat'] == 1:
				try:
					base[id]['stav'], ob = rar(int(body))
					vk.method("messages.send", {"peer_id": id, "message": 'Просчитано '+ str(len(base[id]['stav']))+' ставки. Общая сумма прокрутов '+str(ob)+' $.', 'keyboard': keyboard1.get_keyboard(), 'random_id':0})
					base[id]['stat'] = 2
				except Exception as err:
					print(err)
					vk.method("messages.send", {"peer_id": id, "message": 'Введите число:','random_id':0})
			elif base[id]['stat'] == 2:
				if body == 'Следующая ставка':
					if base[id]['nstav'] >= len(base[id]['stav']):
						vk.method("messages.send", {"peer_id": id, "message": 'Ставок больше нету.', 'random_id':0})
						vk.method("messages.send", {"peer_id": id, "message": 'Введите ставку:','random_id':0})
						base[id]['stat'] = 1
					else:	
						vk.method("messages.send", {"peer_id": id, "message": base[id]['stav'][base[id]['nstav']], 'keyboard': keyboard1.get_keyboard(), 'random_id':0})
						base[id]['nstav'] += 1

				elif body == 'Закончить':
					vk.method("messages.send", {"peer_id": id, "message": 'Введите ставку:','random_id':0})
					base[id]['stat'] = 1
					base[id]['nstav'] = 0



