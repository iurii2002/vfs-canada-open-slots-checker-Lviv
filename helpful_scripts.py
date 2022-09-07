import requests

from anticaptchaofficial.imagecaptcha import imagecaptcha
from PIL import Image
from io import BytesIO
from working_data import enter_captcha_position, anticaptcha_key


def solve_captcha_pic(driver):
    solver = imagecaptcha()
    solver.set_verbose(0)
    solver.set_key(anticaptcha_key)
    get_captcha_pic(driver)

    captcha_text = solver.solve_and_return_solution("captcha.png")
    if captcha_text != 0:
        print("captcha text " + captcha_text)
        return captcha_text
    else:
        print("task finished with error " + solver.error_code)


def get_captcha_pic(driver):
    png = driver.get_screenshot_as_png()  # saves screenshot of entire page
    im = Image.open(BytesIO(png))  # uses PIL library to open image in memory
    (left, top, right, bottom) = enter_captcha_position
    im = im.crop((left, top, right, bottom))  # defines crop points
    im.save('captcha.png')  # saves new cropped image


def telegram_bot_sendtext(bot_message):
    bot_token = '1635932722:AAEUIQ27kTpUKF_57FJtAeTS3cnkmaxDa3Y'
    bot_chatID = '486767090'
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + \
                bot_chatID + '&parse_mode=Markdown&text=' + bot_message
    response = requests.get(send_text)
    return response.json()
