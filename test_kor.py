"""
Feladatod, hogy automatizáld selenium webdriverrel az alábbi funkcionalitásokat a kör területe appban:
* Helyes kitöltés esete:
    * r: 10
    * Eredmény: 314

* Nem számokkal történő kitöltés:
    * r: kiscica
    * Eredmény: NaN

* Üres kitöltés:
    * r: <üres>
    * Eredmény: NaN
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

options = Options()
options.headless = False

driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=options)
URL = "https://wonderful-pond-0d96a8503.azurestaticapps.net/f1.html"
driver.get(URL)
time.sleep(2)

test_data = [(10, 314), ("kiscica", "NaN"), ("", "NaN")]
fields = [{'r_field_id': 'r'}, {'submit_id': 'submit'}, {'result_id': 'result'}]


def locator(l_id):
    element = driver.find_element_by_id(l_id)
    return element


def locator_by_xp(xp):
    element = driver.find_element_by_id(xp)
    return element


def clear_and_fill_field(t_data):
    locator(fields[0]['r_field_id']).clear()
    locator(fields[0]['r_field_id']).send_keys(t_data)
    locator(fields[1]['submit_id']).click()


def test_correct_filling():
    clear_and_fill_field(test_data[0][0])
    assert test_data[0][1] == int(locator(fields[2]['result_id']).text)  


def test_string_filling():
    clear_and_fill_field(test_data[1][0])
    assert test_data[1][1] == locator(fields[2]['result_id']).text


def test_empty_filling():
    clear_and_fill_field(test_data[2][0])
    assert test_data[2][1] == locator(fields[2]['result_id']).text
