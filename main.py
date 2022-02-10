import time
from urllib import response
from bs4 import BeautifulSoup
from urllib.parse import unquote
import lxml
import json

from selenium import webdriver
from selenium.webdriver.common.by import By


big_string = ""

with open("./compiled.json", "r") as f:
    big_string = f.read()

f.close()

json_emoji = json.loads(big_string)


def open_page():
    url = "https://emoji-captcha.glitch.me"
    global browser
    #! change this to your own executable path
    browser = webdriver.Edge(
        executable_path="/Users/arijitroy/Projects/bumblebee/msedgedriver"
    )
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

    goal = goal[:-1]

    submit_button = browser.find_element(By.CLASS_NAME, "submit")

    emojis = browser.find_elements(By.CLASS_NAME, "emoji")
    for ctr, emoji in enumerate(emojis):
        image = emoji.find_element(By.TAG_NAME, "img")
        svg = image.get_attribute("src")
        svg = unquote(svg)
        svg = svg.split(",")[1]
        svg = svg.replace("'", '"')

        target = json_emoji[goal]

        if svg == target:
            emoji.click()
            submit_button.click()
            time.sleep(3)
            # browser.close()
            break

    return browser


open_page()
