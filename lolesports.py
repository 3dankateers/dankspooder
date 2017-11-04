from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time

from datetime import datetime, date

import sqlite3

driver = webdriver.Firefox()

HTTP = "http://www.lolesports.com/"
REGION = "en_US/"



driver.get(HTTP + REGION)