"""
1. make a GET request to https://yaktribe.games/underhive/campaign/2021_grimdark_dick_%26_fart_joke_summit.10329/
2. take a screenshot of the page
3. Convert the screnshot to RGB
4. save the screenshot to a JPEG file
5. scroll halfway down the length of the page
6. take a second screenshot
7. get the text content of any div that has 'card' in the class name
8. format the text content and print to the terminal output as cards
"""

from posixpath import split
from parso import split_lines
import requests
from PIL import Image
from io import BytesIO
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import dotenv
import os
import time
import json
dotenv.load_dotenv()


# import Slack SDK and init Slack client
from slack_sdk import WebClient
slack_client = WebClient(token=os.getenv('SLACK_USER_TOKEN'))



def print_in_box(string):
    '''
    Prints a string in a box.
    '''
    print('+' + '-' * (len(string) + 2) + '+')
    print('|' + ' ' * (len(string) + 2) + '|')
    print('| ' + string + ' |')
    print('|' + ' ' * (len(string) + 2) + '|')
    print('+' + '-' * (len(string) + 2) + '+')

def print_in_box_width(string, width):
    '''
    Prints a string in a box with a given width
    '''

    print('+' + '-' * (width + 2) + '+')
    print('|' + ' ' * (width + 2) + '|')
    print('| ' + string + ' |')
    print('|' + ' ' * (width + 2) + '|')
    print('+' + '-' * (width + 2) + '+')


# 1. Target url
url = 'https://yaktribe.games/underhive/campaign/2021_grimdark_dick_%26_fart_joke_summit.10329/'


# 2. take a screenshot of the page
chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)
driver.get(url)
driver.save_screenshot('screenshot.png')

# 3. Convert the screnshot to RGB
im = Image.open('screenshot.png')
rgb_im = im.convert('RGB')

# 4. save the screenshot to a JPEG file
rgb_im.save('screenshot.jpg')

# 5. scroll halfway down the length of the page
actions = ActionChains(driver)
actions.send_keys(Keys.PAGE_DOWN)
actions.perform()

# 6. take a second screenshot
driver.save_screenshot('screenshot2.png')

# 7. get the text content of any div that has 'card' in the class name
# cards = driver.find_elements_by_class_name('card')
cards = driver.find_elements(by=By.CLASS_NAME,value='card')

# 8. format the text content and print to the terminal output as cards
pattern = re.compile(r'\dmth')

content= []
for card in cards:
    format_text = re.sub(pattern, f'\n{"="*15}\n', card.text)
    print(format_text)
    content.append(format_text)


def divide_list(list_of_strings):
    list_of_strings_1 = list_of_strings[0:len(list_of_strings)//4]
    list_of_strings_2 = list_of_strings[len(list_of_strings)//4:len(list_of_strings)//2]
    list_of_strings_3 = list_of_strings[len(list_of_strings)//2:3*len(list_of_strings)//4]
    list_of_strings_4 = list_of_strings[3*len(list_of_strings)//4:len(list_of_strings)]
    return [list_of_strings_1, list_of_strings_2, list_of_strings_3, list_of_strings_4]


def format_block(x):
    blocks = [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": "GrimDank Battle Report",
                "emoji": True,
            },
        },
        {
            "type": "divider",
        },
        {
            "type": "section",
                "text": {
                "type": "mrkdwn",
                "text": f"{x}",
            },
        },
    ]
    return blocks


list_content = divide_list(content)
list_of_strings = ["".join(x) for x in list_content]


for x in list_of_strings:

    if len(x) > 3000:
        split_lines = x.splitlines()
        split_content1 = split_lines[0:len(split_lines)//2]
        split_content2 = split_lines[len(split_lines)//2:len(split_lines)]
        split_content1_formatted = format_block(split_content1)
        split_content2_formatted = format_block(split_content2)

        slack_client.chat_postMessage(channel='C02HXJ4EGSC', blocks=split_content1_formatted)
        time.sleep(2)
        slack_client.chat_postMessage(channel='C02HXJ4EGSC', blocks=split_content2_formatted)
        time.sleep(2)
    else:
        slack_client.chat_postMessage(channel='C02HXJ4EGSC', blocks=format_block(x))
        time.sleep(2)



    # block_text = json.dumps(blocks)
    # slack_client.chat_postMessage(channel='C02HXJ4EGSC', blocks=blocks, text=x)
    

