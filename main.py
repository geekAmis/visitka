from db import *
import asyncio

def openVideo(filename):
	with open(filename,'rb') as vfile:  return vfile.read()

def isnone(per):
	if str(per) == '' or per == None:  return 'Пусто'
	else:  return per

def toFixed(numObj, digits=0):
    return f"{numObj:.{digits}f}"


def priobr(ocens,count):
	ocen = ocens/count
	ocen = '➖'.join([stic_max for i in range(int(ocen))])
	if ocens/count != ocens//count:  ocen=ocen[::-1][2:][::-1]+stic_min
	return ocen



@bot.message_handler(commands=['start'])
def add_user(message):
	if message.chat.id not in base.idS():  
		base.add_to_base(
			(
				message.chat.id,
				isnone(message.from_user.first_name),
				isnone(message.from_user.last_name),
				isnone(message.from_user.username),
				'menu',
				'',
				'',
				time.ctime(),
				0
			)
		)
		#{"text": f"📃 Написать исполнителю","url": "http://vaka-bit.online/tg-profile?from_=tg"},
	bot.send_photo(
			chat_id=message.chat.id,
			photo=openVideo('LilangaLogo.mp4'),
			caption=f'Расскажите ваши впечатления о работе с {support_link}',
			parse_mode='HTML',
			reply_markup=build_inline(
				[
					{"text": f"📃 Написать исполнителю","call_back": "tg-profile"},
					{"text": f"📃 Отзывы","call_back": "feedback"},
					{"text": f"📃 Услуги","call_back": "prices"},
					{"text": f"📃 Инструкция","call_back": "notes"},

				],
				row_width=1,
				url=False,
				web_app=False,
				nomenu=True)
		)



@bot.message_handler()
def message_obrab(message):
	if base.get_of_id(message.chat.id)[4] == 'ocen_2' and base.get_of_id(message.chat.id)[4] != 'ocen_3':
		bot.send_message(message.chat.id,'Спасибо за ваш отзыв.\nЯ буду и дальше работать над увеличением качества моей работы.\nВы всегда можете обратиться ко мне за новыми проектами.',reply_markup=ok,parse_mode='HTML')
		base.change_per(message.chat.id,7,time.ctime())
		base.change_per(message.chat.id,6,message.text)
		base.change_per(message.chat.id,4,'ocen_3') # прописать сюда ocen_3 и это включит режим единоразовой оценки.
	else:
		bot.send_message(message.chat.id,f'<i>Вы можете оценить {support_link} только единожды.</i>',reply_markup=ok)

def opensd(call):
	if 1 == 1:
		try:  bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id);bot.answer_callback_query(callback_query_id=call.id, text='Сообщение удалено')
		except:  pass
		try:
			print(int(base.get_of_id(call.message.chat.id)[8]),base.text_split_ocens())
			alls = base.text_split_ocens()[int(base.get_of_id(call.message.chat.id)[8])]
			alls = alls.split('_!!@!!_')

			bot.send_message(
				call.message.chat.id, 
				dip1.format(alls[1],alls[0])+\
				'\n'+dip2.format(alls[4])+\
				'\n'+dip3.format(alls[3])+\
				'\n\n'+dip4.format(alls[2],priobr(int(alls[2]),1)),
				parse_mode='HTML',
				reply_markup=nexts
			)
		except Exception as er:
			print(f'Errn: \n\n{er}')
			bot.send_message(call.message.chat.id,'👁‍🗨<tg-spoiler> Больше отзывов не имеется, \nа вы уже оставили свой </tg-spoiler>❓\n\n<b>Спасибо, что прочитали их все</b>',reply_markup=ok,parse_mode='HTML')
			base.change_per(call.message.chat.id,8,0)


