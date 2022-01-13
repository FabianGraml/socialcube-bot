import os

from selenium import webdriver
import time
from services.botService import login, read_file, write_file, guess_word
from dotenv import load_dotenv

load_dotenv()
EMAIL = os.getenv('EMAIL')
PASSWORD = os.getenv('PASSWORD')
SERVER = os.getenv('SERVER')

words = read_file("assets/english-dictionary.txt")
while True:
  try:
    driver = webdriver.Chrome(executable_path="assets/chromedriver.exe")

    login(EMAIL, PASSWORD, driver)

    guess_word(driver, words)

    write_file("./assets/english-dictionary.txt", words)

    driver.close()
    time.sleep(60*15)
  except Exception as e:
      driver.close()
      os.system("python guessWord.py")
