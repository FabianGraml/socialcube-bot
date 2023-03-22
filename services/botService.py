from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import time
from datetime import datetime
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
    login_btn = driver.find_element(By.CLASS_NAME, "btn-primary")
    login_btn.click()


def press_button(driver):
    driver.get("https://www.socialcube.net/games/thebutton")
    main_btn = driver.find_element(By.CLASS_NAME, "btn-primary")
    main_btn.click()

    try:
        log_msg = driver.find_element(By.CSS_SELECTOR,
                                      "#content_data > div.alert.alert-dismissable.alert-warning.animated.pulse > p")
    except NoSuchElementException:
        try:
            log_msg = driver.find_element(By.CSS_SELECTOR,
                                          "#content_data > div.alert.alert-dismissable.alert-success.animated.tada")
        except NoSuchElementException:
            log_msg = "Something went wrong"

    return log_msg


def guess_word(driver, words):
    while True:
        log_msg = ""
        current_word = 0
        while not log_msg.startswith("Du hast") and "Wartezeit" not in log_msg:
            word_guess = words[current_word].replace("\n", "")
            words.pop(current_word)
            current_word += 1
            driver.get("https://www.socialcube.net/games/wordguess")
            time.sleep(2)
            word_guesser = driver.find_element(By.CSS_SELECTOR,
                                               "#content_data > div.row > div.col-md-8 > div > "
                                               "div.panel-body.content_box_content > form > fieldset > "
                                               "div.form-control-wrapper > input")
            word_guesser.send_keys(word_guess)
            time.sleep(1)
            guess_btn = driver.find_element(By.CLASS_NAME, "btn-primary")
            guess_btn.click()
            time.sleep(2)

            try:
                log_msg = driver.find_element(By.CSS_SELECTOR, "#content_data > div.alert.alert-dismissable.alert"
                                                               "-danger.animated.shake > p").text
            except NoSuchElementException:
                try:
                    log_msg = driver.find_element(By.CSS_SELECTOR, "#content_data > h2").text
                except NoSuchElementException:
                    log_msg = driver.find_element(By.CSS_SELECTOR, "#content_data > div.alert.alert-dismissable.alert"
                                                                   "-warning.animated.pulse").text
                    log_msg = log_msg.replace("\n", "").replace("×", "")

            print("Word: " + word_guess + ", " + log_msg)
        return log_msg


def create_log(log_msg):
    now = datetime.now()
    log = " ".join(log_msg.splitlines())
    now = now.strftime("%d/%m/%Y, %H:%M:%S")
    write_file("log.txt", "[" + now + "]" + log)


def read_file(file_name):
    with open(file_name) as f:
        lines = f.readlines()
    return lines


def write_file(file_name, data):
    with open(file_name, 'w') as f:
        f.write("".join(data))
