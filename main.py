from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time

from datetime import datetime, date

import sqlite3

driver = webdriver.Firefox()
#doesnt do shit to implicit wait, nice meme
#driver.implicitly_wait(30)#secs
driver.get("https://nitrogensports.eu/")

USERNAME = "3Dankateers"
PASSWORD = "0m3g4lul"

conn = sqlite3.connect('data/Betting.sqlite')
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS BetInfo (Team1, Team2, BTC1, BTC2, MLNum1, MLNum2, mapNumber,TournamentDate, datePulled);")
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


#assuming this is how many data lines there are per row (teams + bets etc)
offset = 6
#Each line corresponds to a certain piece of data
dateLine = 1
team1Line = 2
BTC1Line = 3
Odds1Line = 4
team2Line = 5
BTC2Line = 6
Odds2Line = 7






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



		#WEW LADS
		#GL reading this bois
		if(len(lines)>=7):
			TournamentDate = datetime.strptime(lines[dateLine], '%A, %B %d, %Y %I:%M%p')

			for skip in range(((len(lines)-2)/6)):
				print "HERE"
				print ((len(lines)-2)/6)
				#Temp Variable
				tempo = lines[team1Line+skip*offset].split('(')
				Team1 = tempo[0]

				try:
					mapNumber = lines[team1Line+skip*offset][lines[team1Line+skip*offset].index("(") + 5:lines[team1Line+skip*offset].rindex(")")]
				except:
					mapNumber = -1#-1 if its a bet on the match

				tempo = lines[team2Line+skip*offset].split('(')
				Team2 = tempo[0]
				BTC1 = lines[BTC1Line+skip*offset][:-4]
				BTC2 = lines[BTC2Line+skip*offset][:-4]
				#MLNum1 = lines[4][10:-1]
				#MLNum2 = lines[7][10:-1]
				
				try:
					MLNum1 = lines[Odds1Line+skip*offset][lines[Odds1Line+skip*offset].index("(") + 1:lines[Odds1Line+skip*offset].rindex(")")]
					MLNum2 = lines[Odds2Line+skip*offset][lines[Odds2Line+skip*offset].index("(") + 1:lines[Odds2Line+skip*offset].rindex(")")]
				except:
					#IDK why but sometimes the numbers in brackets arent on the website, not even selinium's fault because I cant see them either
					MLNum1 = "Error"
					MLNum2 = "Error"

				PulledTime = datetime.now()

				c.execute("INSERT INTO BetInfo VALUES (?,?,?,?,?,?,?,?,datetime('now','localtime'));", (Team1, Team2, BTC1, BTC2, MLNum1, MLNum2, mapNumber,TournamentDate))
				conn.commit()
