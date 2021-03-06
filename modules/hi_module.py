# modules/hi_module.py
from app.mac import mac, signals
import config
import apiai
import uuid
import numpy
import json
import difflib

client_token = config.client["token"]
client_word = config.client["word"]

@signals.message_received.connect
def handle(message):
        index = message.who.index('@')
        who_number = message.who[:index]
        who_name = message.who_name

        session_id = who_number
        request = apiai.ApiAI(client_token).text_request() # Токен API к Dialogflow
        request.lang = 'ru' # На каком языке будет послан запрос
        request.session_id = session_id # ID Сессии диалога (нужно, чтобы потом учить бота)
        request.query = message.text # Посылаем запрос к ИИ с сообщением от юзера
        responseJson = json.loads(request.getresponse().read().decode('utf-8'))
        response = responseJson['result']['fulfillment']['messages'][0]['speech']
        mac.send_message(response, message.conversation)
        
        if message.text == "@":
                link_whatsapp = "https://wa.me/" + who_number
                text_msg = "Заявка из Whatsapp\nИмя: " + who_name + "\nНомер: " + who_number + "\nНачать чат: " + link_whatsapp

                for contact in config.contacts.keys():
                        mac.send_message_to(text_msg, contact)

        seq = difflib.SequenceMatcher(a=client_word.lower(), b=message.text.lower())
        
        if seq.ratio() >= 0.5:
                link_whatsapp = "https://wa.me/" + who_number
                text_msg = "Начат чат с ботом\nИмя: " + who_name + "\nНомер: " + who_number + "\nНачать чат: " + link_whatsapp

                for contact in config.contacts.keys():
                        mac.send_message_to(text_msg, contact)
        # Can also send media
        #mac.send_image("path/to/image.png", message.conversation)
        #mac.send_video("path/to/video.mp4", message.conversation)