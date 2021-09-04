"""
## 9 Feladat: Találd ki a filmet
Készíts egy Python python applikációt (egy darab python file) ami selenium-ot használ.
Feladatod, hogy automatizáld selenium webdriverrel az alábbi funkcionalitásokat a Találd ki a filmet appban:
Az ellenőrzésekhez használj `pytest` keretrendszert. A tesztjeidben `assert` összehasonlításokat használj!

* Helyesen jelenik meg az applikáció:
    * minden strike gomb zöld
    * egy gomb sincs lenyomva

* Helyesen működik us film-re az applikáció
    * Tallágassunk és végig ellenőrizzük, hogy a megfelelő karakterek jelennek-e
    * Ha kitaláljuk 4 találgatásból, akkor jó üzenet jelenik-e meg.

* Helytelenül találgatunk akkor működik-e az applikáció:
    * Tallágassunk és végig ellenőrizzük, hogy a megfelelő karakterek jelennek-e
    * Most ne találjuk el 4 találgatásból, akkor jó üzenet jelenik-e meg.
"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

options = Options()
options.headless = False

driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=options)
URL = "https://witty-hill-0acfceb03.azurestaticapps.net/imdb_guessmovie.html"
driver.get(URL)
time.sleep(2)

fields = [{"strikes": "//div[@class='strike']"}, {"country_btn_us": "//input[@value='us']"},
          {"keyboard_buttons": "//div[@id='keyboard']//button"}, {"pos_test_char_id": ["M", "E", "N", "T", "O"]},
          {"result": "//div[@id='game']/h2"}, {"confirm_btn": "confirmNext"},
          {"neg_test_char_id": ["S", "1", "Q", "T", "X", "E", "Y"]}]
test_data = [{"strike_b_color": "rgba(144, 238, 144, 1)"}, {"wrong_strike_b_color": "rgba(255, 0, 0, 1)"},
             {"keyboard_btn_class": "key"}, {"pressed_keyboard_btn_class": "key keyOn"}, {"result": "M E M E N T O"},
             {"r_confirm": "Well Done! You've Guessed it Right."}, {"w_confirm": "You've Guessed it Wrong."},
             {"right_char_color": "rgba(0, 128, 0, 1)"}, {"wrong_char_color": "rgba(255, 0, 0, 1)"}]


def locators_by_xp(xp):
    elements = driver.find_elements_by_xpath(xp)
    return elements


def locator_by_xp(xp):
    element = driver.find_element_by_xpath(xp)
    return element


def locator_by_id(e_id):
    element = driver.find_element_by_id(e_id)
    return element


def guessing_movies_from_us(chars):
    if locator_by_xp(fields[1]["country_btn_us"]).is_displayed():
        locator_by_xp(fields[1]["country_btn_us"]).click()
    else:
        locator_by_id(fields[5]["confirm_btn"]).click()
    time.sleep(2)
    for _ in chars:
        locator_by_id(_).click()
        attribute_value = locator_by_id(_).get_attribute("class")
        assert attribute_value == test_data[3]["pressed_keyboard_btn_class"]
        char_color = locator_by_id(_).value_of_css_property("background-color")
        if char_color == test_data[8]["wrong_char_color"]:
            continue
        else:
            assert locator_by_id(_).text in locator_by_xp(fields[4]["result"]).text


def check_confirm_text(test_d_confirm):
    full_text = locator_by_id(fields[5]["confirm_btn"]).text
    confirm_text = full_text.split("\n")
    assert confirm_text[0] == test_d_confirm


def test_start_app_tc01():
    """ Helyesen jelenik meg az applikáció: minden strike gomb zöld, egy gomb sincs lenyomva """

    strikes = locators_by_xp(fields[0]["strikes"])
    for _ in strikes:
        background_color = _.value_of_css_property("background-color")
        assert background_color == test_data[0]["strike_b_color"]

    keyboard_buttons = locators_by_xp(fields[2]["keyboard_buttons"])
    for _ in keyboard_buttons:
        attribute_value = _.get_attribute("class")
        assert attribute_value == test_data[2]["keyboard_btn_class"]
        assert attribute_value != test_data[3]["pressed_keyboard_btn_class"]


def test_film_from_us_tc02():
    """
    Helyesen működik us film-re az applikáció:
    * Tallágassunk és végig ellenőrizzük, hogy a megfelelő karakterek jelennek-e
    * Ha kitaláljuk 4 találgatásból, akkor jó üzenet jelenik-e meg.
    """
    guessing_movies_from_us(fields[3]["pos_test_char_id"])
    assert locator_by_xp(fields[4]["result"]).text == test_data[4]["result"]
    time.sleep(3)
    check_confirm_text(test_data[5]["r_confirm"])


def test_wrong_guessing_tc03():
    """
    Helytelenül találgatunk akkor működik-e az applikáció:
    * Tallágassunk és végig ellenőrizzük, hogy a megfelelő karakterek jelennek-e
    * Most ne találjuk el 4 találgatásból, akkor jó üzenet jelenik-e meg.
    """
    guessing_movies_from_us(fields[6]["neg_test_char_id"])
    check_confirm_text(test_data[6]["w_confirm"])
