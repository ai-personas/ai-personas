import argparse
import pickle
from pathlib import Path
from time import sleep

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from engine.colab.AuthGoogle import auth_user
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

def is_id_present(driver, id_name):
    try:
        driver.find_element_by_xpath('//*[@id="'+id_name+'"]')
    except NoSuchElementException:
        return False
    return True

def is_tag_present(driver, tag_name):
    try:
        driver.find_element_by_xpath("//" + tag_name)
    except NoSuchElementException:
        return False
    return True

def expand_find_element_by_xpath(root, shadow_root_xpath, local_xpath):
    element = root.find_element_by_xpath(shadow_root_xpath)
    shadow_root = root.execute_script('return arguments[0].shadowRoot', element)
    for elem in shadow_root.find_elements_by_tag_name("*"):
        try:
            result = elem.find_element_by_xpath('.' + local_xpath)
            return result
        except NoSuchElementException:
            pass

    return None

def is_text_present(root, text):
    try:
        root.find_element_by_xpath("//*[contains(text(),'" + text + "')]")
    except NoSuchElementException:
        return False
    return True

def is_text_present_inside_elem(root, text):
    try:
        root.find_element_by_xpath(".//*[contains(text(),'" + text + "')]")
    except NoSuchElementException:
        return False
    return True

def create_new_notebook(driver, notebook_name):
    # create new notebook using 'File' menu
    driver.find_element_by_xpath('//*[@id="file-menu-button"]/div/div/div[1]').click()
    driver.find_elements_by_xpath("//div[text()='New notebook']")[0].click()
    driver.switch_to.window(driver.window_handles[1])
    wait = WebDriverWait(driver, 10)
    wait.until(lambda driver: is_id_present(driver, 'doc-name'))
    doc_elem = driver.find_element_by_xpath('//*[@id="doc-name"]')
    doc_elem.clear()
    doc_elem.send_keys(notebook_name)

def terminate_same_notebook_session(driver, notebook_name):
    driver.find_element_by_xpath('//*[@id="runtime-menu-button"]/div/div/div[1]').click()
    driver.find_element_by_xpath('//*[@id=":29"]/div').click()
    sleep(5)
    try:
        colab_session_elem = expand_find_element_by_xpath(driver,
                                                          "//paper-dialog/colab-sessions-dialog",
                                                          "//colab-session")
        # terminate session
        if colab_session_elem is not None:
            colab_session_elem.find_element_by_xpath(".//paper-button").click()
        sleep(10)
        # close session dialogue
        colab_session_close_elem = expand_find_element_by_xpath(driver,
                                                          "//paper-dialog/colab-sessions-dialog",
                                                          "//paper-button")
        colab_session_close_elem.click()
    except Exception:
        pass

def change_colab_runtime(driver, runtime_type):
    wait = WebDriverWait(driver, 10)
    wait.until(lambda driver: is_id_present(driver, 'runtime-menu-button'))
    driver.find_element_by_xpath('//*[@id="runtime-menu-button"]/div/div/div[1]').click()
    driver.find_element_by_xpath('//*[@id=":27"]/div').click()
    driver.find_element_by_xpath('//select[@id="accelerator"]/option[text()="'+runtime_type+'"]').click()
    # change to High-RAM for colab pro
    # wd.find_element_by_xpath('//select[@id="shape"]/option[text()="High-RAM"]').click()
    driver.find_element_by_xpath('//*[@id="ok"]').click()
    # change colab notebook name

def run_colab(personaName):
    # authenticate user if cookie file doesn't exist
    if not Path(COOKIES_FILEPATH).exists():
        auth_user()

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
        print('Cookie file is missing!!!')

    notebook_name = 'aipersona_' + personaName + '.ipynb'

    # create new notebook
    create_new_notebook(wd, notebook_name)

    # terminate session if name of the running notebook is same as current notebook name
    terminate_same_notebook_session(wd, notebook_name)

    # change runtime type for colab
    change_colab_runtime(wd, 'GPU')

    # paste colab commands in the code cell
    cell = wd.find_elements_by_css_selector("textarea")[0]
    cell.send_keys(run_commands)

    # run all cells
    ActionChains(wd).key_down(Keys.CONTROL).send_keys('[').perform()
    sleep(3)
    ActionChains(wd).key_down(Keys.CONTROL).key_down(Keys.F9).perform()
    sleep(10)

    # wait until all running cells are complete
    wait = WebDriverWait(wd, 1000000)
    wait.until(lambda driver: not is_class_present(driver, 'running'))

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Train Persona')
    parser.add_argument('--persona', required=True, help='persona name')
    args = parser.parse_args()
    run_colab(args.persona)
