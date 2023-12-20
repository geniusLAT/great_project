#!/usr/bin/python 
from transformers import pipeline
import telebot
import Gmap

import ourAI

user_datas=[]

class user_data(object):
    def __init__(self,id) -> None:
        self.latitude=None
        self.longitude=None

        self.request= None
        self.user_id=id

    def set_coordinate(self,lat,lon):
        self.latitude=lat
        self.longitude=lon

    def set_request(self, request):
        self.request=request

    def check(self):
        return (self.longitude!=None) and(self.latitude!=None) and (self.request!=None) 

def get_user_data(id):
    ud = None
    for data in user_datas:
        if data.user_id==id:
            ud=data

    if ud==None:
        ud = user_data(id)
        user_datas.append(ud)
    return ud

token= '6968662842:AAF6j6Pxy3cNbntdrhD1zlawnFD2lPJXFds'

bot=telebot.TeleBot(token)


def process(ud):
    print("process")

    places=    Gmap.get_nameful_array(ud.latitude,ud.longitude)

    result = ourAI.request_AI(ud.request,places)

    bot.send_message(ud.user_id,result)

    ud.request=None #user has not to send location twice, but has to send request only once
    #it lets him to send multiple requests about one locations. And it forbids to send 
    #multiple locations for one requests. 

    return str(result)


@bot.message_handler(content_types='text')
def message_reply(message):
    ud = get_user_data(message.chat.id)
    ud.set_request(message.text)
    if ud.check():
        bot.send_message(message.chat.id,str('Бот работает. Ожидайте'))
        process(ud)
    else:
        bot.send_message(message.chat.id,str('Пришлите локацию через телеграм'))

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
        #bot.send_message(message.chat.id,str("latitude: %s; longitude: %s" % (message.location.latitude, message.location.longitude)))
        ud = get_user_data(message.chat.id)
        ud.set_coordinate(message.location.latitude,message.location.longitude)
        if ud.check():
            bot.send_message(message.chat.id,str('Бот работает. Ожидайте'))
            process(ud)
        else:
            bot.send_message(message.chat.id,str('Напишите ваш текстовый запрос'))

'''
def AI_example():
    clf = pipeline(
        task = 'sentiment-analysis', 
        model = 'SkolkovoInstitute/russian_toxicity_classifier')

    text = ['У нас в есть убунты и текникал превью.']

    print(clf(text))
'''
bot.infinity_polling()