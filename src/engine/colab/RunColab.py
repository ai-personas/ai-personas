import argparse
import pickle
from pathlib import Path
from time import sleep

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from engine.colab.ColabConstants import *

def get_colab_run_commands(personaName):
    with open('resources/colab_run_commands.txt', 'r') as file:
        data = file.read()
        return data

def is_class_present(driver, class_name):
    try:
        driver.find_element_by_xpath("//div[contains(@class, '"+class_name+"')]")
    except NoSuchElementException:
        return False
    return True

def run_colab(personaName):
    run_commands = get_colab_run_commands(personaName)
    chrome_options = Options()
    # chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    wd = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)

    # load page
    wd.get(COLAB_URL)

    # add cookies if exists
    if Path(COOKIES_FILEPATH).exists():
        for cookie in pickle.load(open(COOKIES_FILEPATH, "rb")):
            # 'expiry' cookie is causing problem after Chrome 74
            # https://github.com/jimmy927/requestium/commit/596db69d18926981df23988e96ca33c361badb40
            cookie.pop('expiry', None)
            wd.add_cookie(cookie)
    else:
        print('start auth_google.py first !')

    # create new notebook using 'File' menu
    wd.find_element_by_xpath('//*[@id="file-menu-button"]/div/div/div[1]').click()
    wd.find_elements_by_xpath("//div[text()='New notebook']")[0].click()
    wd.switch_to.window(wd.window_handles[1])
    sleep(5)

    # change runtime type for colab
    wd.find_element_by_xpath('//*[@id="runtime-menu-button"]/div/div/div[1]').click()
    wd.find_element_by_xpath('//*[@id=":27"]/div').click()
    wd.find_element_by_xpath('//select[@id="accelerator"]/option[text()="GPU"]').click()
    # change to High-RAM for colab pro
    # wd.find_element_by_xpath('//select[@id="shape"]/option[text()="High-RAM"]').click()
    wd.find_element_by_xpath('//*[@id="ok"]').click()
    cell = wd.find_elements_by_css_selector("textarea")[0]
    cell.send_keys(run_commands)

    # run all cells
    ActionChains(wd).key_down(Keys.CONTROL).send_keys('[').perform()
    sleep(3)
    ActionChains(wd).key_down(Keys.CONTROL).key_down(Keys.F9).perform()
    sleep(10)
    wait = WebDriverWait(wd, 1000)
    wait.until(lambda driver: not is_class_present(driver, 'running'))

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Train Persona')
    parser.add_argument('--persona', required=True, help='persona name')
    args = parser.parse_args()
    run_colab(args.persona)
