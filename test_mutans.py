"""
A Marvel új web alapú rajongó oldalt készít az X-man képregény adaptációkból.
Teszteld le, hogy a különböző szűrőfeltételek alapján megfelelő karaktereket mutatja az oldal.
Tehát mondjuk `iceman` pontosan az `original` és a `factor` csapatban van benne és a `hellfire` illetve a `force`
csapatokban nincs benne.
(Figyelem: ne engedd, hogy az oldal dinamikus működése elvonja a figyelmed a célról!
A karaktereket csoporthoz tartozását nem feltétlenül a felület változásával tudod ellenőrizni.)
Az alkalmazás helyesen mutatja a felületen a csoporthoz tartozást. Nincs külön tesztadat leírás ehhez a feladathoz,
tehát a látottak alapján kell a tesztadatot összeállítanod.
"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
from pprint import pprint

options = Options()
options.headless = False

driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=options)

driver.get("https://witty-hill-0acfceb03.azurestaticapps.net/mutant_teams.html")
time.sleep(2)

fields = [{"orig_group_xp": "//label[@for='original']"}, {"force_group_xp": "//label[@for='force']"},
          {"factor_group_xp": "//label[@for='factor']"},
          {"hellfire_group_xp": "//label[@for='hellfire']"}, {"characters_xp": "//ul/li"},
          {"iceman_xp": "//*[@id='iceman']/h2"}]

test_data = [{"original_group": ['Angel', 'Beast', 'Cyclops', 'Iceman', 'Jean Grey', 'Professor X']},
             {"force_group": ['Angel', 'Cyclops', 'Nightcrawler', 'Psylocke', 'Rictor', 'Storm', 'Sunspot',
                              'Wolverine']},
             {"factor_group": ['Angel', 'Beast', 'Cyclops', 'Iceman', 'Jean Grey', 'Quicksilver', 'Rictor']},
             {"hellfire_group": ['Angel', 'Emma Frost', 'Magneto', 'Psylocke', 'Storm', 'Sunspot', 'Tithe']}]


def locator_by_xp(xp):
    element = driver.find_element_by_xpath(xp)
    return element


def locators_by_xp(xp):
    elements = driver.find_elements_by_xpath(xp)
    return elements


def get_characters_in_group(label_xp, group_list, test_d):
    locator_by_xp(label_xp).click()
    group = locators_by_xp(fields[4]["characters_xp"])
    for character in group:
        if character.is_displayed():
            if character.text != "":
                group_list.append(character.text)
    assert group_list == test_d


def test_tc01_original_group():
    original_group_list = []
    get_characters_in_group(fields[0]["orig_group_xp"], original_group_list, test_data[0]["original_group"])
    assert locator_by_xp(fields[5]["iceman_xp"]).text in original_group_list


def test_tc02_force_group():
    force_group_list = []
    get_characters_in_group(fields[1]["force_group_xp"], force_group_list, test_data[1]["force_group"])
    assert locator_by_xp(fields[5]["iceman_xp"]).text not in force_group_list


def test_tc03_factor_group():
    factor_group_list = []
    get_characters_in_group(fields[2]["factor_group_xp"], factor_group_list, test_data[2]["factor_group"])
    assert locator_by_xp(fields[5]["iceman_xp"]).text in factor_group_list


def test_tc04_hellfire_group():
    hellfire_group_list = []
    get_characters_in_group(fields[3]["hellfire_group_xp"], hellfire_group_list, test_data[3]["hellfire_group"])
    assert locator_by_xp(fields[5]["iceman_xp"]).text not in hellfire_group_list


# # másik megközelítés
# ### collect test_data
# character_elements = driver.find_elements_by_xpath('//ul[@class="characters"]/li')
#
# with open("character.txt", "w") as chfile:
#     for character in character_elements:
#         chfile.write(character.get_attribute("id"))
#         chfile.write(",")
#         chfile.write(character.get_attribute("data-teams").replace(" ", ","))
#         chfile.write("\n")
#
#
# ### prepare test data
# characters = []
# with open("character.txt", "r") as chtest_data:
#     for row in chtest_data.readlines():
#         row = row.replace("\n", "")
#         characters.append(row.split(","))
#
# # pprint(characters)
#
#
# # TestCase
# def test_tc00():
#     def get_character_data(id):
#         for character in characters:
#             if character[0] == id:
#                 return character
#
#     for character_element in character_elements:
#         id = character_element.get_attribute("id")
#         teams = character_element.get_attribute("data-teams").split(" ")
#         test_data = get_character_data(id)
#         for team in test_data[1:]:
#             assert team in teams
