import logging
import os
import sys
from telethon.sync import TelegramClient
from telethon import events
from telethon.errors import SessionPasswordNeededError
from telethon.errors import UserBannedInChannelError
from iqoptionapi.stable_api import IQ_Option


logger = logging.getLogger(__name__)


class TraderZismoBot(object):
    """
    This bot is used to place trades on the IQ Option platform.
    """

    def __init__(self, email, password, chat_id):
        """
        Initialize the bot.

        Args:
            email: The email address of the bot account.
            password: The password of the bot account.
            chat_id: The chat ID of the channel or group where the bot will send messages.
        """
        self.email = email
        self.password = password
        self.chat_id = chat_id

        # Connect to the IQ Option platform.
        self.iq_option = IQ_Option(email, password)
        self.iq_option.connect()

        # Initialize the Telegram client.
        API_ID = '12093312'
        API_HASH = '67926450017650430bfc865ad771523d'
        self.client = TelegramClient('session_name', API_ID, API_HASH)
        self.client.start()

        # Subscribe to the `NewMessage` event.
        self.client.on(events.NewMessage)

    def on_new_message(self, event):
        """
        Handle a new message.

        Args:
            event: The event object.
        """
        # Check if the message is from the correct chat.
        if event.chat_id != self.chat_id:
            return

        # Get the message text.
        text = event.message.text

        # Check if the message contains the "TRADERZISMO FREE" keyword.
        if "TRADERZISMO FREE" in text:
            # Process the trade request.
            self.process_trade_request(text)

    def process_trade_request(self, text):
        """
        Process a trade request.

        Args:
            text: The text of the trade request.
        """
        # Parse the trade request.
        result = {}
        result['par'] = text[text.find('📊') + 2:text.find('\n')]
        result['direction'] = text[text.find('🔴') + 2:text.find('\n')]
        result['horario'] = text[text.find('⚠️ Operar ') + 10:text.find(' ⚠️')]

        # Check if the trade request is valid.
        if not all(result.values()):
            logger.error('Invalid trade request: %s', text)
            return

        # Place the trade.
        amount = 1
        duration = 1
        money = []
        actives = []
        action = []
        expirations_mode = []
        money.append(amount)
        actives.append(result['par'])
        action.append(result['direction'])
        expirations_mode.append(duration)
        id_list = self.iq_option.buy_multi(
            money, actives, action, expirations_mode)

        # Check if the trade was successful.
        if id_list == [None]:
            logger.error('Trade failed: %s', text)
            return

        # Send a message to the chat with the trade ID.
        self.client.send_message(
            self.chat_id, 'Trade ID: {}'.format(id_list[0]))


def main():
    # Get the bot email, password, and chat ID from the environment.
    email = os.getenv('email')
    password = os.getenv('senha')
    # chat_id = '-1001474420372' #traderzsimo
    chat_id = '-1001864670859'  # moneymaker

    # Create a new bot instance.
    bot = TraderZismoBot(email, password, chat_id)

    # Start the bot.
    bot.client.run_until_disconnected()


if __name__ == '__main__':
    main()
