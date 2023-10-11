import sqlite3,random,time,requests,os
from bs4 import BeautifulSoup as bs
from telebot import *

# Общие функции

def build_inline(data,row_width='',nomenu=False,url=False,web_app=False):
	# [{"text": "tet", "call_back": "tet"}]
	
	if url and web_app:
		data = [types.InlineKeyboardButton(text=f'{i["text"]}',web_app=types.WebAppInfo(i['url'])) for i in data]
	elif not url and not web_app:
		data = [types.InlineKeyboardButton(text=f'{i["text"]}',callback_data=f'{i["call_back"]}') for i in data]
	elif url and not web_app:
		data = [types.InlineKeyboardButton(text=f'{i["text"]}',url=f'{i["url"]}') if i.get('url') else types.InlineKeyboardButton(text=f'{i["text"]}',callback_data=f'{i["call_back"]}') for i in data]
		
	if not nomenu:
		data.append(types.InlineKeyboardButton(text='В меню ↗️', callback_data='menu'))

	if row_width != '':
		return types.InlineKeyboardMarkup(row_width=row_width).add(*data)
	return types.InlineKeyboardMarkup().add(*data)

clear = types.InlineKeyboardMarkup().add(*[
	types.InlineKeyboardButton(text='🗑 Удалить',callback_data='clear')
])
ok = types.InlineKeyboardMarkup().add(*[
	types.InlineKeyboardButton(text='👌 Ok',callback_data='menu')
])

range_05 = types.InlineKeyboardMarkup().add(*[
	types.InlineKeyboardButton(text='🌟 1 🌟',callback_data='j_1'),
	types.InlineKeyboardButton(text='🌟 2 🌟',callback_data='j_2'),
	types.InlineKeyboardButton(text='🌟 3 🌟',callback_data='j_3'),
	types.InlineKeyboardButton(text='🌟 4 🌟',callback_data='j_4'),
	types.InlineKeyboardButton(text='🌟 5 🌟',callback_data='j_5')
])

nexts = types.InlineKeyboardMarkup().add(*[
	types.InlineKeyboardButton(text='⬅️',callback_data='back_check'),
	types.InlineKeyboardButton(text='⛔️',callback_data='feedback'),
	types.InlineKeyboardButton(text='➡️',callback_data='next_check')
])

# Общие переменные.
token = '6189221266:AAG23C80KcacyIDn1x6wCFUA5sgt_ssm228'
admin = 5091972921
support_link = '@Lilanga'
bot = TeleBot(token)

stic_min = '✨'
stic_max = '⭐️'
dip1 = 'Пользователь <tg-spoiler><i>{}</i></tg-spoiler> (<b>ID</b><code>{}</code>)'
dip2 = 'Time: {}\n'
dip3 = '<b>Оставил отзыв:</b> \n{}\n'
dip4 = '<b>Оценка:</b> <code>{}</code> \n{}'
