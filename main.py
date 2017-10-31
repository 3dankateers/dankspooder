from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time

driver = webdriver.Firefox()
#doesnt do shit to implicit wait, nice meme
#driver.implicitly_wait(30)#secs
driver.get("https://nitrogensports.eu/")

USERNAME = "3Dankateers"
PASSWORD = ""

time.sleep(10)
loginButton = driver.find_element_by_id("modal-welcome-login-button").click()

time.sleep(2)
username = driver.find_element_by_id("modal-account-login-username-textbox").send_keys(USERNAME)
time.sleep(2)
password = driver.find_element_by_id("modal-account-login-password-textbox").send_keys(PASSWORD)
time.sleep(2)
submitLogin = driver.find_element_by_id("modal-account-login-button").click()
time.sleep(2)
esportsButton = driver.find_element_by_css_selector('li.menu-item-sport:nth-child(19)').click()
time.sleep(2)
#leagueTourny = driver.find_element_by_xpath("//div[contains(text(),'League')]").click()
#leagueTourny = driver.find_element_by_xpath("//a[contains(@href,'League')]").click()
#leagueTourny = driver.find_element_by_partial_link_text("League").click()
leagueTourny = driver.find_element_by_css_selector('li.menu-item-sport:nth-child(19) > ul:nth-child(2) > li:nth-child(27) > a:nth-child(1)').click()
time.sleep(2)
nameOfTourny = driver.find_element_by_css_selector('#page-find-games > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > h3:nth-child(1)').text
print nameOfTourny
