from getpass import getpass
from webbrowser import get
from list_helpers.browser import setup_browser
from list_helpers.categories import get_all_listing_pages, get_categories, scrap_category
from list_helpers.login_process import login_process
from list_helpers.misc import save_all_shows, goto_home_page
from pyvirtualdisplay.display import Display
from utils.logmngt import get_logger
from utils.cfgmngt import get_config
from utils.dbmngt import setup_db

if __name__ == "__main__":
    config = get_config()
    log = get_logger("list_shows", cfg=config)
    log.debug("Starting list_shows")

    setup_db(config)

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
            category = get_all_listing_pages(config, browser, category)
            shows = scrap_category(config, browser, category, shows)

        save_all_shows(config, shows)
    log.info(f"Found a total of {len(shows)} distinct shows")
