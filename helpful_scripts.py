import requests
import imaplib
import email
from email.header import decode_header
import webbrowser
import re
import os
from bs4 import BeautifulSoup

from anticaptchaofficial.imagecaptcha import imagecaptcha
from PIL import Image
from io import BytesIO
from working_data import enter_captcha_position, anticaptcha_key, tg_token, tg_chat_id, mail_account, imap_psw


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
    bot_token = tg_token
    bot_chatID = tg_chat_id
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + \
                bot_chatID + '&parse_mode=Markdown&text=' + bot_message
    response = requests.get(send_text)
    return response.json()


def make_full_screenshot(driver):
    png = driver.get_screenshot_as_png()  # saves screenshot of entire page
    im = Image.open(BytesIO(png))  # uses PIL library to open image in memory
    im.save('screenshot2.png')  # saves new cropped image


def clean(text):
    # clean text for creating a folder
    return "".join(c if c.isalnum() else "_" for c in text)


def check_mail():
    username = mail_account
    password = imap_psw
    imap_server = "imap.ukr.net"
    # create an IMAP4 class with SSL
    imap = imaplib.IMAP4_SSL(imap_server)
    # authenticate
    imap.login(username, password)

    status, messages = imap.select("INBOX")
    # number of top emails to fetch
    N = 1
    # total number of emails

    messages = int(messages[0])
    code = 0

    for i in range(messages, messages - N, -1):
        # fetch the email message by ID
        res, msg = imap.fetch(str(i), "(RFC822)")
        for response in msg:
            if isinstance(response, tuple):
                # parse a bytes email into a message object
                msg = email.message_from_bytes(response[1])
                # decode the email subject
                subject, encoding = decode_header(msg["Subject"])[0]
                if isinstance(subject, bytes):
                    # if it's a bytes, decode to str
                    subject = subject.decode(encoding)
                # decode email sender
                From, encoding = decode_header(msg.get("From"))[0]
                if isinstance(From, bytes):
                    From = From.decode(encoding)
                print("Subject:", subject)
                print("From:", From)
                # if the email message is multipart
                # print(msg)
                if msg.is_multipart():
                    # iterate over email parts
                    for part in msg.walk():
                        # extract content type of email
                        content_type = part.get_content_type()
                        content_disposition = str(part.get("Content-Disposition"))
                        try:
                            # get the email body
                            body = part.get_payload(decode=True).decode()
                        except:
                            pass
                        if content_type == "text/plain" and "attachment" not in content_disposition:
                            # print text/plain emails and skip attachments
                            print(body)
                        elif "attachment" in content_disposition:
                            # download attachment
                            filename = part.get_filename()
                            if filename:
                                folder_name = clean(subject)
                                if not os.path.isdir(folder_name):
                                    # make a folder for this email (named after the subject)
                                    os.mkdir(folder_name)
                                filepath = os.path.join(folder_name, filename)
                                # download attachment and save it
                                open(filepath, "wb").write(part.get_payload(decode=True))
                else:
                    # extract content type of email
                    content_type = msg.get_content_type()
                    print(content_type)
                    # get the email body
                    body = msg.get_payload(decode=True).decode()
                    if content_type == "text/plain":
                        # print only text email parts
                        print(body)
                if content_type == "text/html":
                    # if it's HTML, create a new HTML file and open it in browser
                    # folder_name = clean(subject)
                    # if not os.path.isdir(folder_name):
                    #     # make a folder for this email (named after the subject)
                    #     os.mkdir(folder_name)
                    # filename = "index.html"
                    # filepath = os.path.join(folder_name, filename)
                    # write the file
                    # open(filepath, "w").write(body)
                    # open in the default browser
                    # webbrowser.open(filepath)
                    soup = BeautifulSoup(body, 'html.parser')
                    code_text = soup.body.findAll(text=re.compile('Your One-time Password*'))
                    code = int(code_text[0].split('Your One-time Password (OTP) is ')[1][:6])
                    print(code)


                print("=" * 100)
    # close the connection and logout
    imap.close()
    imap.logout()
    return code

check_mail()