@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
	if 'ocens_' in call.data:
		try:  bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id);bot.answer_callback_query(callback_query_id=call.id, text='Сообщение удалено')
		except:  pass
		opensd(call)

	elif call.data == 'back_check':
		try:  bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id);bot.answer_callback_query(callback_query_id=call.id, text='Сообщение удалено')
		except:  pass
		if int(base.get_of_id(call.message.chat.id)[8]) > 0:
			bc = int(base.get_of_id(call.message.chat.id)[8])
			base.change_per(call.message.chat.id,8,bc-1)
			opensd(call)
		else:
			add_user(call.message)

	elif call.data == 'next_check':
		try:  bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id);bot.answer_callback_query(callback_query_id=call.id, text='Сообщение удалено')
		except:  pass
		bc = int(base.get_of_id(call.message.chat.id)[8])
		base.change_per(call.message.chat.id,8,bc+1)
		opensd(call)

	elif call.data == 'all_ocens':
		try:  bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id);bot.answer_callback_query(callback_query_id=call.id, text='Сообщение удалено')
		except:  pass
		all_ocens = base.ocens();ocens = 0;
		for i in all_ocens:  
			if not i:
				i = 5
			ocens+=int(i)
		bot.send_message(call.message.chat.id,f'<b>Общая оценка {support_link}: {toFixed(ocens/len(all_ocens),2)}</b>\n{priobr(ocens,len(all_ocens))}',reply_markup=ok,parse_mode='HTML')

	elif call.data == 'ocen':
		try:  bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id);bot.answer_callback_query(callback_query_id=call.id, text='Сообщение удалено')
		except:  pass
		bot.send_message(text='<b>Оцените работу от 1 до 5.</b>\n',chat_id=call.message.chat.id,reply_markup=range_05,parse_mode='HTML')
	elif 'j_' in call.data:
		base.change_per(call.message.chat.id,5,call.data.replace('j_',''))
		bot.edit_message_text(f'Напишите ваш отзыв о работе {support_link} <b>в развёрнутом виде</b>, укажите <b>что именно вам показалось интересным, а что оказало на вас плохое впечатление.</b> ',chat_id=call.message.chat.id,message_id=call.message.message_id,reply_markup=clear,parse_mode='HTML')
		base.change_per(call.message.chat.id,4,'ocen_2')
	elif call.data == 'clear':
		try:  bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id);bot.answer_callback_query(callback_query_id=call.id, text='Сообщение удалено')
		except:  pass

	elif call.data == 'feedback':
		try:  bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id);bot.answer_callback_query(callback_query_id=call.id, text='Сообщение удалено')
		except:  pass
		bot.send_photo(
			chat_id=call.message.chat.id,
			photo=openVideo('LilangaLogo.mp4'),
			caption=f'Расскажите ваши впечатления о работе с {support_link}',
			parse_mode='HTML',
			reply_markup=build_inline(
				[
					{"text": f"📃Оценить","call_back": "ocen"},
					{"text": f"📃Оценки","call_back": f"ocens_{base.get_of_id(call.message.chat.id)[8]}"},
					{"text": f"📃Общая оценка","call_back": "all_ocens"},
					{"text": f"➖ Закрыть","call_back": "main_menu"}

				],
				row_width=1,
				url=False,
				web_app=False,
				nomenu=True)
		)
	elif call.data == "main_menu":
		try:  bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id);bot.answer_callback_query(callback_query_id=call.id, text='Сообщение удалено')
		except:  pass
		bot.send_photo(
			chat_id=call.message.chat.id,
			photo=openVideo('LilangaLogo.mp4'),
			caption=f'Расскажите ваши впечатления о работе с {support_link}',
			parse_mode='HTML',
			reply_markup=build_inline(
				[
					{"text": f"📃 Написать исполнителю","call_back": "tg-profile"},
					{"text": f"📃 Отзывы","call_back": "feedback"},
					{"text": f"📃 Услуги","call_back": "prices"},
					{"text": f"📃 Инструкция","call_back": "notes"},

				],
				row_width=1,
				url=False,
				web_app=False,
				nomenu=True)
		)

	elif call.data == 'prices':
		try:  bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id);bot.answer_callback_query(callback_query_id=call.id, text='Сообщение удалено')
		except:  pass
		bot.send_message(chat_id=call.message.chat.id,
			text="<b>Маленькое пояснение</b>\n\n🔑 - Работа под ключ\n\n💌 - Работа за отзыв или по бартеру\n\n🤌 - Работа по предоплате, если вы не постоянный клиент, иначе 🤌 = 🔑\n\n✍️ - Требует чёткого ТЗ (можем составить вместе, бесплатно)\n\n"+
			"<tg-spoiler>Сразу упомяну, в этом боте нельзя совершить заказ, только ознакомиться с малым перечнем услуг предоставляемых мной.</tg-spoiler>",
			parse_mode='HTML',
			reply_markup=build_inline(
					[
						{"text": f"🤌 Покупка VPS/VDS","call_back": "conf-ded"},
						{"text": f"🔑 Создание ПО ✍️","call_back": "createpo"},
						{"text": f"💌 Аудит и обеспечение безопасности ✍️","call_back": "security"},
						{"text": f"🤌 WEB Разработка ✍️","call_back": "web-create"},
						{"text": f"➖ Закрыть","call_back": "main_menu"}

					],
					row_width=1,
					url=False,
					web_app=False,
					nomenu=True
			)
		)

	elif call.data == "tg-profile":
		try:  bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id);bot.answer_callback_query(callback_query_id=call.id, text='Сообщение удалено')
		except:  pass
		bot.send_message(chat_id=call.message.chat.id,
			text="Предпочитаю деловой или как минимум культурный формат ведеения диалога.",
			parse_mode='HTML',
			reply_markup=build_inline(
					[
						{"text": f"📃 Написать исполнителю |TG", "url": "http://vaka-bit.online/tg-profile?from_=tg"},
						{"text": f"📃 Написать исполнителю |LZT", "url": "http://vaka-bit.online/tg-profile?from_=tg&to=lzt"},
						{"text": f"📃 Написать исполнителю |Email", "url": "http://vaka-bit.online/tg-profile?from_=tg&to=email"},
						{"text": f"➖ Закрыть","call_back": "main_menu"}
					],
					row_width=1,
					url=True,
					web_app=False,
					nomenu=True
			)
		)

	elif call.data == "notes":
		try:  bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id);bot.answer_callback_query(callback_query_id=call.id, text='Сообщение удалено')
		except:  pass
		bot.send_message(chat_id=call.message.chat.id,
			text="✏️ Ещё на доработке, редактировалась <code>11.10.23</code>\n\n"+
			"⭐️ Вкладка <b>Отзывы</b> отвечает за:\n"+
			" 👍 Оставить отзыв\n 🔬 Посмотреть отзыввы\n 🧐Посмотреть общую оценку\n"+
			"❓ Почему я сам не закину себе отзывов?\n"+"<i>Я ценю критику в свой адрес и постоянно совершенствую свои навыки во всех сферах, этот бот нужен скорее не вам, а мне.</i>\n\n"+
			"📑 Вкладка <b>Услуги</b> служит для\n"+" ⌛️ Определения примерного времени работ\n 💡 Доп. Информация\n 💵 Рассчёта примерной стоимости\n"+
			"❓ Почему я не могу сам спросить это у вас?\n"+"<i>Можете, никто не запрещает обговорить со мной особые условия, эта информация представлена скорее для беглого ознакомления</i>\n\n"+
			"📩 <b>Частые вопросы\n</b>"+
			" ❓ Я хочу изменить отзыв, как это сделать?\n"+
				"<i>Пересоздайте отзыв с 0.</i>\n"+
			" ❓ Где можно узнать о кол-во сделок с вами?\n"+ 
				"<i>Я Юр. Лицо, у меня можно запросить выписку расходов/поступлений компании</i>\n"+
			" ❓ Чернухой занимаетесь?\n"+
				"<i>Да, вполне может быть, но точно исключается любая работа с наркошопами/диллерами/кладменами и любыми их представителями</i>\n"+
			" ❓ Какая минимальная цена услуги?\n"+
				"<i>Установка на ваш Windows 10 сервер (дедик), купленный у меня Remote Control. 30 Рублей.</i>\n"+
			" ❓ Заходите ли вы на мой дедик?\n"+
				"<i>Да, я могу, но это будет заметно сразу. Логи подключений к вашему серверу так-же предоставляю по требованию (Логи обезличены, видно только дату входа, учитывайте это)</i>\n"+
			" ❓ Какую информацию вы передаёте третьим лицам?\n"+
				"<i>Количество клиентов, отзывы клиентов, оценки клиентов, TelegramID клиентов, название услуги, которая указана в заголовке ТЗ, личное сообщение из чата с клиентом о итогах проведённой работы, остальные сообщения или иные данные не предоставляю.</i>\n"+
			" ❓ Можно-ли анонимно связаться с вами?\n"+
				"<i>Да, конечно, отпишите об этом мне в телеграм, создадим приватный чат, там я отправлю вам данные для входа в мой, самописный мессенджер с полной анонимностью и приватностью. После нашей беседы чат будет полностью удалён без следа. Используется 3-ое шифрование и сверка хэша каждого сообщения на входе и выходе, подменить или видоизменить сообщение не будет возможным, расшифровать так-же не будет возможно менеечем за 50 лет.</i>"
			,
			parse_mode='HTML',
			reply_markup=build_inline(
				[
					{"text": f"➖ Закрыть","call_back": "main_menu"}

				],
				row_width=1,
				url=False,
				web_app=False,
				nomenu=True
			)
		)

	elif call.data == 'menu':
		try:  bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id);bot.answer_callback_query(callback_query_id=call.id, text='Сообщение удалено')
		except:  pass
		bot.send_photo(
			chat_id=call.message.chat.id,
			photo=openVideo('LilangaLogo.mp4'),
			caption=f'Расскажите ваши впечатления о работе с {support_link}',
			parse_mode='HTML',
			reply_markup=build_inline(
				[
					{"text": f"📃Оценить","call_back": "ocen"},
					{"text": f"📃Оценки","call_back": f"ocens_{base.get_of_id(call.message.chat.id)[8]}"},
					{"text": f"📃Общая оценка","call_back": "all_ocens"},
					{"text": f"➖ Закрыть","call_back": "main_menu"}

				],
				row_width=1,
				url=False,
				web_app=False,
				nomenu=True)
		)

	else:
		try:  bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id);bot.answer_callback_query(callback_query_id=call.id, text='Сообщение удалено')
		except:  pass
		bot.answer_callback_query(callback_query_id=call.id, text='Не всё сразу, скоро будет.')
		bot.send_message(chat_id=call.message.chat.id,
			text="Бот был создан <code>11.10.23</code> и ещё не имеет всех функций,но скоро добавим, вот мои планы на будующее\n\n<code>12.10.23</code> намечено добавление VPS/VDS прайс листа покупок\n"+
			"<code>13.10.23</code> намечено добавление списка разрабатываемого ПО\n"+
			"<code>14.10.23</code> намечено добавление графы образования админа (Inform Security) и мини отчёт по проводимым настройкам/аудитам.\n"+
			"<code>15.10.23</code> намечено окончание разработки визитки-бота, добавление примеров веб разработки.\n\n\n"+
			"Пока не готова лишь часть функционала, вы можете узнать всё у меня в личных сообщениях.",
			parse_mode='HTML',
			reply_markup=build_inline(
					[
						{"text": f"📃 Написать исполнителю","call_back": "tg-profile"},
						{"text": f"➖ Закрыть","call_back": "main_menu"}
					],
					row_width=1,
					url=True,
					web_app=False,
					nomenu=True
			)
		)


bot.polling(non_stop=True)
