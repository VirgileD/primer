from requests import get
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from list_helpers.misc import safe_wait
from list_helpers.browser import load_cookies, save_cookies
import time
import sys
from utils.logmngt import get_logger

from utils.logmngt import get_logger


def login_process(config, browser):
    log = get_logger("login_process", cfg=config)
    log.debug("Handling login process")
    
    if load_cookies(browser):
        browser.refresh()

    # either not connected or connected thanks to cookies
    WebDriverWait(browser, 30).until(expected_conditions.any_of(expected_conditions.title_contains("Welcome to Prime Video"),
                                    expected_conditions.title_contains("Prime Video | "),))
    if browser.title == "Welcome to Prime Video":
        log.info(f"Sign-in required")
        #time.sleep(10)
        element = browser.find_element(By.XPATH, "//a[contains(text(), 'Sign In')]")
        browser.get(element.get_attribute("href"))

        # get the a tag with the id set to "nav-link-accountList"
        WebDriverWait(browser, 30).until(expected_conditions.title_contains("Amazon Sign-In"))
        # find the element with the id set to "ap_email"
        WebDriverWait(browser, 30).until(expected_conditions.presence_of_element_located((By.ID, "ap_email")))
        log.debug("Entering email")
        try:
            element = browser.find_element(By.ID, "ap_email")
            element.send_keys(config['email'])
            # find the element with the id set to "continue"
            element = browser.find_element(By.ID, "continue")
            element.click()
        except:
            log.error("Can't reach the email page")
            exit()

        WebDriverWait(browser, 30).until(expected_conditions.presence_of_element_located((By.ID, "ap_password")))
        try:
            # first set the remember me checkbox
            log.debug("Entering password")
            element = browser.find_element(By.XPATH, "//input[@type='checkbox']")
            if not element.get_attribute('checked'):
                element.click()
            element = browser.find_element(By.ID, "ap_password")
            element.send_keys(config['password'])
            element = browser.find_element(By.ID, "signInSubmit")
            element.click()
        except Exception as e:
            log.error("Can't reach the password page")
            exit()

        WebDriverWait(browser, 30).until(expected_conditions.title_is("Two-Step Verification"))
        log.info("Two-Step Verification required")
        try:
            otp = input("Enter the OTP: ")
            # TODO: if empty code extract "the resend code" link and try that
            element = browser.find_element(By.ID, "auth-mfa-otpcode")
            element.send_keys(otp)
            element = browser.find_element(By.ID, "auth-signin-button")
            element.click()
        except:
            log.error("Can't reach the OTP page")
            exit()
    else:
        log.info(f"Already signed in")

    save_cookies(browser)