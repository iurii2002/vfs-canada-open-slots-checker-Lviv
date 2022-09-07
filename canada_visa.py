import random
import datetime

from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from helpful_scripts import solve_captcha_pic


class VFSBot:
    url = 'https://www.vfsglobal.ca/IRCC-AppointmentWave1/'

    def __init__(self, selenium_driver_path, mail, password, application):
        self._sdp = selenium_driver_path
        self.driver = self._start_driver()
        self.mail = mail
        self.password = password
        self.application = application

    def _start_driver(self):
        service = Service(self._sdp)
        chrome_options = webdriver.ChromeOptions()
        # for not closing window use detach
        chrome_options.add_experimental_option("detach", True)
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.page_load_strategy = "none"
        driver = webdriver.Chrome(service=service, options=chrome_options)
        return driver

    def enter_account(self):
        print('Entering account......')
        self.driver.get(self.url)
        sleep(random.randint(3, 5))
        wait = WebDriverWait(self.driver, 60)
        try:
            mail_filed = '/html/body/div[2]/div[1]/div[4]/div/form/div[1]/div[2]/input'
            wait.until(EC.presence_of_element_located((By.XPATH, mail_filed)))

            mail_filed = self.driver.find_element(By.XPATH, mail_filed)
            psw_filed = self.driver.find_element(By.XPATH,
                                                 '/html/body/div[2]/div[1]/div[4]/div/form/div[2]/div[2]/input')
            two_fa_filed = self.driver.find_element(By.XPATH,
                                                    '/html/body/div[2]/div[1]/div[4]/div/form/div[3]/div/input[2]')
            enter_button = self.driver.find_element(By.XPATH, '/html/body/div[2]/div[1]/div[4]/div/form/div[4]/input')

            captcha_word = solve_captcha_pic(self.driver).upper()
            mail_filed.send_keys(self.mail)
            psw_filed.send_keys(self.password)
            two_fa_filed.send_keys(captcha_word)
            enter_button.click()
            welcome_message_html = '/html/body/div[2]/div[1]/div[1]/span/div/form/label[1]'
            wait.until(EC.presence_of_element_located((By.XPATH, welcome_message_html)))
            print('Entered account!')
            sleep(random.randint(2, 5))

        except:
            print('Something went wrong, will try again in a couple of minutes.')
            sleep(random.randint(90, 120))
            self.driver.refresh()
            self.enter_account()

    def retrieve_appointment(self):
        print(f'Retrieving application at {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")} ')
        try:
            retrieve_app_button = self.driver.find_element(By.XPATH,
                                                           "/html/body/div[2]/div[1]/div[2]/div/div/div[2]/div/ul/li[5]/a")
            retrieve_app_button.click()
            sleep(random.randint(3, 5))
        except:
            #     there is no retrieve button, so we are not logged in
            self.enter_account()

        wait = WebDriverWait(self.driver, 90)
        try:
            reg_bum_field_html = '/html/body/div[2]/div[1]/div[3]/div[2]/form/div[3]/div[1]/div/div/input'
            wait.until(EC.presence_of_element_located((By.XPATH, reg_bum_field_html)))

            reg_bum_field = self.driver.find_element(By.XPATH, reg_bum_field_html)
            reg_bum_field.send_keys(self.application)
            submit_button = self.driver.find_element(By.XPATH,
                                                     '/html/body/div[2]/div[1]/div[3]/div[2]/form/div[3]/div[5]/div/input[2]')
            submit_button.click()
            sleep(random.randint(2, 4))

            edit_button_html = '/html/body/div[2]/div[1]/div[3]/div[2]/table/tbody/tr[2]/td[5]/a[1]'
            wait.until(EC.presence_of_element_located((By.XPATH, edit_button_html)))
            edit_button = self.driver.find_element(By.XPATH, edit_button_html)
            edit_button.click()

            sleep(random.randint(1, 3))
            continue_button_html = '/html/body/div[2]/div[1]/div[3]/div[3]/form/div[2]/input'
            wait.until(EC.presence_of_element_located((By.XPATH, continue_button_html)))
            continue_button = self.driver.find_element(By.XPATH, continue_button_html)
            continue_button.click()
            appointment_booking = '/html/body/div[2]/div[1]/div[3]/h1'
            wait.until(EC.presence_of_element_located((By.XPATH, appointment_booking)))

        except:
            sleep(random.randint(30, 60))
            self.retrieve_appointment()

    def is_there_available_slots(self):
        try:
            if self.driver.find_element(By.XPATH,
                                        '/html/body/div[2]/div[1]/div[3]/div[3]/form/div[1]/ul/li').text == "No slots are currently available for 1 applicants.":
                print('there is no slots available')
                return False
            else:
                print('there is slots available')
                return True
        except:
            with open("page_source.html", "w") as f:
                f.write(self.driver.page_source)
