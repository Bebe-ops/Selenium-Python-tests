"""
Készíts egy Python python applikációt (egy darab python file) ami selenium-ot használ.
Feladatod, hogy automatizáld selenium webdriverrel a  véletlen kalkulátor app tesztelését.
Az applikáció minden frissítésnél véletlenszerűen változik!
A feladatod, hogy a random számokkal működő matematikai applikációt ellenőrizd.
A teszted ki kell, hogy olvassa a két operandust (számot) és az operátort (műveleti jelet).
Ennek megfelelően kell elvégezned a kalkulációt Pythonban.
A kalkulátor gombra kattintva mutatja meg az applikáció, hogy mi a művelet eredménye szerinte.
Hasonlítsd össze az applikáció által kínált megoldást és a Python által kalkulált eredményt.
Ennek a kettőnek egyeznie kell.
"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

options = Options()
options.headless = False

driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=options)
URL = "https://wonderful-pond-0d96a8503.azurestaticapps.net/f3.html"
driver.get(URL)
time.sleep(2)

fields = [{'num1_id': 'num1'}, {'num2_id': 'num2'}, {'num3_id': 'num3'}, {'op1_id': 'op1'}, {'op2_id': 'op2'},
             {'submit_id': 'submit'}, {'result_id': 'result'}]


def locator(field_id):
    element = driver.find_element_by_id(field_id)
    return element


def test_calculate():
    locator(fields[5]['submit_id']).click()
    ex = eval(f"{locator(fields[0]['num1_id']).text}{locator(fields[3]['op1_id']).text}"
              f"{locator(fields[1]['num2_id']).text}{locator(fields[4]['op2_id']).text}"
              f"{locator(fields[2]['num3_id']).text}")
    assert int(locator(fields[6]['result_id']).text) == ex
