#!/usr/bin/python 
from transformers import pipeline
import telebot

token= '6968662842:AAF6j6Pxy3cNbntdrhD1zlawnFD2lPJXFds'

bot=telebot.TeleBot(token)


@bot.message_handler(content_types='text')
def message_reply(message):
    bot.send_message(message.chat.id,str(message.chat.id))

'''
@bot.message_handler(commands=["geo"])
def geo(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_geo = types.KeyboardButton(text="Отправить местоположение", request_location=True)
    keyboard.add(button_geo)
    bot.send_message(message.chat.id, "Привет! Нажми на кнопку и передай мне свое местоположение", reply_markup=keyboard)
'''

@bot.message_handler(content_types=["location"])
def location(message):
    if message.location is not None:
        print(message.location)
        print("latitude: %s; longitude: %s" % (message.location.latitude, message.location.longitude))
        bot.send_message(message.chat.id,str("latitude: %s; longitude: %s" % (message.location.latitude, message.location.longitude)))

'''
def AI_example():
    clf = pipeline(
        task = 'sentiment-analysis', 
        model = 'SkolkovoInstitute/russian_toxicity_classifier')

    text = ['У нас в есть убунты и текникал превью.']

    print(clf(text))
'''
bot.infinity_polling()