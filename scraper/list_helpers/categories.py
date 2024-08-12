import time
import sys
from halo import Halo
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import StaleElementReferenceException
from list_helpers.misc import document_complete, save_all_shows

from utils.logmngt import get_logger


def get_categories(config, browser):
    log = get_logger("get_categories", cfg=config)
    log.debug("Getting categories")
    
    WebDriverWait(browser, 30).until(expected_conditions.title_contains("Prime Video"))
    # get the anchor tag in the label tag whose attribute "for" is "pv-nav-categories"
    element = browser.find_element(By.XPATH, "//a[@data-testid='pv-nav-categories-dropdown-trigger']")
    browser.get(element.get_attribute("href"))
    WebDriverWait(browser, 30).until(expected_conditions.title_contains("Categor"))
    # find all anchors in h3 tags with their attribute data-testid to "genre-card"
    category_elements = browser.find_elements(By.XPATH, "//h3[@data-testid='genre-card']/a")
    categories = []
    for category_element in category_elements:
        category = category_element.get_attribute("aria-label")
        if category in config["filter_categories"]:
            continue
        categories.append({ "name": category, "main_page": category_element.get_attribute("href"), "urls": [] })

    log.info(f"Found {len(categories)} categories: { ', '.join([ cat['name'] for cat in categories])}")

    return categories

def get_all_listing_pages(config, browser, category):
    browser.get(category["main_page"])
    WebDriverWait(browser, 30).until(expected_conditions.presence_of_element_located((By.XPATH, "//a[@data-testid='see-more']")))
    more_pages = browser.find_elements(By.XPATH, "//a[@data-testid='see-more']") # element is not interactive, so just record the url
    for more_page in more_pages:
        type_ = more_page.get_attribute("aria-label")
        if type_ in config["more_of"].keys():
            category["urls"].append({ "type": config["more_of"][type_], "url": more_page.get_attribute("href")})
    return category

def scrap_category(config, browser, category, shows):
    log = get_logger("scrap_category", cfg=config)
    category_name = category['name']
    spinner = Halo(spinner='dots')
    these_shows = {}
    for list_page in category["urls"]:
        type_ = list_page["type"]
        spinner.text = f"Scraping '{category_name}/{type_}'"
        spinner.start()
        browser.get(list_page["url"])
        
        WebDriverWait(browser, 30).until(expected_conditions.presence_of_element_located((By.XPATH, "//div[@data-testid='grid-mini-details-controller']")))

        last = None
        tot = 0
        staled = 0
        reread = 0
        while True:
            # browse the newly loaded cards
            # there we just thecurrently displayed cards so we sometimes reread some of them.
            article_elements = browser.find_elements(By.XPATH, "//div[@data-testid='grid-mini-details-controller']/div/article")
            # there should always be cards, unless we're at the end of the list
            if not article_elements:
                break
            # FIXME: this is probably useless - the absence of an article_element should be enough
            last_element_id = article_elements[-1].get_attribute("data-card-title")
            if last == last_element_id:
                break
            last = last_element_id

            for article_element in article_elements:
                try:
                    title = article_element.get_attribute("data-card-title")
                    url = article_element.find_element(By.XPATH, ".//a").get_attribute("href")
                    id = url.split('detail/')[1].split('/')[0]
                    if id not in these_shows:
                        tot += 1
                        these_shows[id] = { "title": title, "url": url, "type": type_ }
                    else:
                        reread += 1
                except StaleElementReferenceException as e:
                    staled += 1
            # when all the currently displayed cards have been processed, scroll down to load more
            browser.execute_script("arguments[0].scrollIntoView();", article_elements[-1])
            WebDriverWait(browser, 30).until(document_complete())
            # FIXME: normally the document_complete expectation should be enough, but it's not
            time.sleep(0.5) # let the page settle down, otherwise it's breaking out of loop bc, probably, the next cards are not loaded
        spinner.stop()
        # # Deletes the last line in the STDOUT"
        # sys.stdout.write('\x1b[1A')
        # sys.stdout.write('\x1b[2K')
        log.info(f"    - found {tot} shows in '{category_name}/{type_}' page ({reread} reread, {staled} staled)")
        save_all_shows(config, these_shows)

    already_known = 0
    added = 0
    for id, these_show in these_shows.items():
        if id not in shows:
            shows[id] = these_show
            added += 1
        else:
            already_known += 1

    log.info(f"  => Added {added} shows from '{category_name}' category / {already_known} others were in nmultiple categories")
    return shows
