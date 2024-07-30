import csv
import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException
from pymongo import MongoClient

def save_all_shows(config, all_shows, type_=''):
    client = MongoClient(config['db_uri'])
    shows_db = client.get_default_database("shows")
    raw_coll = shows_db.raw
    for id, show in all_shows.items():
        show["id"] = id
        show["last_update"] = datetime.datetime.now()
        raw_coll.update_one({ "id": id }, { "$set": show }, upsert=True)        

def safe_wait(config, condition):
    try:
        WebDriverWait(config["browser"], 30).until(condition)
    except:
        print("safe_wait failed, condition {condition} not met")
        print(f"Current page title: {config['browser'].title}")
        print(f"Current page url: {config['browser'].current_url}")
        exit()
    

def goto_home_page(config, browser):
    browser.get(config["store_url"])

class document_complete(object):   
    def __call__(self, driver):
        script = 'return document.readyState'
        try:
            return driver.execute_script(script) == 'complete'
        except WebDriverException:
            return False
