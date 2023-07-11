from telethon.sync import TelegramClient
from telethon import events

API_ID = '12093312'
API_HASH = '67926450017650430bfc865ad771523d'
# CHAT_ID = '-1001474420372'
CHAT_ID = '-1001864670859'

with TelegramClient('session_name', API_ID, API_HASH) as client:
    @client.on(events.NewMessage)
    async def armazenar_mensagem(event):
        if event.is_group and str(event.chat_id) == CHAT_ID:
            print(f"Nova mensagem recebida: {event.message.text}")
        # else:
        #     print(event.chat_id)
    while True:
        try:
            client.run_until_disconnected()
        except KeyboardInterrupt:
            loop = False
