# modules/hi_module.py
from app.mac import mac, signals
import config
import apiai
import uuid
import numpy
import json

client_token = config.client["token"]
client_phone = config.client["phone"]

@signals.message_received.connect
def handle(message):
        if message.text == "@":
                index = message.who.index('@')
                who_number = message.who[:index]
                who_name = message.who_name

                link_whatsapp = "https://wa.me/" + who_number
                text_msg = "Заявка из Whatsapp\nИмя: " + who_name + "\nНомер: " + who_number + "\nНачать чат: " + link_whatsapp

                for contact in config.contacts.keys():
                        mac.send_message_to(text_msg, contact)

        session_id = str(uuid.uuid4())
        request = apiai.ApiAI(client_token).text_request() # Токен API к Dialogflow
        request.lang = 'ru' # На каком языке будет послан запрос
        request.session_id = session_id # ID Сессии диалога (нужно, чтобы потом учить бота)
        request.query = message.text # Посылаем запрос к ИИ с сообщением от юзера
        responseJson = json.loads(request.getresponse().read().decode('utf-8'))
        response = responseJson['result']['fulfillment']['messages'][0]['speech']
        mac.send_message(response, message.conversation)
        
        # Can also send media
        #mac.send_image("path/to/image.png", message.conversation)
        #mac.send_video("path/to/video.mp4", message.conversation)