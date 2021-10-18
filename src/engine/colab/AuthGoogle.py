import pickle
import time

import undetected_chromedriver.v2 as uc
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.wait import WebDriverWait

from engine.colab.ColabConstants import *


def has_text(driver, text):
    driver.implicitly_wait(2)
    try:
        driver.find_element_by_xpath("//*[contains(text(), '" + str(text) + "')]")
    except NoSuchElementException:
        driver.implicitly_wait(5)
        return False
    driver.implicitly_wait(5)
    return True


def wait_for_xpath(driver, x):
    while True:
        try:
            driver.find_element_by_xpath(x)
            return True
        except:
            time.sleep(0.1)
            pass


def auth_user():
    chrome_options = uc.ChromeOptions()
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_options.add_argument("--profile-directory=Default")
    chrome_options.add_argument("--disable-plugins-discovery")
    chrome_options.add_argument("--incognito")
    # chrome_options.add_argument("user_agent=DN")

    wd = uc.Chrome(options=chrome_options)

    wd.delete_all_cookies()
    wd.get(GOOGLE_SIGNIN_URL)
    time.sleep(2)

    wait = WebDriverWait(wd, 100)
    wait.until(lambda driver: GOOGLE_SIGNED_URL in driver.current_url)
    wd.get(COLAB_URL)
    pickle.dump(wd.get_cookies(), open(COOKIES_FILEPATH, "wb"))

    wd.close()
    print("Cookies saved. You can start run.py")


if __name__ == '__main__':
    auth_user()
