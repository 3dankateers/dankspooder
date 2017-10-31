from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time

import datetime

import sqlite3

driver = webdriver.Firefox()
#doesnt do shit to implicit wait, nice meme
#driver.implicitly_wait(30)#secs
driver.get("https://nitrogensports.eu/")

USERNAME = "3Dankateers"
PASSWORD = "0m3g4lul"

conn = sqlite3.connect('data/Betting.sqlite')
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS BetInfo1 (Team1, Team2, BTC1, BTC2, MLNum1, MLNum2, TournamentDate, PulledTime, mapNumber);")
conn.commit()

#Hardcode tournament names for now
tournamentNames = []
tournamentNames.append("league-of-legends-world-championship")


'''
Team1, Team2 = ""
BTC1, BTC2, MLStd1, MLStd2 = 0
TournamentDate, PulledTime = None
'''
'''
Team names 1 and 2
BTC are the BTC values to the right, idk what they are there for
MLNum is the x.xxx format ML odds
MLStd is (+/-)xxx format ML odds
TournamentDate is when the tournament is set to happen
PulledTime is when data was pulled using this program
'''
Team1 = ""
Team2 = ""
BTC1 = 0
BTC2 = 0
MLStd1 = 0
MLStd2 = 0
mapNumber = 0



time.sleep(10)
loginButton = driver.find_element_by_id("modal-welcome-login-button").click()

time.sleep(2)
username = driver.find_element_by_id("modal-account-login-username-textbox").send_keys(USERNAME)
time.sleep(2)
password = driver.find_element_by_id("modal-account-login-password-textbox").send_keys(PASSWORD)
time.sleep(2)
submitLogin = driver.find_element_by_id("modal-account-login-button").click()
time.sleep(2)

for rows in range (len(tournamentNames)):
	driver.get("https://nitrogensports.eu/sport/esports/"+str(tournamentNames[rows]))
	time.sleep(2)
	events = driver.find_elements_by_class_name('event')
	time.sleep(2)
	for e in range (len(events)):
		print "Events's e: " + str(e)
		temp = events[e].text
		print temp

		lines = temp.splitlines()
		for i in range(len(lines)):
			print "Line: " + str(i) + " " + str(lines[i])

		#Temp var
		if(len(lines)>=7):
			tempo = lines[2].split('(')

			TournamentDate = lines[1]
			Team1 = tempo[0]
			mapNumber = tempo[1]
			tempo = lines[5].split('(')
			Team2 = tempo[0]
			BTC1 = lines[3][:-4]
			BTC2 = lines[6][:-4]
			MLNum1 = lines[4][3:]
			MLNum2 = lines[7][3:]
			now = datetime.datetime.now()
			PulledTime = now.strftime("%Y-%m-%d %H:%M")

			c.execute("INSERT INTO BetInfo1 VALUES (?,?,?,?,?,?,?,?,?);", (Team1, Team2, BTC1, BTC2, MLNum1, MLNum2, TournamentDate, PulledTime, mapNumber))
			conn.commit()
		'''
		###Garbage Detected
		teams = events[e].find_elements_by_class_name('event-participant span6')
		time.sleep(2)
		odds = events[e].find_elements_by_class_name('event-odds span4')
		time.sleep(2)
		for x in range (len(teams)):
			print "Teams x: " + str(x)
			print teams[x].text
		for x in range (len(odds)):
			print "odds x: " + str(x)
			print odds[x].text
		'''


