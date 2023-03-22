import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from services.botService import login, press_button, create_log

EMAIL = os.getenv('EMAIL')
PASSWORD = os.getenv('PASSWORD')

while True:
    try:
        service = Service("assets/chromedriver.exe")
        driver = webdriver.Chrome(service=service)
        login(EMAIL, PASSWORD, driver)
        log_msg = press_button(driver).text
        create_log(log_msg)
        driver.close()
        time.sleep(60*30)

    except Exception as e:
        os.system("python pressButton.py")
