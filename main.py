from pprint import pprint
import time
from urllib import response
from bs4 import BeautifulSoup
from urllib.parse import unquote
import lxml

from selenium import webdriver
from selenium.webdriver.common.by import By


def open_page():
    url = "https://emoji-captcha.glitch.me"
    global browser
    browser = webdriver.Safari()
    browser.set_page_load_timeout(10)
    browser.get(url)
    time.sleep(5)
    html = browser.page_source

    soup = BeautifulSoup(html, "lxml")
    try:
        paras = soup.findAll("p")
        text = paras[1].text
        goal = text.replace("Please select ", "")
    except Exception as e:
        print("Unable to detect challenge text")

    print(goal)

    emojis = browser.find_elements(By.CLASS_NAME, "emoji")
    for emoji in emojis:
        image = emoji.find_element(By.TAG_NAME, "img")
        svg = image.get_attribute("src")
        svg = unquote(svg)
        svg = svg.split(",")[1]
        print(svg)
        break

    return browser


open_page()
