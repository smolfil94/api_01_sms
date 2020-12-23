import os
import requests
import time

from twilio.rest import Client
from dotenv import load_dotenv
load_dotenv()

URL = 'https://api.vk.com/method/users.get'


def get_status(user_id):
    access_token = os.getenv('VK_TOKEN')
    params = {
        'user_ids': user_id,
        'fields': 'online',
        'v': '5.92',
        'access_token': access_token
    }
    status = requests.post(URL, params=params)
    return status.json()['response'][0]['online']  # Верните статус пользователя в ВК


def sms_sender(sms_text):
    account_sid = os.getenv('ACCOUNT_SID')
    auth_token = os.getenv('AUTH_TOKEN')
    client = Client(account_sid, auth_token)
    number_from = os.getenv('NUMBER_FROM')
    number_to = os.getenv('NUMBER_TO')
    message = client.messages.create(
        body=sms_text,
        from_=number_from,
        to=number_to
    )
    return message.sid  # Верните sid отправленного сообщения из Twilio


if __name__ == '__main__':
    # тут происходит инициализация Client
    vk_id = input('Введите id ')
    while True:
        if get_status(vk_id) == 1:
            sms_sender(f'{vk_id} сейчас онлайн!')
            break
        time.sleep(5)
