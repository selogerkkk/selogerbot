import sys
import time
from telethon.sync import TelegramClient
from telethon import events
import threading
import asyncio
import os
from dotenv import load_dotenv
import datetime
from iqoptionapi.stable_api import IQ_Option
load_dotenv()

API_ID = '12093312'
API_HASH = '67926450017650430bfc865ad771523d'
# CHAT_ID = '-1001474420372'  # traderzismo
CHAT_ID = '-1001864670859'

email = os.getenv('email')
password = os.getenv('senha')

mensagem = ''
msg = ''

# bot login
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

stoploss = 2
stopwin = 2
saldo = 0


def check_win_loss(id_list, result, tipo_operacao):
    global stoploss, stopwin, saldo

    if tipo_operacao == 'binaria':
        if iq.check_win_v3(id_list) != None:
            print(result['par'])
            print(result['direcao'])
            print(result['horario'])
            resultado_binaria = iq.check_win_v3(id_list)
            print("resultado da operação: {:.2f}".format(resultado_binaria))
            saldo += resultado_binaria
    if tipo_operacao == 'digital':
        print(result['par'])
        print(result['direcao'])
        print(result['horario'])
        op_digital = iq.check_win_digital(id_list, 2)
        print("resultado da operação: {:.2f}".format(op_digital))
        saldo += op_digital
    print("\nSaldo das operaçoes: {:.2f}".format(saldo))


def loop_conexao():
    with TelegramClient('session_name', API_ID, API_HASH) as client:
        @client.on(events.NewMessage)
        async def armazenar_mensagem(event):
            global mensagem
            global msg
            if event.is_group and str(event.chat_id) == CHAT_ID:
                texto = event.message.text

                result = {}

                if "TRADERZISMO FREE" in texto:
                    # print(f"Texto da mensagem:\n {texto}\n\n")

                    # Encontrar o par (EURUSD)
                    indice_inicio_par = texto.find('📊') + 2
                    indice_fim_par = texto.find('\n', indice_inicio_par)
                    par = texto[indice_inicio_par:indice_fim_par]
                    result['par'] = par

                    # Encontrar a direção (PUT ou CALL)
                    palavras_chave_direcao = {
                        'PUT': '🔴',
                        'CALL': '🟢'
                    }
                    direcao_encontrada = None
                    for direcao, emoji in palavras_chave_direcao.items():
                        if emoji in texto:
                            indice_inicio_direcao = texto.find(emoji) + 2
                            indice_fim_direcao = texto.find(
                                '\n', indice_inicio_direcao)
                            direcao_encontrada = direcao
                            result['direcao'] = direcao_encontrada
                            break

                    if not direcao_encontrada:
                        print("Direção não encontrada.")

                    # Encontrar o horário (Operar AGORA)
                    indice_inicio_horario = texto.find('⚠️ Operar ') + 10
                    # indice_fim_horario = texto.find('⚠️', indice_inicio_horario)
                    horario = texto[indice_inicio_horario:(
                        indice_inicio_horario+5)]
                    if horario.upper() == 'AGORA':
                        horario = datetime.datetime.now().strftime("%H:%M")
                    result['horario'] = horario

                    amount = 1
                    duration = 1

                    Money = []
                    ACTIVES = []
                    ACTION = []
                    expirations_mode = []

                    Money.append(amount)
                    ACTIVES.append(par)
                    ACTION.append(direcao)
                    expirations_mode.append(duration)

                    # operaçao

                    id_list = iq.buy_multi(
                        Money, ACTIVES, ACTION, expirations_mode)
                    if id_list == [None]:
                        print(datetime.datetime.now().strftime("%H:%M"))
                        print(result)
                        print("Não foi possível entrar na binária.")
                        print("Tentando entrar na digital.")
                        _, id = iq.buy_digital_spot(
                            ACTIVES[0], Money[0], ACTION[0], expirations_mode[0])
                        print("ID da operação:", id)
                        tipo_operacao = 'digital'
                        win_loss_thread = threading.Thread(
                            target=check_win_loss, args=[id, result, tipo_operacao])
                        win_loss_thread.start()
                    else:  # entra na operaçao
                        print('Entrando na operação...')
                        print(datetime.datetime.now().strftime("%H:%M"))
                        print(result)
                        print("ID da operação:", id_list[0])
                        tipo_operacao = 'binaria'
                        print("\n")
                        win_loss_thread = threading.Thread(
                            target=check_win_loss, args=[id_list[0], result, tipo_operacao])
                        win_loss_thread.start()

                else:
                    print(datetime.datetime.now().strftime("%H:%M"))
                    print("Mensagem não está no formato.")

        client.start()
        client.run_until_disconnected()


def run_loop_conexao():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(loop_conexao())


thread_conexao = threading.Thread(target=run_loop_conexao)
thread_conexao.start()
