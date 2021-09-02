"""
A program töltse be a sales Film register app-ot az https://witty-hill-0acfceb03.azurestaticapps.net/film_register.html
oldalról.
Feladatod, hogy automatizáld az alkalmazás két funkciójának a tesztelését
Teszteld le, hogy betöltés után megjelennek filmek az alkalmazásban, méghozzá 24 db.
Teszteld le, hogy fel lehet-e venni az alábbi adatokkal egy új filmet:
Film title: Black widow
Release year: 2021
Chronological year of events: 2020
Trailer url: https://www.youtube.com/watch?v=Fp9pNPdNwjI
Image url: https://m.media-amazon.com/images/I/914MHuDfMSL._AC_UY327_FMwebp_QL65_.jpg
Film summary: https://www.imdb.com/title/tt3480822/
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

options = Options()
options.headless = False

driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=options)
URL = "https://witty-hill-0acfceb03.azurestaticapps.net/film_register.html"
driver.get(URL)

time.sleep(6)
fields = [{"films_xp": "//img"}, {"register_xp": "//button[@class='mostra-container-cadastro']"},
          {"reg_fields_xp": "//input"}, {"save_xp": "//button[contains(text(), 'Save')]"}, {"": ""}]
test_data = [{"all_movies": 24}, {"film_title": "Black widow"}, {"Release year": "2021"},
             {"chronological_year_of_events": "2020"}, {"trailer_url": "https://www.youtube.com/watch?v=Fp9pNPdNwjI"},
             {"image_url": "https://m.media-amazon.com/images/I/914MHuDfMSL._AC_UY327_FMwebp_QL65_.jpg"},
             {"film_summary": "https://www.imdb.com/title/tt3480822/"}]


def locators_by_xp(xp):
    elements = driver.find_elements_by_xpath(xp)
    return elements


def locator_by_xp(xp):
    element = driver.find_element_by_xpath(xp)
    return element


def test_tc01_basic():  # betöltés után megjelennek filmek az alkalmazásban, méghozzá 24 db.
    all_movies = locators_by_xp(fields[0]["films_xp"])
    assert len(all_movies) == test_data[0]["all_movies"]


def test_tc02_add_new_movie():  # új film felvitele
    locator_by_xp(fields[1]["register_xp"]).click()
    time.sleep(2)
    for field, dic in zip(locators_by_xp(fields[2]["reg_fields_xp"]), test_data[1:]):
        for value in dic.values():
            field.send_keys(value)
    locator_by_xp(fields[3]["save_xp"]).click()
    all_movies = locators_by_xp(fields[0]["films_xp"])
    time.sleep(2)
    assert len(all_movies) == test_data[0]["all_movies"] + 1
    assert len(locators_by_xp(f"//div/h2[starts-with(text(), '{test_data[1]['film_title']}')]")) == 1
