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
        texto = message['text']
        print(f"Texto da mensagem:\n {texto}\n\n")
        # Encontrar o par (AUDJPY)
        indice_inicio_par = texto.find('📊') + 2
        indice_fim_par = texto.find('\n', indice_inicio_par)
        par = texto[indice_inicio_par:indice_fim_par]

        # Encontrar a direção (CALL ou PUT)
        palavras_chave_direcao = ['CALL', 'PUT']
        indice_inicio_direcao = None
        indice_fim_direcao = None
        for palavra in palavras_chave_direcao:
            if palavra in texto:
                indice_inicio_direcao = texto.find(palavra) + len(palavra) + 1
                indice_fim_direcao = texto.find('\n', indice_inicio_direcao)
                break

        direcao = texto[indice_inicio_direcao:indice_fim_direcao]

        # Encontrar o horário (10:45)
        indice_inicio_horario = texto.find('Operar ') + 7
        indice_fim_horario = texto.find('⚠️', indice_inicio_horario)
        horario = texto[indice_inicio_horario:indice_fim_horario]
        if horario == ' AGORA':
          horario = datetime.datetime.now().strftime("%H:%M")
        print("Par:", par)
        print("Direção:", direcao)
        print("Horário:"    , horario)

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
