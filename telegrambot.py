import requests
import time

API_TOKEN = '6184059120:AAG_l2CjEchcrHatL8Jzb1u3Ott-WPEgcqA'
CHAT_ID = '726897147'

# Função para obter as atualizações do Telegram


def get_updates():
    url = f'https://api.telegram.org/bot{API_TOKEN}/getUpdates'
    response = requests.get(url)
    data = response.json()
    return data

# Função para enviar uma mensagem para o Telegram


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

# Função para executar a ação desejada


def perform_action():
    # Coloque sua ação aqui
    # Exemplo: enviar uma mensagem para o grupo
    send_message("Mensagem lida!")

# Função para controlar a ação

# Função para processar a mensagem recebida


def process_message(message):
    if 'text' in message:
        # Extrai o nome do remetente
        sender_name = message['from']['first_name']
        # Extrai o conteúdo da mensagem
        text = message['text']
        # Imprime o conteúdo da mensagem
        print(f"{sender_name}: {text}")
    else:
        print("Mensagem enviada não é um texto!")
# Função para controlar a ação


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


# Iniciar o controle da ação
control_action()
