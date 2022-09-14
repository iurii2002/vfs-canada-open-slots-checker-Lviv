import random

from time import sleep
from working_data import chechek_account, selenium_driver_path
from canada_visa import VFSBot
from helpful_scripts import telegram_bot_sendtext


def main():
    try:
        slots_available = False
        cycles = 0
        mail, psw, application = chechek_account
        bot = VFSBot(selenium_driver_path, mail, psw, application)
        bot.enter_account()
        while not slots_available:
            cycles += 1
            bot.retrieve_appointment()
            if bot.is_there_available_slots():
                slots_available = True
            if cycles % 20 == 0:
                bot.reload_driver()
            sleep(random.randint(60, 100))
        telegram_bot_sendtext("SLOTS AVAILABLE")

    except Exception as err:
        print(err)


if __name__ == '__main__':
    main()
