'''
This is a simple bot to use telegram API to create and read SSTV voice signal.

@package telegram_sstv
'''

import pysstv.color as sstvutil
import telebot
import requests
import os
from io import BytesIO
from PIL import Image, ImageOps

from config import *


# Init bots.
## Enable proxy if configured
if(bot_enable_proxy):
    telebot.apihelper.proxy = bot_proxy

bot = telebot.TeleBot(bot_api_token, num_threads=bot_threads_num)

# Resize Image
def resize_img_with_padding(picture: Image, width: int, height: int) -> Image:
    original_size = picture.size
    ratio = min(float(width)/picture.width, float(height)/picture.height)
    new_size = tuple([int(x*ratio) for x in original_size])
    resized = Image.new("RGB", (width, height))
    resized.paste(picture.resize(new_size, Image.ANTIALIAS), ((width-picture.width)//2, (width-picture.width)//2))
    return resized

# SSTV helper function
def sstv_convert(picture: Image) -> BytesIO :
    result = BytesIO()
    sstv = sstvutil.Robot36(resize_img_with_padding(picture, 320, 240), 48000, 16)
    sstv.write_wav(result)
    return result

# Help info
@bot.message_handler(content_types=['text'], commands=['start', 'help'])
def send_hello(message):
    bot.reply_to(message, "Send me picture then I'll convert it to a SSTV video file.")

# Encode picture
@bot.message_handler(content_types=['photo'])
def sstv_encode(message):
    # Get file from message
    file_url = bot.get_file_url(message.photo[0].file_id)
    received_img = Image.open(BytesIO(requests.get(file_url).content))

    convert_result = sstv_convert(received_img)
    convert_result.seek(0)
    print(convert_result)
    bot.send_document(message.chat.id, convert_result.read(), reply_to_message_id = message.message_id)
    print(convert_result)
    convert_result.close()
    received_img.close()

bot.polling(none_stop=True)
