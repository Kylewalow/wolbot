import config
import telebot
from telebot import types
import time
import os

bot_token = config.token
cid =  config.chat_id
serverIp = config.ip
hulkMac = config.mac

bot = telebot.TeleBot(bot_token, parse_mode=None)
menuKeyboard = types.InlineKeyboardMarkup()
menuKeyboard.add(types.InlineKeyboardButton('Server Status', callback_data='status'), types.InlineKeyboardButton('Start Plex-Server', callback_data='start'))


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    sentMessage = bot.reply_to(message, "Ahoy")

    if cid != message.chat.id:
        bot.edit_message_text("Wrong chat for this command", sentMessage.chat.id, sentMessage.message_id)
        return

    response = os.system("ping -c 1 " + serverIp)
    print(response)
    if response == 0:
        bot.edit_message_text("Plex server is up", sentMessage.chat.id, sentMessage.message_id)
    else:
        bot.edit_message_text("Starting plex server...", sentMessage.chat.id, sentMessage.message_id)

    waittime = 3

    while response != 0 and waittime >= 0:
        os.system("sudo etherwake "+ serverIp)
        time.sleep(1)
        response = os.system("ping -c 1 " + serverIp)

        if response != 0 and waittime > 0:
            bot.edit_message_text(waittime, sentMessage.chat.id, sentMessage.message_id)
        if  response != 0 and waittime <= 0:
            bot.edit_message_text("Server still down, please try again or contact the server admin", sentMessage.chat.id, sentMessage.message_id)
        if response == 0:
            bot.edit_message_text("Server is running", sentMessage.chat.id, sentMessage.message_id)

        waittime -= 1

bot.infinity_polling()
