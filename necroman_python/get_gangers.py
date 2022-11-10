"""
1. make a GET request to https://yaktribe.games/underhive/gang/_extra_spicy_chunky_salsa_boys.222836/
2. Get the text contents at the selector of #gang-tab-details > tr:nth-child(1) > td
3. print the text contents
"""

import re
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from PIL import Image
base_url = "https://yaktribe.games/"


def get_gang_name(gang_url):
    """
    Get the gang name from the gang url
    :param gang_url:
    :return:
    """
    response = requests.get(gang_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    gang_name = soup.select_one('#gang-tab-details > tr:nth-child(1) > td').text
    return gang_name


def get_gang_urls(gang_list_url):
    """
    Get the gang urls from the gang list url
    :param gang_list_url:
    :return:
    """
    response = requests.get(gang_list_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    gang_urls = [a['href'] for a in soup.select('a[href*=gang]')]
    return gang_urls

req = get_gang_name('https://yaktribe.games/underhive/gang/_extra_spicy_chunky_salsa_boys.222836/')
print(req)

def get_campaign_urls(gang_url):
    """
    Get the campaign urls from the gang url
    :param gang_url:
    :return:
    """
    response = requests.get(gang_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    campaign_slug = soup.select_one('#gang-tab-details > tr:nth-child(4) > td > a').get('href')
    campaign_url = f"{base_url}{campaign_slug}"
    print(campaign_url)
    return campaign_url

def campaign_data(campaign_url):
    # 1. make a GET request to https://yaktribe.games/underhive/campaign/2021_grimdark_dick_%26_fart_joke_summit.10329/
    response = requests.get(f'{campaign_url}')

    # 2. take a screenshot of the page
    driver = webdriver.Chrome()
    driver.get('https://yaktribe.games/underhive/campaign/2021_grimdark_dick_%26_fart_joke_summit.10329/')
    driver.save_screenshot('screenshot.png')

    # 3. save the screenshot to a JPEG file
    im = Image.open('screenshot.png')
    rgb_im = im.convert('RGB')
    rgb_im.save('screenshot.jpg')

    # 4. get the text content of any div that has 'card' in the class name
    soup = BeautifulSoup(response.text, 'html.parser')
    cards = soup.find_all('div', class_='card')
    for card in cards:
        print(card.text)


camp_url = get_campaign_urls('https://yaktribe.games/underhive/gang/_extra_spicy_chunky_salsa_boys.222836/')
campaign_data(camp_url)