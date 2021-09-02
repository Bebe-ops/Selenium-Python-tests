"""
Készíts egy Python python applikációt (egy darab python file) ami selenium-ot használ.
Feladatod, hogy automatizáld selenium webdriverrel a Stopper kihívás app tesztelését.
TC01: iduláskor a stopper 00:00:00 értéket mutat
TC02: 6 másodperchez közel megállítás +-1 mp-en belül
 - Itt az a kihívás, hogy a start link megnyomása után pontosan 6 másodperc
   után picivel nyomjuk meg a stop gombot és nézzük meg, hogy az óra 00:06:00 és 00:06:99 között állt meg
TC03: újrakezdés és stop után az óra kissebb értéket mutat, mint azelőtt, tehát újra indítható
 - Itt az a kihívás, hogy a restart nem egyszerűen leállítja az órát, hanem el is indítja a stoppert.
   Ezért egyből egy stop linket is kell nyomni, hogy megáljon és vizsgálhassuk a feltételt.
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

options = Options()
options.headless = False

driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=options)
URL = "https://witty-hill-0acfceb03.azurestaticapps.net/stopwatch.html"
driver.get(URL)
time.sleep(2)

fields = [{"stop_watch_class": "stopwatch"}, {"start_id": "start"}, {"lap_id": "lap"}, {"stop_id": "stop"},
          {"restart_id": "restart"}, {"clear_id": "clear_laps"}, {"results_xp": "//ul[@class='results']/li"}]
test_data = [("00: 00: 00", ), ("00: 06: 00", "00: 06: 99")]


def locator_by_id(e_id):
    element = driver.find_element_by_id(e_id)
    return element


def locator_by_class(c_name):
    element = driver.find_element_by_class_name(c_name)
    return element


def locator_by_xp(xp):
    element = driver.find_element_by_xpath(xp)
    return element


def test_tc01():
    assert locator_by_class(fields[0]["stop_watch_class"]).text == test_data[0][0]


def test_tc02():
    locator_by_id(fields[1]["start_id"]).click()
    time.sleep(6)
    locator_by_id(fields[3]["stop_id"]).click()
    locator_by_id(fields[2]["lap_id"]).click()
    result = locator_by_xp(fields[6]["results_xp"]).text
    result_num = result.replace(":", "").split(" ")
    start = test_data[1][0].replace(":", "").split(" ")
    end = test_data[1][1].replace(":", "").split(" ")

    assert result_num[1] == start[1]
    assert int(result_num[2]) >= int(start[2])
    assert int(result_num[2]) < int(end[2])


def test_tc03():
    previous = locator_by_class(fields[0]["stop_watch_class"]).text.replace(":", "").split(" ")
    locator_by_id(fields[4]["restart_id"]).click()
    locator_by_id(fields[3]["stop_id"]).click()
    locator_by_id(fields[2]["lap_id"]).click()
    actual = locator_by_class(fields[0]["stop_watch_class"]).text.replace(":", "").split(" ")
    assert int(actual[0]) <= int(previous[0])
    assert int(actual[1]) < int(previous[1])
