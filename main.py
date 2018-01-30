from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import psycopg2

from datetime import datetime, date

options = Options()
options.add_argument('--headless')
driver = webdriver.Chrome(executable_path='chromedriver', chrome_options=options)

#doesnt do shit to implicit wait, nice meme
#driver.implicitly_wait(30)#secs
driver.get("https://nitrogensports.eu/")

USERNAME = "3Dankateers"
PASSWORD = "0m3g4lul"

conn = psycopg2.connect("dbname='league' user='postgres' host='localhost' password='Postgres1423'")
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS Betting (team1 TEXT, team2 TEXT, btc1 REAL, btc REAL, moneyLine1 REAL, moneyLine2 REAL, typeOfBet TEXT,tournamentDate TIMESTAMP, datePulled TIMESTAMP);")
conn.commit()

#Hardcode tournament names for now
tournamentNames = []
tournamentNames.append("league-of-legends-champions-korea")
tournamentNames.append("league-of-legends-china-lpl")
tournamentNames.append("league-of-legends-elite-challenger-series")
tournamentNames.append("league-of-legends-garuda-series")
tournamentNames.append("league-of-legends-latin-america-north-cup")
tournamentNames.append("league-of-legends-lcs-europe")
tournamentNames.append("league-of-legends-lcs-north-america")
tournamentNames.append("league-of-legends-lol-master-series")
tournamentNames.append("league-of-legends-oceanic-pro-league")
tournamentNames.append("league-of-legends-thailand-pro-league")
tournamentNames.append("league-of-legends-turkish-champions-league")


####Delay in updating bets (in seconds)
REFRESH_DELAY = 600

#Ghetto mode, set false when you want it to stop
stillRunning = True

'''
team1, team2 = ""
btc1, btc2, moneyLine1, moneyLine2 = 0
tournamentDate, PulledTime = None
'''
'''
Team names 1 and 2
BTC are the BTC values to the right, idk what they are there for
MLNum is the x.xxx format ML odds
MLStd is (+/-)xxx format ML odds
tournamentDate is when the tournament is set to happen
PulledTime is when data was pulled using this program
'''
team1 = ""
team2 = ""
btc1 = 0
btc2 = 0
moneyLine1 = 0
moneyLine2 = 0
typeOfBet = 0


#assuming this is how many data lines there are per row (teams + bets etc)
offset = 6
#Each line corresponds to a certain piece of data
dateLine = 1
team1Line = 2
btc1Line = 3
odds1Line = 4
team2Line = 5
btc2Line = 6
odds2Line = 7






time.sleep(10)
loginButton = driver.find_element_by_id("modal-welcome-login-button").click()

time.sleep(2)
username = driver.find_element_by_id("modal-account-login-username-textbox").send_keys(USERNAME)
time.sleep(2)
password = driver.find_element_by_id("modal-account-login-password-textbox").send_keys(PASSWORD)
time.sleep(2)
submitLogin = driver.find_element_by_id("modal-account-login-button").click()

while (stillRunning):
	time.sleep(REFRESH_DELAY)
	for rows in range (len(tournamentNames)):
		time.sleep(2)
		driver.get("https://nitrogensports.eu/sport/esports/"+str(tournamentNames[rows]))
		time.sleep(2)
		events = driver.find_elements_by_class_name('event')
		time.sleep(2)
		for e in range (len(events)):
			temp = events[e].text

			lines = temp.splitlines()
			#for i in range(len(lines)):



			#WEW LADS
			#GL reading this bois
			if(len(lines)>=7):
				tournamentDate = datetime.strptime(lines[dateLine], '%A, %B %d, %Y %I:%M%p')

				for skip in range(((len(lines)-2)/6)):
					#Temp Variable
					tempo = lines[team1Line+skip*offset].split('(')
					team1 = tempo[0]

					try:
						array = lines[team1Line+skip*offset].split(')')
						#print "Array: " + str(array)
						answers = ""

						for k in range(len(array)):
							if '(' in array[k]:
								kek = array[k].split('(')[1]
								#print "Kek: " + kek
								answers += kek
								answers += ","

						if (answers == ""):
							answers = "Match,"
						typeOfBet = answers

					except:
						typeOfBet = -1#-1 if something went wong

					tempo = lines[team2Line+skip*offset].split('(')
					team2 = tempo[0]
					btc1 = lines[btc1Line+skip*offset][:-4]
					btc2 = lines[btc2Line+skip*offset][:-4]
					#moneyLine1 = lines[4][10:-1]
					#moneyLine2 = lines[7][10:-1]
					
					try:
						moneyLine1 = lines[odds1Line+skip*offset][lines[odds1Line+skip*offset].index("(") + 1:lines[odds1Line+skip*offset].rindex(")")]
						moneyLine2 = lines[odds2Line+skip*offset][lines[odds2Line+skip*offset].index("(") + 1:lines[odds2Line+skip*offset].rindex(")")]
					except:
						#IDK why but sometimes the numbers in brackets arent on the website, not even selinium's fault because I cant see them either
						continue
						moneyLine1 = "Error"
						moneyLine2 = "Error"
						#This makes sure u always get at least one of the ML odds, not sure if I should just put it in another column
						#moneyLine1 = lines[odds1Line+skip*offset][3:]
						#moneyLine2 = lines[odds2Line+skip*offset][3:]

					c.execute("INSERT INTO Betting VALUES (%s,%s,%s,%s,%s,%s,%s,%s,now());", (team1, team2, btc1, btc2, moneyLine1, moneyLine2, typeOfBet,tournamentDate,))
					conn.commit()

c.close()