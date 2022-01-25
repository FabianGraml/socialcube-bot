import os
import time
from selenium import webdriver
from services.botService import login, press_button, create_log

EMAIL = os.getenv('EMAIL')
PASSWORD = os.getenv('PASSWORD')
SERVER = os.getenv('SERVER')

while True:
    try:
        driver = webdriver.Chrome(executable_path="assets/chromedriver.exe")

        login(EMAIL, PASSWORD, driver)

        logMsg = press_button(driver).text

        print(logMsg)
        # create_log(SERVER, logMsg)
        driver.close()
        time.sleep(60*30)

    except Exception as e:
        driver.close()
        os.system("python pressButton.py")
