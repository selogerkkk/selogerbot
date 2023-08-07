import sys
import time
import os
import datetime
from threading import Thread
import asyncio
from telethon.sync import TelegramClient
from telethon import events
from dotenv import load_dotenv
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
saldo = 0
usargale = 0
num_gales = 2
multiplier = 2

# Bot login
iq = IQ_Option(email, password)
check, reason = iq.connect()  # connect to IQ Option


def print_account_info():
    balance_mode = iq.get_balance_mode()
    balance = iq.get_balance()
    print(datetime.datetime.now().strftime("%H:%M"))
    print("Conta conectada.")
    print("Bem-vindo de volta.")
    print("Você está na conta:", balance_mode)
    print("Seu saldo é:", balance)
    print("\n")
    return balance


def stop_loss_check(saldo, stoploss):
    if saldo <= -stoploss:
        print("Stop Loss alcançado.")
        return True
    return False


def stop_win_check(saldo, stopwin):
    if saldo >= stopwin:
        print("Stop Win alcançado.")
        return True
    return False


if iq.check_connect():
    print_account_info()
    print("Aguardando operações...")
else:
    print(datetime.datetime.now().strftime("%H:%M"))
    print("Erro ao logar. Tente novamente.")
    sys.exit()

stoploss = 2
stopwin = 2
can_enter_trade = True


def check_win_loss(id_list, result, tipo_operacao):
    global saldo, can_enter_trade
    if tipo_operacao == 'binaria':
        resultado_binaria = iq.check_win_v3(id_list)
        if resultado_binaria is not None:
            print(result['par'])
            print(result['direcao'])
            print(result['horario'])
            print("Resultado da operação: {:.2f}".format(resultado_binaria))
            saldo += resultado_binaria
            stop_loss_reached = stop_loss_check(saldo, stoploss)
            stop_win_reached = stop_win_check(saldo, stopwin)
            if stop_loss_reached or stop_win_reached:
                can_enter_trade = False
            print("\nSaldo das operações: {:.2f}".format(saldo))
    elif tipo_operacao == 'digital':
        print(result['par'])
        print(result['direcao'])
        print(result['horario'])
        op_digital = iq.check_win_digital(id_list, 2)
        print("Resultado da operação: {:.2f}".format(op_digital))
        saldo += op_digital
        stop_loss_reached = stop_loss_check(saldo, stoploss)
        stop_win_reached = stop_win_check(saldo, stopwin)
        if stop_loss_reached or stop_win_reached:
            can_enter_trade = False
        print("\nSaldo das operações: {:.2f}\n".format(saldo))

# Configurable Martingale Function


def martingale(id_list, result, tipo_operacao, num_gales, multiplier):
    global saldo, can_enter_trade

    if tipo_operacao == 'binaria':
        if iq.check_win_v3(id_list) is not None:
            print(result['par'])
            print(result['direcao'])
            print(result['horario'])
            resultado_binaria = iq.check_win_v3(id_list)
            print("resultado da operação: {:.2f}".format(resultado_binaria))
            saldo += resultado_binaria
            stop_loss_reached = stop_loss_check(saldo, stoploss)
            stop_win_reached = stop_win_check(saldo, stopwin)
            if stop_loss_reached or stop_win_reached:
                can_enter_trade = False
            print("\nSaldo das operações: {:.2f}\n".format(saldo))
        else:
            print("Operação perdida.")
            loss_amount = sum(id_list)
            saldo -= loss_amount

            for i in range(num_gales):
                print(f"Martingale {i+1} - Multiplicador: {multiplier}")
                id_list = iq.buy_multi(
                    [loss_amount * multiplier], [result['par']], [result['direcao']], [1])
                if id_list != [None]:
                    print('Entrando na operação de Martingale...')
                    print(datetime.datetime.now().strftime("%H:%M"))
                    print(result)
                    print("ID da operação:", id_list[0])
                    print("\n")
                    break
                else:
                    print(
                        "Não foi possível entrar na operação de Martingale. Tentando novamente.")

    elif tipo_operacao == 'digital':
        if iq.check_win_digital_v2(id_list) is not None:
            print(result['par'])
            print(result['direcao'])
            print(result['horario'])
            resultado_digital = iq.check_win_digital_v2(id_list)
            print("resultado da operação: {:.2f}".format(resultado_digital))
            saldo += resultado_digital
            stop_loss_reached = stop_loss_check(saldo, stoploss)
            stop_win_reached = stop_win_check(saldo, stopwin)
            if stop_loss_reached or stop_win_reached:
                can_enter_trade = False
            print("\nSaldo das operações: {:.2f}\n".format(saldo))
        else:
            print("Operação digital perdida.")
            loss_amount = sum(id_list)
            saldo -= loss_amount

            for i in range(num_gales):
                print(f"Martingale {i+1} - Multiplicador: {multiplier}")
                _, id = iq.buy_digital_spot(
                    result['par'], loss_amount * multiplier, result['direcao'], 1)
                if id:
                    print('Entrando na operação digital de Martingale...')
                    print(datetime.datetime.now().strftime("%H:%M"))
                    print(result)
                    print("ID da operação:", id)
                    print("\n")
                    break
                else:
                    print(
                        "Não foi possível entrar na operação digital de Martingale. Tentando novamente.")

    print("\nSaldo das operações: {:.2f}".format(saldo))


