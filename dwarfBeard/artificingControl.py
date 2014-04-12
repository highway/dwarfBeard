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
import time
from random import randint

import dwarfBeard
from dwarfBeard.db import DBConnection


#this function will return a array of tasks info in order of priority
def getTaskPriorityArray(characterName):

	#make connection to db
	mydb = DBConnection(dwarfBeard.DB_FILE)
	
	#query string
	query = "SELECT * FROM tasks WHERE characterName=?"
	
	#create an array with the task info from the db
	taskArray = mydb.action(query, (characterName,)).fetchall()
	
	return taskArray
		

def startNewArtificingTasks(browser, characterName,  taskPriorityArray):
	
	#this task should begin a new task and then return True if it succeeded
	time.sleep(4)
	
	#start with the first task
	taskPrioritIndex = 0
	
	###########################################
	#wait for the page to load
	reissueCount = 0
	while browser.is_element_not_present_by_css('div.task-list-entry.common') and browser.is_element_not_present_by_css('DIV.task-list-entry.rare') and browser.is_text_not_present('No matching records found'):
		x = randint(6,10)
		#go to professions
		print '  attempting to navigate to profession task list'
		if taskPriorityArray[taskPrioritIndex]['taskProfession'] == 'Platesmithing':
			browser.visit('http://gateway.playneverwinter.com/#char(' + characterName + '@' + dwarfBeard.NW_ACCOUNT_NAME + ')/professions-tasks/' + 'Armorsmithing_Heavy')
		elif taskPriorityArray[taskPrioritIndex]['taskProfession'] == 'Mailsmithing':
			browser.visit('http://gateway.playneverwinter.com/#char(' + characterName + '@' + dwarfBeard.NW_ACCOUNT_NAME + ')/professions-tasks/' + 'Armorsmithing_Med')
		else:
			browser.visit('http://gateway.playneverwinter.com/#char(' + characterName + '@' + dwarfBeard.NW_ACCOUNT_NAME + ')/professions-tasks/' + taskPriorityArray[taskPrioritIndex]['taskProfession'])
		reissueCount += 1
		if reissueCount > 4:
			browser.reload()
			x = 20
			reissueCount = 0
			print '  trying browser reload and sleeping for 20s'
		time.sleep(x)
	
	print '  begining search for the task'
	#here we search through the task list for what we want
	#when this is finished we will be on the first task we have found in the priority list
	lookingForTask = True
	while lookingForTask and (taskPrioritIndex <= len(taskPriorityArray)-1):
		
		#if we are not in the correct profession then we need to navigate to it first
		###########################################
		#wait for the page to load
		reissueCount = 0
		while (browser.is_element_not_present_by_css('div.task-list-entry.common') and browser.is_element_not_present_by_css('DIV.task-list-entry.rare') and browser.is_text_not_present('No matching records found')) or not ((taskPriorityArray[taskPrioritIndex]['taskProfession'] in browser.url) or (taskPriorityArray[taskPrioritIndex]['taskProfession'] == 'Platesmithing' and 'Armorsmithing_Heavy' in browser.url) or (taskPriorityArray[taskPrioritIndex]['taskProfession'] == 'Mailsmithing' and 'Armorsmithing_Med' in browser.url) ):
			x = randint(6,10)
			#go to professions
			print '  attempting to navigate to', taskPriorityArray[taskPrioritIndex]['taskProfession']
			if taskPriorityArray[taskPrioritIndex]['taskProfession'] == 'Platesmithing':
				browser.visit('http://gateway.playneverwinter.com/#char(' + characterName + '@' + dwarfBeard.NW_ACCOUNT_NAME + ')/professions-tasks/' + 'Armorsmithing_Heavy')
			elif taskPriorityArray[taskPrioritIndex]['taskProfession'] == 'Mailsmithing':
				browser.visit('http://gateway.playneverwinter.com/#char(' + characterName + '@' + dwarfBeard.NW_ACCOUNT_NAME + ')/professions-tasks/' + 'Armorsmithing_Med')
			else:
				browser.visit('http://gateway.playneverwinter.com/#char(' + characterName + '@' + dwarfBeard.NW_ACCOUNT_NAME + ')/professions-tasks/' + taskPriorityArray[taskPrioritIndex]['taskProfession'])
			reissueCount += 1
			if reissueCount > 4:
				browser.reload()
				x = 20
				reissueCount = 0
				print '  trying browser reload and sleeping for 20s'
			time.sleep(x)
				
		#this will input into the filter box
		filterInput = browser.find_by_css('#tasklist_filter > label:nth-child(1) > input:nth-child(1)')
		filterInput.fill(taskPriorityArray[taskPrioritIndex]['taskName'])
		time.sleep(2)
	
		#collect a list of tasks
		listOfTasks = browser.find_by_css('div.task-list-entry.common')
		#collect any rare task available
		listOfRareTasks = browser.find_by_css('DIV.task-list-entry.rare')
		
		#look through the tasks for the one you want
		for idx, eachTask in enumerate(listOfTasks):
		
			if taskPriorityArray[taskPrioritIndex]['taskName'] and taskPriorityArray[taskPrioritIndex]['taskLevel'] in browser.find_by_css('div.task-list-entry.common')[idx].text:
				if not ' red' in browser.find_by_css('div.task-list-entry.common')[idx].html:
					print '  found the task', taskPriorityArray[taskPrioritIndex]['taskName']
					lookingForTask = False
					break
				else:
					print '  the task was found but requirments not met'
					break
					
		#if the task want found above the we can check for rare tasks
		if lookingForTask:
			for idx, eachTask in enumerate(listOfRareTasks):
				if taskPriorityArray[taskPrioritIndex]['taskName'] and taskPriorityArray[taskPrioritIndex]['taskLevel'] in browser.find_by_css('DIV.task-list-entry.rare')[idx].text:
					if not ' red' in browser.find_by_css('DIV.task-list-entry.rare')[idx].html:
						print '  found the task', taskPriorityArray[taskPrioritIndex]['taskName']
						lookingForTask = False
						break
					else:
						print '  the task was found but requirments not met'
						break
		
		#if we didn't find the task
		#increment the taskPrioritIndex to search for the next in priority
		if lookingForTask:
			print "  didn't find", taskPriorityArray[taskPrioritIndex]['taskName'], "as an available task"
			taskPrioritIndex += 1
			
		
	#if a task was matched in the priority list then we can start it
	#if the priority index has exceeded the array size then none was found
	if taskPrioritIndex <= len(taskPriorityArray)-1:
		#collect a list of tasks again to make sure they are current
		listOfTasks = browser.find_by_css('div.task-list-entry.common')
		#collect any rare task available
		listOfRareTasks = browser.find_by_css('DIV.task-list-entry.rare')
		
		#look through the task for the one you want
		for idx, eachTask in enumerate(listOfTasks):
			if taskPriorityArray[taskPrioritIndex]['taskName'] and taskPriorityArray[taskPrioritIndex]['taskLevel'] in browser.find_by_css('div.task-list-entry.common')[idx].text:
				#we found the right task but we need to check of all the requirements have been met
				print '  checking if requirments have been met'
				if not ' red' in browser.find_by_css('div.task-list-entry.common')[idx].html:
					#now we start the task
					###########################################
					#wait for the page to load
					while browser.is_element_not_present_by_css("DIV.input-field.button.epic"):
						listOfTasks[idx].find_by_css('div.input-field.button.light.with-arrow').find_by_css('button').click()
						x = randint(2,5)
						print '  trying to click select task, waiting', x, 's'
						time.sleep(x)
						
						
					#start the task
					while browser.is_element_not_present_by_css("DIV.input-field.button.epic"):
						x = randint(2,5)
						print '  waiting for task start button, waiting', x, 's'
						time.sleep(x)
						
					browser.find_by_css('DIV.input-field.button.epic').find_by_css('button').click()
						
					#signal that a task was started
					print '  started task'
					
					return True
					
		#now we'll do the same thing for rare tasks
		for idx, eachTask in enumerate(listOfRareTasks):
			if taskPriorityArray[taskPrioritIndex]['taskName'] and taskPriorityArray[taskPrioritIndex]['taskLevel'] in browser.find_by_css('DIV.task-list-entry.rare')[idx].text:
				#we found the right task but we need to check of all the requirements have been met
				print '  checking if rare task requirments have been met'
				if not ' red' in browser.find_by_css('DIV.task-list-entry.rare')[idx].html:
					#now we start the task
					###########################################
					#wait for the page to load
					while browser.is_element_not_present_by_css("DIV.input-field.button.epic"):
						listOfRareTasks[idx].find_by_css('div.input-field.button.light.with-arrow').find_by_css('button').click()
						x = randint(2,5)
						print '  trying to click select task, waiting', x, 's'
						time.sleep(x)
						
						
					#start the task
					while browser.is_element_not_present_by_css("DIV.input-field.button.epic"):
						x = randint(2,5)
						print '  waiting for task start button, waiting', x, 's'
						time.sleep(x)
						
					browser.find_by_css('DIV.input-field.button.epic').find_by_css('button').click()
						
					#signal that a task was started
					print '  started rare task'
					
					return True
	
	#if this point is reached then no tasks were started
	return False
	

	







