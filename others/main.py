from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import psycopg2

from datetime import datetime, date

options = Options()
#options.add_argument('--headless')
driver = webdriver.Chrome(executable_path='chromedriver', chrome_options=options)

#options.add_argument('-headless')
#driver = Firefox(executable_path='geckodriver')

WIERD_STRING = "U3BvcnRzYmV0V2Vic2l0ZUNhdGVnb3J5OjU5OTE2YWE1ZmNhYTY4MDAxYzk1ODQyZg=="
USERNAME = "3Dankateers"
PASSWORD = "0m3g4lul"



driver.get("https://sportsbet.io/sports/e-sports/"+str(WIERD_STRING))





conn = psycopg2.connect("dbname='league' user='postgres' host='localhost' password='Postgres1423'")
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS Betting (team1 TEXT, team2 TEXT, moneyLine1 REAL, moneyLine2 REAL, typeOfBet TEXT, datePulled TIMESTAMP);")
conn.commit()

####Delay in updating bets (in seconds)
REFRESH_DELAY = 600

#Ghetto mode, set false when you want it to stop
stillRunning = True

team1 = ""
team2 = ""
moneyLine1 = 0
moneyLine2 = 0
typeOfBet = 0
tournamentDate = 0

LeagueID = 0
offset = 9 #Offset means every x lines you get the same shit, so team1 is on line a, next team1 is on line a + offset



time.sleep(5)
driver.find_elements_by_class_name("pt-dialog-close-button")[0].click()

time.sleep(10)
events = driver.find_elements_by_class_name('events-container')
for i in range(len(events)):
	if('League' in events[i].text):
		print (i)
		LeagueID = i
		events[i].click()

time.sleep(1)
	
while (stillRunning):

	scanthrough = driver.find_elements_by_class_name('sports-events')
	stringEvents = scanthrough[LeagueID].text.split('\n')
	print(stringEvents)
	time.sleep(1)

	parsing = int(len(stringEvents)/9)



	for i in range(parsing):
		typeOfBet = stringEvents[1+(i*offset)]
		team1 = stringEvents[6+(i*offset)]
		moneyLine1 = stringEvents[7+(i*offset)]
		team2 = stringEvents[8+(i*offset)]
		moneyLine2 = stringEvents[9+(i*offset)]
		print(team1+moneyLine1+team2+moneyLine2+typeOfBet)
		c.execute("INSERT INTO Betting VALUES (%s,%s,%s,%s,%s,now());", (team1, team2, moneyLine1, moneyLine2, typeOfBet,))
		conn.commit()

	#for i in events:
		#print (events[i])


	time.sleep(REFRESH_DELAY)

c.close()