def verificar_maior_payout(par):
    payout_binaria = iq.get_binary_option_detail()
    payout_digital = iq.get_digital_payout(par)
    print("payout binária:", payout_binaria[par]["turbo"])
    if payout_binaria[par]["turbo"] > payout_digital(par):
        return 'binaria', payout_binaria[par]["turbo"]
    else:
        return 'digital', payout_digital(par)


async def armazenar_mensagem(event):
    global mensagem
    global msg
    global can_enter_trade

    if event.is_group and str(event.chat_id) == CHAT_ID:
        texto = event.message.text
        result = {}

        if "TRADERZISMO FREE" in texto:
            if not can_enter_trade:
                return

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
            horario = texto[indice_inicio_horario:(
                indice_inicio_horario+5)]
            if horario.upper() == 'AGORA':
                horario = datetime.datetime.now().strftime("%H:%M")
            result['horario'] = horario

            amount = 1
            duration = 1

            Money = [amount]
            ACTIVES = [par]
            ACTION = [direcao_encontrada]
            expirations_mode = []
            expirations_mode.append(duration)

            tipo_operacao1, payout_maior = verificar_maior_payout(par)
            print(
                f"Maior Payout: {payout_maior:.2f} - Tipo de Operação: {tipo_operacao}")
            if tipo_operacao1 == 'binaria':
                id_list = iq.buy_multi(
                    Money, ACTIVES, ACTION, expirations_mode)
                if id_list != [None]:
                    print('Entrando na operação binária...')
                    print(datetime.datetime.now().strftime("%H:%M"))
                    print(result)
                    print("ID da operação:", id_list[0])
                    tipo_operacao = 'binaria'
                    print("\n")
                    check_win_loss_thread = Thread(target=check_win_loss, args=[
                        id_list[0], result, tipo_operacao])
                    check_win_loss_thread.start()
                else:
                    print(
                        "Não foi possível entrar na operação binária.")

            elif tipo_operacao == 'digital':
                _, id = iq.buy_digital_spot(
                    ACTIVES[0], Money[0], ACTION[0], expirations_mode[0])
                if id:
                    print('Entrando na operação digital...')
                    print(datetime.datetime.now().strftime("%H:%M"))
                    print(result)
                    print("ID da operação:", id)
                    tipo_operacao = 'digital'
                    print("\n")
                    check_win_loss_thread = Thread(target=check_win_loss, args=[
                        id, result, tipo_operacao])
                    check_win_loss_thread.start()
                else:
                    print("Não foi possível entrar na operação digital.")
                # if usargale == 0:
                #     win_loss_thread = Thread(target=check_win_loss, args=[
                #         id_list[0], result, tipo_operacao])
                #     win_loss_thread.start()
                # elif usargale == 1:
                #     win_loss_thread = Thread(target=martingale, args=[
                #         id_list[0], result, tipo_operacao,])
                #     win_loss_thread.start()
        else:
            print(datetime.datetime.now().strftime("%H:%M"))
            print("Mensagem não está no formato.")


def loop_conexao():
    with TelegramClient('session_name', API_ID, API_HASH) as client:
        client.on(events.NewMessage)(armazenar_mensagem)
        client.start()
        client.run_until_disconnected()


def run_loop_conexao():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(loop_conexao())


thread_conexao = Thread(target=run_loop_conexao)
thread_conexao.start()
