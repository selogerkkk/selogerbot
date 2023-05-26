import os
import requests
import time
from dotenv import load_dotenv
import re
import datetime

load_dotenv()

API_TOKEN = os.getenv('API_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')

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


# Função para enviar mensagem
def perform_action():
    send_message("Mensagem lida!")


# Função para processar a mensagem recebida sem filtro
def process_message_without_filter(message):
    if 'text' in message:
        # Extrai o nome do remetente
        sender_name = message['from']['first_name']
        # Extrai o conteúdo da mensagem
        text = message['text']
        print(f"Texto da mensagem: {text}")

        # Imprime o conteúdo da mensagem
        print(f"{sender_name}: {text}")
    else:
        print("Mensagem enviada não é um texto!")


def process_message(message):
    # Verifica se a mensagem contém texto
    if 'text' in message:
        # Extrai o nome do remetente
        sender_name = message['from']['first_name']
        # Extrai o conteúdo da mensagem
        text = message['text']
        
        # Verifica se a mensagem contém o padrão específico
        if "✅🔥 TRADERZISMO FREE 🔥✅" in text:
            # Procura um padrão específico na mensagem usando expressões regulares
            pattern = r"📊 ([^\n]+)\n(🔴 PUT|🟢 CALL)?\n⚠️ Operar (AGORA|\d{2}:\d{2})"
            match = re.search(pattern, text)
            
            # Verifica se o padrão foi encontrado
            if match:
                # Extrai as informações desejadas
                par = match.group(1).strip()
                direcao = match.group(2).strip() if match.group(2) else "N/A"
                horario = match.group(3).strip() if match.group(3) != "AGORA" else  datetime.datetime.now().strftime("%H:%M")
                # Imprime as informações com o nome do remetente
                print(f"Mensagem recebida de {sender_name}:")
                print(f"Par: {par}")
                print(f"Direção: {direcao}")
                print(f"Horário: {horario}")
            else:
                print("Padrão não encontrado na mensagem.")
        else:
            print("Mensagem não contém o padrão esperado.")

# Função para não repetir a mensagem

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


# Iniciar
control_action()
