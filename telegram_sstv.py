'''
This is a simple bot to use telegram API to create and read SSTV voice signal.

@package telegram_sstv
'''

import pysstv as sstv
import telebot

from config import *


# Init bots.
## Enable proxy if configured
if(bot_enable_proxy):
    telebot.apihelper.proxy = bot_proxy

bot = telebot.TeleBot(bot_api_token, num_threads=bot_threads_num)

# Help info
@bot.message_handler(content_types=['text'], commands=['start', 'help'])
def send_hello(message):
    bot.reply_to(message, "Send me picture then I'll convert it to a SSTV video file.")

# Encode picture
@bot.message_handler(content_types=['photo'])
def sstv_encode(message):
    print(message.photo)

bot.polling()
