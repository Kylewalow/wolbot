import config
import telebot
from telebot import types
import time
import os

bot_token = config.token
cid =  config.chat_id
hulkServerIp = config.ip

bot = telebot.TeleBot(token=bot_token)
menuKeyboard = types.InlineKeyboardMarkup()
menuKeyboard.add(types.InlineKeyboardButton('Server Status', callback_data='status'), types.InlineKeyboardButton('Start Plex-Server', callback_data='start'))

@bot.message_handler(commands=['start', 'verwache', 'wachufdusiech', 'wachaentlechufman', 'ufwache'])
def send(message):
    if cid == message.chat.id:    
        bot.send_message(cid, 'What would you like to do?', reply_markup=menuKeyboard)
    else:
        bot.reply_to(message,'You dont have permission for this command')

@bot.callback_query_handler(lambda query: query.data == 'status')
def status(query):
    response = os.system("ping -c 1 " + hulkServerIp)
    if response == 0:
        bot.send_message(cid, 'Server is running🤙')
    else:
        bot.send_message(cid, 'Server is down😴')

@bot.callback_query_handler(lambda query: query.data == 'start')
def start(query): 
    response = os.system("ping -c 1 " + hulkServerIp) 
    waittime = 1
    bot.send_message(cid, 'Roger, im gona wake it up!🥁')
    while response != 0 and waittime <= 15:
        os.system("etherwake D0:50:99:1C:0E:01")
        time.sleep(1)
        waittime += 1
        response = os.system("ping -c 1 " + hulkServerIp) 

    if response != 0 and waittime >= 15:
        bot.send_message(cid, '''I couldnt handl'e to wakeup the server😑''')

    if response == 0:
        bot.send_message(cid, 'All right. The server is running😁')

@bot.message_handler(commands=['help'])
def help(message):
    if cid == message.chat.id:    
        bot.reply_to(message, 'Enter: /start')

while True:
    try:
        bot.polling(interval=1)
    except Exception:
        time.sleep(15)