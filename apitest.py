import os
from dotenv import load_dotenv
from iqoptionapi.stable_api import IQ_Option


load_dotenv()
email = os.getenv('email')
password = os.getenv('senha')

iq = IQ_Option(email, password)
check, reason = iq.connect()  # connect to iqoption
if iq.check_connect() == True:
    print("Conta conectada.")
    print("Você está na conta:", iq.get_balance_mode())
    print("Seu saldo é:", iq.get_balance())
