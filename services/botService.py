from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import time
from datetime import datetime
import requests
import os
from dotenv import load_dotenv
load_dotenv()

SERVER = os.getenv('SERVER')


def login(email, password, driver):
    driver.get("https://www.socialcube.net/login")
    email_input = driver.find_element(By.ID, "inputEmail")
    password_input = driver.find_element(By.ID, "inputPassword")
    email_input.send_keys(email)
    time.sleep(1)
    password_input.send_keys(password)
    time.sleep(1)
    loginBtn = driver.find_element(By.CLASS_NAME, "btn-primary")
    loginBtn.click()


def press_button(driver):
    driver.get("https://www.socialcube.net/games/thebutton")
    mainButton = driver.find_element(By.CLASS_NAME, "btn-primary")
    mainButton.click()

    try:
        logMsg = driver.find_element(By.CSS_SELECTOR,
                                  "#content_data > div.alert.alert-dismissable.alert-warning.animated.pulse > p")
    except NoSuchElementException:
        try:
            logMsg = driver.find_element(By.CSS_SELECTOR,
                                      "#content_data > div.alert.alert-dismissable.alert-success.animated.tada")
        except NoSuchElementException:
            logMsg = "Something went wrong"

    return logMsg


def create_log(server, log_msg):
    now = datetime.now()
    log = " ".join(log_msg.splitlines())
    now = now.strftime("%d/%m/%Y, %H:%M:%S")
    logMsg = now + " ---> " + log
    print(logMsg)
    data = {'logMsg': log, 'logDate': now}
    requests.post(server, json=data)


def guess_word(driver, words):
    while True:
        logMsg = ""
        wordGuess = ""
        currentWord = 0
        while not logMsg.startswith("Du hast"):
            wordGuess = words[currentWord].replace("\n", "")
            words.pop(currentWord)
            currentWord += 1
            driver.get("https://www.socialcube.net/games/wordguess")
            time.sleep(2)
            wordGuesser = driver.find_element(By.CSS_SELECTOR,
                                              "#content_data > div.row > div.col-md-8 > div > div.panel-body.content_box_content > form > fieldset > div.form-control-wrapper > input")
            wordGuesser.send_keys(wordGuess)
            time.sleep(1)
            guessBtn = driver.find_element(By.CLASS_NAME, "btn-primary")
            guessBtn.click()
            try:
                logMsg = driver.find_element(By.CSS_SELECTOR, "#content_data > div.alert.alert-dismissable.alert-danger.animated.shake > p").text
            except NoSuchElementException:
                try:
                    logMsg = driver.find_element(By.CSS_SELECTOR, "#content_data > h2").text
                    logMsg = "Gratulation! " + logMsg
                    create_log(SERVER, logMsg)
                except NoSuchElementException:
                    logMsg = driver.find_element(By.CSS_SELECTOR, "#content_data > div.alert.alert-dismissable.alert-warning.animated.pulse").text

            print("Word: " + wordGuess + ", " + logMsg)
        return logMsg


def read_file(file_name):
    with open(file_name) as f:
        lines = f.readlines()
    return lines


def write_file(file_name, data):
    with open(file_name, 'w') as f:
        f.write("".join(data))


