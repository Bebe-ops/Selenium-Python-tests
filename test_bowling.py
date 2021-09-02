"""
8 Feladat: Bowling eredménylap
Készíts egy Python python applikációt (egy darab python file) ami selenium-ot használ.
Feladatod, hogy automatizáld selenium webdriverrel az alábbi funkcionalitásokat a Bowling eredménylap appban:
Az ellenőrzésekhez használj `pytest` keretrendszert. A tesztjeidben `assert` összehasonlításokat használj!
"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

options = Options()
options.headless = False

driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=options)
URL = "https://witty-hill-0acfceb03.azurestaticapps.net/bowling-scorecard.html"
driver.get(URL)
time.sleep(2)

fields = [{"buttons": ["//button[contains(text(), 'Gutter')]", "//button[contains(text(), '1')]",
                       "//button[contains(text(), '2')]", "//button[contains(text(), '3')]",
                       "//button[contains(text(), '4')]", "//button[contains(text(), '5')]",
                       "//button[contains(text(), '6')]", "//button[contains(text(), '7')]",
                       "//button[contains(text(), '8')]", "//button[contains(text(), '9')]",
                       "//button[contains(text(), '10')]"]},
          {"frames": ["frame1", "frame2", "frame3", "frame4", "frame5", "frame6", "frame7", "frame8", "frame9",
                      "frame10"]},
          {"markers": ["marker0", "marker1", "marker2", "marker3", "marker4", "marker5", "marker6", "marker7",
                       "marker8", "marker9"]},
          {"invalid_roll_msg_id": "comments"}]


def rolls(t_data_list):
    for _ in t_data_list:
        if _ == 0:
            driver.find_element_by_xpath(fields[0]["buttons"][0]).click()
        elif _ != 0:
            element = driver.find_element_by_xpath(f"//button[contains(text(), '{_}')]")
            element.click()


def check_frames(t_data_list):
    for d, f in zip(t_data_list, fields[1]["frames"]):
        if d == ("X",) or d == ("",):
            data = str(d).strip("()").replace(",", "").replace("'", "")
        else:
            data = str(d).strip("()").replace(" ", "")
        assert driver.find_element_by_id(f).text == data


def check_markers(t_data_list):
    for exp, res in zip(t_data_list, fields[2]["markers"]):
        assert driver.find_element_by_id(res).text == str(exp)


def test_tc01_start_page():
    """
    Helyesen jelenik meg az üres eredmény kártya:
    * mind a 10 guritási mező üres
    * mind a 10 összegző mező üres
    """
    tc01_data = [{"frames_d": [("",), ("",), ("",), ("",), ("",), ("",), ("",), ("",), ("",), ("",)]},
                 {"markers_d": ["", "", "", "", "", "", "", "", "", ""]}]

    check_frames(tc01_data[0]["frames_d"])
    check_markers(tc01_data[1]["markers_d"])


def test_tc02_correct_rolls_adm():
    """
    Helyes gurítások adminisztrációja jól működik
    * gurítsunk sorrendben: 0,1,2,3,4,5,6,0,7,0,8,0,9,0,10,10,0,0
    * ellenőrizzük, hogy ezek a gruítások szerepelnek: [(0,1),(2,3),(4,5),(6,0),(7,0),(8,0),(9,0),(X),(X),(0,0)]
    * ellenőrizzük, hogy ezek az összegek szerepelnek: [1,6,15,21,28,36,45,55,65,75]
    """
    tc02_data = [{"rolls": [0, 1, 2, 3, 4, 5, 6, 0, 7, 0, 8, 0, 9, 0, 10, 10, 0, 0]},
                 {"frames_d": [(0, 1), (2, 3), (4, 5), (6, 0), (7, 0), (8, 0), (9, 0), ("X",), ("X",), (0, 0)]},
                 {"markers_d": [1, 6, 15, 21, 28, 36, 45, 55, 65, 75]}]

    rolls(tc02_data[0]["rolls"])
    check_frames(tc02_data[1]["frames_d"])
    check_markers(tc02_data[2]["markers_d"])


def test_tc03_error_msg():
    """
    Nem lehet egyszerre 11 bábut gurítani:
    * gurítsunk: 6, majd 5 bábút
    * ellezőrizzük, hogy a hibaüzenet ezt írja-e: `Invalid Roll - there are only ten pins!`
    """
    tc03_data = [{"rolls": [6, 5]}, {"invalid_roll_msg": "Invalid Roll - there are only ten pins!"}]

    driver.refresh()
    rolls(tc03_data[0]["rolls"])
    assert driver.find_element_by_id(fields[3]["invalid_roll_msg_id"]).text == tc03_data[1]["invalid_roll_msg"]
