"""
Készíts egy Python python applikációt (egy darab python file) ami selenium-ot használ.
Feladatod, hogy automatizáld selenium webdriverrel a password mező app tesztelését.
A cél az password validáció tesztelése:
* Helyes kitöltés esete:
    * email: teszt@elek.hu
    * jelszó: Kiscica1234
    * A Submit gomb megnyomása után átnavigál egy oldalra ahol a "404 Not Found" hibaüzenet látha.Ezt kell assertezned.
* Helytelen:
    * email: teszt@elek.hu
    * jelszó: a1
    * Megjelenik egy üzenet ami megmondja, mit kell tartalmazni a jelszónak. Ellenőrizd le, hogy:
      * number ellnőrzés valid jelzés ad
      * letter ellnőrzés valid jelzés ad
      * capital ellnőrzés invalid jelzés ad
      * length ellnőrzés invalid jelzés ad
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = Options()
options.headless = False

driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=options)
URL = "https://wonderful-pond-0d96a8503.azurestaticapps.net/f4.html"


test_data = [('teszt@elek.hu', 'Kiscica1234', '404: Not Found'),
             ('teszt@elek.hu', 'a1', 'valid', 'valid', 'invalid', 'invalid',
              'Must contain at least one number and one uppercase and lowercase letter, and at least 8 or more '
              'characters')]

fields = [{'user_name': 'usrname'},
          {'password': 'psw'},
          {'submit_xp': '//input[@type="submit"]'},
          {'title_text': 'titleText'},
          {'letter_msg': 'letter'},
          {'number_msg': 'number'},
          {'capital_msg': 'capital'},
          {'length_msg': 'length'}]


def locator(l_id):
    element = driver.find_element_by_id(l_id)
    return element


def locator_by_xpath(xp):
    element = driver.find_element_by_xpath(xp)
    return element


def fill_fields(user_n_data, user_pwd_data):
    locator(fields[0]['user_name']).clear()
    locator(fields[1]['password']).clear()
    locator(fields[0]['user_name']).send_keys(user_n_data)
    locator(fields[1]['password']).send_keys(user_pwd_data)
    locator_by_xpath(fields[2]['submit_xp']).click()


def test_correct_filling():
    driver.get(URL)
    time.sleep(1)
    fill_fields(test_data[0][0], test_data[0][1])
    time.sleep(1)
    assert locator(fields[3]['title_text']).text == test_data[0][2]
    time.sleep(2)


def assert_validation_msgs(letter, number, capital, length):
    assert locator(fields[4]['letter_msg']).get_attribute("class") == letter
    assert locator(fields[5]['number_msg']).get_attribute("class") == number
    assert locator(fields[6]['capital_msg']).get_attribute("class") == capital
    assert locator(fields[7]['length_msg']).get_attribute("class") == length


def test_incorrect_filling():
    driver.back()
    fill_fields(test_data[1][0], test_data[1][1])
    # felugró buborék validáció ellenőrzése
    msg = WebDriverWait(driver, 5).until(EC.visibility_of_element_located(
        (By.ID, fields[1]['password']))).get_attribute("title")
    assert msg is not None
    assert msg == test_data[1][6]
    # jelszó validáció üzenet ell.
    assert_validation_msgs(test_data[1][2], test_data[1][3], test_data[1][4], test_data[1][5])

    driver.close()
