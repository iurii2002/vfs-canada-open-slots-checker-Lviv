import random

from time import sleep
from working_data import accounts, selenium_driver_path
from canada_visa import VFSBot
from helpful_scripts import telegram_bot_sendtext


def main():
    for account in accounts:
        if account is None:
            continue
        try:
            slots_available = False

            mail, psw, application = account
            bot = VFSBot(selenium_driver_path, mail, psw, application)
            bot.enter_account()
            while not slots_available:
                bot.retrieve_appointment()
                if bot.is_there_available_slots():
                    slots_available = True
                sleep(random.randint(60, 100))
            telegram_bot_sendtext("SLOTS AVAILABLE")

        except Exception as err:
            print(err)


if __name__ == '__main__':
    main()
