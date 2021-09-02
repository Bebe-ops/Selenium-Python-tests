"""
Feladatod, hogy automatizáld selenium webdriverrel az app funkcionalitását tesztelését.
Egy tesztet kell írnod ami addig találgat a megadott intervallumon belül amíg ki nem találja a helyes számot.
Nem jár plusz pont azért ha úgy automatizálsz, hogy minnél optimálisabban és gyorsabban találja ki a helyes számot
a program.
Amikor megvan a helyes szám, ellenőrizd le, hogy a szükséges lépések száma amit az aplikáció kijelez egyezik-e a saját
belső számlálóddal.
Teszteld le, hogy az applikáció helyesen kezeli az intervallumon kívüli találgatásokat. Az applikéció -19 vagy 255
értéknél nem szabad, hogy összeomoljon. Azt kell kiírnia, hogy alá vagy fölé találtál-e.
"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

options = Options()
options.headless = False

driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=options)
URL = "https://witty-hill-0acfceb03.azurestaticapps.net/guess_the_number.html"

driver.get(URL)
time.sleep(2)

fields = [{"guess": "//input[@type='number']"}, {"guess_btn": "//button[contains(text(), 'Guess')]"},
          {"warn_alert": "//p[@class='alert alert-warning']"},
          {"success_alert": "//p[contains(text(), 'Yes! That is it.')]"},
          {"num_of_guesses": "//p/span[@class='badge ng-binding']"},
          {"restart_btn": "//button[contains(text(), 'Restart')]"}]

test_data = [(1, 101, "Yes! That is it."), (-19, "Guess higher."), (255, "Guess lower.")]


def locator_by_xp(xp):
    element = driver.find_element_by_xpath(xp)
    return element


index = 0


def test_tc01_guessing():
    global index
    for index, value in enumerate(range(test_data[0][0], test_data[0][1])):
        locator_by_xp(fields[0]["guess"]).clear()
        locator_by_xp(fields[0]["guess"]).send_keys(value)
        locator_by_xp(fields[1]["guess_btn"]).click()
        index += 1
        if locator_by_xp(fields[3]["success_alert"]).is_displayed():
            break
        else:
            continue
    number_of_guesses = locator_by_xp(fields[4]["num_of_guesses"]).text
    assert int(number_of_guesses) == index


def exception(test_num, test_msg):
    locator_by_xp(fields[0]["guess"]).clear()
    locator_by_xp(fields[0]["guess"]).send_keys(test_num)
    locator_by_xp(fields[1]["guess_btn"]).click()
    w_alert = locator_by_xp(fields[2]["warn_alert"]).text
    assert w_alert == test_msg


def test_tc02_higher():
    exception(test_data[1][0], test_data[1][1])


def test_tc03_lower():
    exception(test_data[2][0], test_data[2][1])


def test_tc04_out_of_range():
    number_of_guesses = locator_by_xp(fields[4]["num_of_guesses"]).text
    assert int(number_of_guesses) == index + 2
