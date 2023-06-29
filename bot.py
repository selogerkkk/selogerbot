import os
import requests
import time
from dotenv import load_dotenv
import datetime
from iqoptionapi.stable_api import IQ_Option

load_dotenv()

API_TOKEN = os.getenv('API_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')
email = os.getenv('email')
password = os.getenv('senha')

#bot login
iq = IQ_Option(email, password)
check, reason = iq.connect()  # connect to iqoption

if iq.check_connect() == True:
    print(datetime.datetime.now().strftime("%H:%M"))
    print("Conta conectada.")
    print("Bem vindo de volta.")
    print("Você está na conta:", iq.get_balance_mode())
    print("Seu saldo é:", iq.get_balance())
    print("\n")
else: 
    print(datetime.datetime.now().strftime("%H:%M"))
    print("Erro ao logar. Tente novamente.")


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
        result = {}
        # Extrai o nome do remetente
        sender_name = message['from']['first_name']
        # Extrai o conteúdo da mensagem
        texto = message['text']
        if "✅🔥 TRADERZISMO FREE 🔥✅" in texto:
            #print(f"Texto da mensagem:\n {texto}\n\n")
            
            # Encontrar o par (EURUSD)
            indice_inicio_par = texto.find('📊') + 2
            indice_fim_par = texto.find('\n', indice_inicio_par)
            par = texto[indice_inicio_par:indice_fim_par]
            result['par']= par

            # Encontrar a direção (PUT ou CALL)
            palavras_chave_direcao = {
                'PUT': '🔴',
                'CALL': '🟢'
            }
            direcao_encontrada = None
            for direcao, emoji in palavras_chave_direcao.items():
                if emoji in texto:
                    indice_inicio_direcao = texto.find(emoji) + 2
                    indice_fim_direcao = texto.find('\n', indice_inicio_direcao)
                    direcao_encontrada = direcao
                    result['direcao'] = direcao_encontrada
                    break

            if not direcao_encontrada:
                print("Direção não encontrada.")

            # Encontrar o horário (Operar AGORA)
            indice_inicio_horario = texto.find('⚠️ Operar ') + 10
            indice_fim_horario = texto.find(' ⚠️', indice_inicio_horario)
            horario = texto[indice_inicio_horario:indice_fim_horario]
            if horario.upper() == 'AGORA':
                horario = datetime.datetime.now().strftime("%H:%M")
            result['horario'] = horario
                           
            amount = 1
            duration = 1

            Money=[]
            ACTIVES=[]
            ACTION=[]
            expirations_mode=[]

            Money.append(amount)
            ACTIVES.append(par)
            ACTION.append(direcao)
            expirations_mode.append(duration)
            
            # operaçao
            
            id_list=iq.buy_multi(Money,ACTIVES,ACTION,expirations_mode)
            if id_list == [None]:
                print(datetime.datetime.now().strftime("%H:%M"))
                print(sender_name)
                print(texto)
                print(result)
                print("Operação falhou.")
            else:
                send_message("Entrando na operação...//")
                print('Entrando na operação...')
                print(datetime.datetime.now().strftime("%H:%M"))
                print(sender_name)
                print(texto)
                print(result)
                print("ID da operação:", id_list)
                print("\n")
        else:
            print(datetime.datetime.now().strftime("%H:%M"))
            print(sender_name)
            print(texto)
            print("Não tá no formato.")
    
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
                    time.sleep(1)


# Iniciar
control_action()
