"""
1. get the latest version of chrome webdriver
2. download chrome webdriver and save it to a file in the current directory
"""

from matplotlib.pyplot import get
import requests
import zipfile
import os
import shutil

def get_chrome_driver():
    """
    get the latest version of chrome webdriver
    """
    url = "https://chromedriver.storage.googleapis.com/LATEST_RELEASE"
    response = requests.get(url)
    version = response.text
    return version

def download_chrome_driver(version):
    """
    download chrome webdriver and save it to a file in the current directory
    """
    url = "https://chromedriver.storage.googleapis.com/{}/chromedriver_win32.zip".format(version)
    response = requests.get(url)
    with open("chromedriver_win32.zip", "wb") as f:
        f.write(response.content)

def unzip_chrome_driver():
    """
    unzip the downloaded file
    """
    with zipfile.ZipFile("chromedriver_win32.zip", "r") as zip_ref:
        zip_ref.extractall(".")

def move_chrome_driver():
    """
    move the unzipped file to the current directory
    """
    shutil.move("chromedriver.exe", ".")


get_chrome_driver()
download_chrome_driver(get_chrome_driver())
unzip_chrome_driver()
