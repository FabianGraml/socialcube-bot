import os
from selenium import webdriver
import time
from services.botService import login, read_file, write_file, guess_word, create_log
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

load_dotenv()
EMAIL = os.getenv('EMAIL')
PASSWORD = os.getenv('PASSWORD')
SERVER = os.getenv('SERVER')

words = read_file("assets/english-dictionary.txt")
while True:
    try:
        service = Service("assets/chromedriver.exe")
        driver = webdriver.Chrome(service=service)
        login(EMAIL, PASSWORD, driver)
        log_msg = guess_word(driver, words)
        create_log(log_msg)
        write_file("./assets/english-dictionary.txt", words)
        driver.close()
        time.sleep(60 * 15)
    except Exception as e:
        os.system("python guessWord.py")
