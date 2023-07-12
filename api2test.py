from telethon.sync import TelegramClient
from telethon import events
import threading
import asyncio

API_ID = '12093312'
API_HASH = '67926450017650430bfc865ad771523d'
# CHAT_ID = '-1001474420372'  # traderzismo
CHAT_ID = '-1001864670859'

mensagem = ''


def loop_conexao():
    with TelegramClient('session_name', API_ID, API_HASH) as client:
        @client.on(events.NewMessage)
        async def armazenar_mensagem(event):
            global mensagem
            if event.is_group and str(event.chat_id) == CHAT_ID:
                mensagem = f"Nova mensagem recebida: {event.message.text}"
                print(mensagem)

        client.start()
        client.run_until_disconnected()


def processar_mensagem(event):
    pass


def run_loop_conexao():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(loop_conexao())


thread_conexao = threading.Thread(target=run_loop_conexao)
thread_conexao.start()


thread_conexao.join()
