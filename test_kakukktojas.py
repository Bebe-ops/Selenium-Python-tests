"""
Készíts egy Python python applikációt (egy darab python file) ami selenium-ot használ.
Feladatod, hogy automatizáld selenium webdriverrel a Kakukktojás - nevek app tesztelését.
Az applikáció minden frissítésnél véletlenszerűen változik!
Feladatod, hogy megtaláld azt a nevet, ami **csupa nagyvetűvel** van írva és kitöltsd a form-ban a mezőt és ellnörizd
le, hogy eltaláltad-e.
A feladatnak több helyes megoldása is van (találgatós/ismétlős, pythonban kalkulálós), mindegy, hogy hogyan oldod meg,
csak találd meg a nevet ami nagybetűvel van írva.
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

options = Options()
options.headless = False

driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=options)
URL = "https://wonderful-pond-0d96a8503.azurestaticapps.net/f5.html"
driver.get(URL)
time.sleep(2)

fields = [{"textarea_id": "names"}, {"random_names_xp": "//ul[@id='randomNames']/li"},
          {"capital_name_id": "allcapsName"}, {"submit_id": "submit"}, {"result_id": "result"}]

test_data = 'Eltaláltad.'


def locator_by_id(e_id):
    element = driver.find_element_by_id(e_id)
    return element


def locators_by_xp(xp):
    elements = driver.find_elements_by_xpath(xp)
    return elements


textarea = locator_by_id(fields[0]["textarea_id"]).text
textarea_list = textarea.replace('"', '').split(', ')

random_names = locators_by_xp(fields[1]["random_names_xp"])
random_names_list = []
for _ in random_names:
    random_names_list.append(_.text)


def test_capital_name():
    for _ in textarea_list:
        if _ in random_names_list:
            continue
        else:
            locator_by_id(fields[2]["capital_name_id"]).send_keys(_)
            locator_by_id(fields[3]["submit_id"]).click()
            assert locator_by_id(fields[4]["result_id"]).text == test_data
