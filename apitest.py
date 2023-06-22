import os
from dotenv import load_dotenv
from iqoptionapi.stable_api import IQ_Option

load_dotenv()
email = os.getenv("email")
password = os.getenv("senha")

error_password = """{"code":"invalid_credentials","message":"You entered the wrong credentials. Please check that the login/password is correct."}"""
iqoption = IQ_Option("email", "password")
check, reason = iqoption.connect()
if check:
    print("Start your robot")
    # if see this you can close network for test
    while True:
        if iqoption.check_connect() == False:  # detect the websocket is close
            print("try reconnect")
            check, reason = iqoption.connect()
            if check:
                print("Reconnect successfully")
            else:
                if reason == error_password:
                    print("Error Password")
                else:
                    print("No Network")

else:

    if reason == "[Errno -2] Name or service not known":
        print("No Network")
    elif reason == error_password:
        print("Error Password")
