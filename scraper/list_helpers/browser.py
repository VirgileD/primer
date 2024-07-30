from requests import get
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import os
import json
import sys
sys.path.append("..")
from utils.logmngt import get_logger # type: ignore

def save_cookies(browser):
    cookies = browser.get_cookies()
    with open('cookies.json', 'w') as file:
        json.dump(cookies, file)
    get_logger("save_cookies", {}).info("Cookies saved")

def load_cookies(browser):
    if 'cookies.json' in os.listdir():
        with open('cookies.json', 'r') as file:
            cookies = json.load(file)

        for cookie in cookies:
            browser.add_cookie(cookie)
        get_logger("load_cookies", {}).info("Cookies loaded from file")
        return True
    else:
        get_logger("load_cookies", {}).info("No cookies file found")
        return False

def setup_browser():
    log = get_logger("setup_browser", {})
    log.debug("Setting up browser")
    # Define Chrome options
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--lang=en")
    chrome_options.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})

    cur_dir = os.path.expanduser("./")
    chrome_binary_path = os.path.join(cur_dir, "chrome-linux64", "chrome")
    chromedriver_path = os.path.join(cur_dir, "chromedriver-linux64", "chromedriver")
    chrome_options.binary_location = chrome_binary_path
    service = Service(chromedriver_path)

    browser = webdriver.Chrome(service=service, options=chrome_options)
    log.info("Browser set up")
    
    return browser