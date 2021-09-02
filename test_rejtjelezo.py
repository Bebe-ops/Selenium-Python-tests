"""
Készíts egy Python python applikációt (egy darab python file) ami selenium-ot használ.
Feladatod, hogy automatizáld selenium webdriverrel a Caesar rejtjelező app tesztelését.

TC01: helybenhagyás
 * Szöveg: abcd
 * Eltolás: 26
 * Titkosított szöveg: abcd

TC02: titokítás
 * Szöveg: abcd
 * Eltolás: 2
 * Titkosított szöveg: cdef

TC03: dekódolás
 * Szöveg: cdef
 * Eltolás: -2
 * Titkosított szöveg: abcd
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import time

options = Options()
options.headless = False

driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=options)
URL = "https://witty-hill-0acfceb03.azurestaticapps.net/caesar.html"
driver.get(URL)
time.sleep(2)

fields = [{"text_id": "cypher"}, {"offset_id": "offset"}, {"encrypted_text_id": "finish"}]
test_data = [("abcd", 26, "abcd"), ("abcd", 2, "cdef"), ("cdef", -2, "abcd")]


def locator(e_id):
    element = driver.find_element_by_id(e_id)
    return element


def fill_fields(text, offset, exp_data):
    locator(fields[0]["text_id"]).clear()
    locator(fields[1]["offset_id"]).clear()
    locator(fields[0]["text_id"]).send_keys(text)
    locator(fields[1]["offset_id"]).send_keys(offset)
    locator(fields[1]["offset_id"]).send_keys(Keys.TAB)
    assert locator(fields[2]["encrypted_text_id"]).get_attribute("value") == exp_data


def test_tc01_no_encryption():
    fill_fields(test_data[0][0], test_data[0][1], test_data[0][2])


def test_tc02_encryption():
    fill_fields(test_data[1][0], test_data[1][1], test_data[1][2])


def test_tc03_decryption():
    fill_fields(test_data[2][0], test_data[2][1], test_data[2][2])
