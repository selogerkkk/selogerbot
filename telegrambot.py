import os
import requests
import time
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv('API_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')


def get_updates():
    url = f'https://api.telegram.org/bot{API_TOKEN}/getUpdates'
    response = requests.get(url)
    data = response.json()
    return data


def send_message(text):
    url = f'https://api.telegram.org/bot{API_TOKEN}/sendMessage'
    params = {'chat_id': CHAT_ID, 'text': text}
    response = requests.post(url, json=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(
            f"Erro ao enviar a mensagem: {response.status_code} - {response.text}")
        return None


def perform_action():
    send_message("Mensagem lida!")


def process_message(message):
    if 'text' in message:
        sender_name = message['from']['first_name']
        text = message['text']
        print(f"{sender_name}: {text}")
    else:
        print("Mensagem enviada não é um texto!")


def control_action():
    action_counter = 0
    while True:
        updates = get_updates()
        if 'result' in updates:
            results = updates['result']
            if results:
                last_message = results[-1]['message']
                last_message_id = last_message['message_id']
                if last_message_id != action_counter:
                    action_counter = last_message_id
                    process_message(last_message)
                    perform_action()

        time.sleep(1)


control_action()
