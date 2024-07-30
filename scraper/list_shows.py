from getpass import getpass
from webbrowser import get
from list_helpers.browser import setup_browser
from list_helpers.categories import get_all_listing_pages, get_categories, scrap_category
from list_helpers.login_process import login_process
from list_helpers.misc import save_all_shows, goto_home_page
from pyvirtualdisplay.display import Display
from utils.logmngt import get_logger
import os
import yaml

if __name__ == "__main__":
    config = {}
    if 'config.yml' in os.listdir():
        with open("config.yml", "r") as f:
            config = yaml.safe_load(f)
    else:
        print("No config file found")
        exit(1)
    log = get_logger("list_shows", cfg=config)
    log.debug("Starting list_shows")


    if "email" not in config:
        config["email"] = input("Enter your email: ")
    if "password" not in config:
        config["password"] = getpass("Enter your password: ")

    # even with a headless browser, at least with chromiun, the browser process is still expecting a display (wsl2)
    with Display(visible=False, size=(800, 600)) as display:
        browser = setup_browser()

        goto_home_page(config, browser)
        # login id needed
        login_process(config, browser)

        categories = get_categories(config, browser)
        shows = {}
        for category in categories:
            category = get_all_listing_pages(browser, category, config)
            shows = scrap_category(config, browser, category, shows)

        save_all_shows(config, shows)
    log.info(f"Found a total of {len(shows)} distinct shows")
