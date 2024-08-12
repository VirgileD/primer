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
    spinner = Halo(spinner='dots')

    category_name = category['name']
    log.info(f" Scraping '{category_name}' category")
    # retain the shows found in this category, whatever the type - there will only be duplicate when the scrolling is not working 
    # fine and we rered the same element on the same page
    category_shows = {}
    already_known = 0
    for list_page in category["urls"]:
        type_ = list_page["type"] # movie, tv shows, rent
        spinner.text = f"Scraping '{category_name}/{type_}'"
        spinner.start()
        browser.get(list_page["url"])
        
        WebDriverWait(browser, 30).until(expected_conditions.presence_of_element_located((By.XPATH, "//div[@data-testid='grid-mini-details-controller']")))

        last = None
        category_total = 0
        staled = 0
        reread = 0
        while True:
            # only the currently displayed cards are in the DOM
            article_elements = browser.find_elements(By.XPATH, "//div[@data-testid='grid-mini-details-controller']/div/article")
            #  unless we're at the end of the list we find some
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
                    if id not in category_shows:
                        category_total += 1
                        category_shows[id] = { "title": title, "url": url, "type": type_ }
                        #print(f" ####### {category_name} {type_} {id} {title}")
                        if id not in shows:
                            shows[id] = category_shows[id]
                            shows[id]['new'] = True
                            shows[id]['categories'] = [{ 'name': category_name, 'type': type_ }]
                        else:
                            shows[id]['categories'].append({ 'name': category_name, 'type': type_ })
                            already_known += 1
                    else:
                        #print(f" +++++++ {category_name} {type_} {id} {title}")
                        reread += 1
                except StaleElementReferenceException as e:
                    staled += 1
            # when all the currently displayed cards have been processed, scroll down to load more
            browser.execute_script("arguments[0].scrollIntoView();", article_elements[-1])
            # and scroll of the elements height 
            browser.execute_script("window.scrollBy(0, 4 * arguments[0].offsetHeight);", article_elements[-1])
            WebDriverWait(browser, 30).until(document_complete())
            # FIXME: normally the document_complete expectation should be enough, but it's not
            time.sleep(0.5) # let the page settle down, otherwise it's breaking out of loop bc, probably, the next cards are not loaded
        spinner.stop()
        # # Deletes the last line in the STDOUT"
        # sys.stdout.write('\x1b[1A')
        # sys.stdout.write('\x1b[2K')
        log.info(f"    - found {category_total} shows in '{category_name}/{type_}' page ({reread} reread, {staled} staled)")
        save_all_shows(config, category_shows)

    log.info(f"  => Added {len(category_shows)} shows from '{category_name}' category / {already_known} were in nmultiple categories")
    return shows
