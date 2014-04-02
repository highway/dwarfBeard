#
# This file is part of dwarfBeard.
#
# dwarfBeard is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# dwarfBeard is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# See <http://www.gnu.org/licenses/> for license information.


from splinter import Browser
from random import randint
import time

import dwarfBeard
from dwarfBeard import artificingControl

#randint(2,9) to generate rnd num between 2-9
#time.sleep(5) # delays for 5 seconds


#this function will search for and collect and completed tasks
def checkForRewards(browser):
	
	###########################################
	#wait for the page to load
	while browser.is_text_not_present("Available Profession Slots"):
		x = randint(2,10)
		print '  waiting for overview to load', x, 's'
		time.sleep(x)

	#get a list of the buttons to check for finished tasks
	print '  searching for completed tasks'
	buttonList = browser.find_by_css('DIV.input-field.button.epic')

	#create a list for the button txt
	buttonTxtList = []
	
	#pull out all of the button text
	for idx, eachButton in enumerate(buttonList):
		buttonTxtList.append(browser.find_by_css('DIV.input-field.button.epic')[idx].text)
		print '  ', buttonTxtList[idx]

	#here is a test for button text
	for idx, eachButton in enumerate(buttonTxtList):
		if eachButton == 'Collect Result':
			print '  completed task found'
			x = randint(2,6)
			print '  pausing before collection', x, 's'
			time.sleep(x)
			#click the button by finding it on the page
			button = browser.find_by_css('DIV.input-field.button.epic')[idx]
			button.click()
			#wait for the collection page to load
			while browser.is_element_not_present_by_css('.professions-rewards-modal > div:nth-child(3)'):
				x = randint(2,6)
				print '  waiting for collection screen to load', x, 's'
				time.sleep(x)
			#collect the reward
			browser.find_by_css('.professions-rewards-modal > div:nth-child(3)').click()
			print '  reward collected'
			#sleep for 5 to allow the reward button to clear
			time.sleep(5)

	return
	

	
#this function will log on to the site, select the char, and goto professions
#this function creates a browser instance and returns it
def openToProfessions(browser):
	###########################################
	#wait for the page to load
	while browser.is_text_not_present("Professions") and browser.is_text_present("Loading Character"):
		x = randint(2,10)
		print '  waiting to select professions', x, 's'
		time.sleep(x)

	#go to professions
	browser.find_by_css('a.nav-button.mainNav.professions.nav-professions').first.click()

	
	
	return 



	
def startNewTasksManager(browser):
	
	#here we need to look for available task slots then call to start a new task in the order of priority
	###########################################
	#wait for the page to load
	while browser.is_text_not_present("Available Profession Slots"):
		x = randint(2,10)
		print '  waiting for overview to load', x, 's'
		time.sleep(x)

	#get a list of the buttons to check for finished tasks
	print '  searching for empty task slots'
	buttonList = browser.find_by_css('DIV.input-field.button.epic')

	#create a list for the button txt
	buttonTxtList = []
	
	#pull out all of the button text before the links go stale
	for idx, eachButton in enumerate(buttonList):
		buttonTxtList.append(browser.find_by_css('DIV.input-field.button.epic')[idx].text)
		print '  ', buttonTxtList[idx]

	#here is a test for button text
	for idx, eachButton in enumerate(buttonTxtList):
		if eachButton == 'Choose Task':
			print '  empty task found'
			print '  attempting to start new artificing task'
			if artificingControl.startNewArtificingTasks(browser):
				print '  new artificing task started'
	
	return
	
	
	
def selectChar(browser, characterName):
	x = randint(2,7)
	print '  a quick pause to let the page load ', x, 's'
	time.sleep(x)
	
	#get the url of the current page
	curUrl = browser.url
	
	###########################################
	#wait for the page to load
	#look for the char name
	while browser.is_text_not_present(characterName):
		x = randint(2,10)
		print '  waiting for character page to load', x, 's'
		time.sleep(x)
	
	#select a character
	#now we select the character by url
	browser.visit('http://gateway.playneverwinter.com/#char(' + characterName + '@' + dwarfBeard.NW_ACCOUNT_NAME + ')/')
	
	return
	
	
def openToOverview(browser):
	
	#look the overview button
	while browser.is_element_not_present_by_css('A.tab.subNav.overview.professions-overview'):
		x = randint(5,10)
		print '  cannot find overview tab', x, 's'
		time.sleep(x)
		
	#wait for the page to load
	while browser.is_text_not_present("Available Profession Slots"):
		x = randint(2,10)
		#go to professions
		browser.find_by_css('A.tab.subNav.overview.professions-overview').first.click()
		print '  waiting for overview to load', x, 's'
		time.sleep(x)

	
	return 

#this function will return the best amount of time to wait
#before logging back in to manage tasks again
def decideLogoutTime(browser):
	
	openToOverview(browser)
	
	#get a list of the current timers
	listOfTimers = browser.find_by_css('div.bar-text')
	
	#pull out the timer text
	listOfTimerText = []
	for eachTimer in listOfTimers:
		listOfTimerText.append(eachTimer.text)
		
	#create a list of the split text
	splitTimerTextList = []
	for eachText in listOfTimerText:
		splitTimerTextList.append(eachText.split())
	
	#create a list of the timer values in seconds
	timerStatusInSec = []
	
	#go through the timer list and convert each one into seconds
	for idx, eachArray in enumerate(splitTimerTextList):
		#append a new item to the timerStatusInSec list
		timerStatusInSec.append(0)
		
		#now we loop through each of the timer texts
		for eachText in eachArray:
			#here we convert the value to seconds and add it to the 
			#timer status list
			if 'h' in eachText:
				timerStatusInSec[idx] = timerStatusInSec[idx] + int(eachText[0:len(eachText)-1]) *60 *60
			
			elif 'm' in eachText:
				timerStatusInSec[idx] = timerStatusInSec[idx] + int(eachText[0:len(eachText)-1]) *60
				
			elif 's' in eachText:
				timerStatusInSec[idx] = timerStatusInSec[idx] + int(eachText[0:len(eachText)-1])
				
	#now we decide what is the shortest amount of time to wait before logging on again
	#init the wait time to a really long time
	waitTime = 1000000
	
	#look through the timer status list for the shortest time
	for eachTimer in timerStatusInSec:
		if eachTimer < waitTime:
			waitTime = eachTimer
			
	#if any of the timers are within 10.5min of the shortest then lets wait for those to complete
	for eachTimer in timerStatusInSec:
		if eachTimer < waitTime+630 and not eachTimer == waitTime:
			waitTime = eachTimer
	
	#add some random time to the time out
	waitTime = waitTime + randint(30,300)
	
	#return the time to wait
	return waitTime

def runTaskManagment(browser, characterName):
	
	#selectCharacter
	print 'running selectChar'
	selectChar(browser, characterName)
	
	#open to professions
	print 'running openToProfessions'
	openToProfessions(browser)
	
	#check for completed tasks
	print 'running checkForRewards'
	checkForRewards(browser)
	
	#start new tasks if possible
	print 'running startNewTasksManager'
	startNewTasksManager(browser)
	
	return
	