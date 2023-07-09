import telebot
import os
import requests
import time
from dotenv import load_dotenv
import datetime
from iqoptionapi.stable_api import IQ_Option

load_dotenv()

TOKEN = os.getenv('API_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')


bot = telebot.TeleBot(TOKEN)
mensagens = []


@bot.message_handler(func=lambda message: True)
def armazenar_mensagem(message):
    mensagens.append(message.text)
    print(f"Nova mensagem recebida: {message.text}\n")


while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(f"Erro: {e}")
