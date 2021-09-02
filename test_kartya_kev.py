"""
Készíts egy Python python applikációt (egy darab python file) ami selenium-ot használ.
Feladatod, hogy automatizáld selenium webdriverrel a kártyakeverő app tesztelését.
Az alkalmazás akkor működik helyesen ha 52 gombnyomásból legalább van 4db 9-es szám. Ezt kell ellenőrizned.
"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

options = Options()
options.headless = False

driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=options)
URL = "https://wonderful-pond-0d96a8503.azurestaticapps.net/f2.html"
driver.get(URL)
time.sleep(2)

fields = [{'paragraph': '//p'},
          {'card_btn': 'submit'},
          {'last_card': 'lastResult'},
          {'card_history': 'deck'}]

test_data = [('Van egy pakli kártyád, valódi váletlen keveréssel:',), ('Húzzunk egy kártyát',), ('utolsó kártya:',),
             ('kártya röténelem:',), (4,)]


def locator_by_id(l_id):
    element = driver.find_element_by_id(l_id)
    return element


def locator_by_xpath(xp):
    element = driver.find_element_by_xpath(xp)
    return element


# Testcase 01
# ell: paragraph szövege és láthatósága
# ell: huzzunk egy kártyát gomb szövege és láthatósága
def test_text_and_visible():
    assert test_data[0][0] == locator_by_xpath(fields[0]['paragraph']).text
    assert locator_by_xpath(fields[0]['paragraph']).is_displayed()

    assert test_data[1][0] == locator_by_id(fields[1]['card_btn']).text
    assert locator_by_id(fields[1]['card_btn']).is_displayed()


# Testcase 02
# üres a 2 mező: "utolsó kártya és kártya röténelem"
def test_empty_values():
    assert locator_by_id(fields[2]['last_card']).text == ""
    assert locator_by_id(fields[3]['card_history']).text == ""


# Tescase 03
def test_correct_operation():
    nines = 0
    for _ in range(52):
        locator_by_id(fields[1]['card_btn']).click()
        if locator_by_id(fields[2]['last_card']).text.startswith("9"):
            nines += 1
            print(locator_by_id(fields[2]['last_card']).text)
    assert test_data[4][0] == nines
