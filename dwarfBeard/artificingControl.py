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
	
	#make a tuple of the character name
	cName = (characterName,)
	
	#create an array with the task info from the db
	taskArray = mydb.action("SELECT * FROM tasks WHERE characterName=?", cName).fetchall()
	
	return taskArray
		

def startNewArtificingTasks(browser, characterName,  taskPriorityArray):
	
	#this task should begin a new task and then return True if it succeeded
	time.sleep(4)
	
	#start with the first task
	taskPrioritIndex = 0
	
	###########################################
	#wait for the page to load
	while browser.is_element_not_present_by_css('div.task-list-entry.common') and browser.is_text_not_present('No matching records found'):
		x = randint(5,9)
		#go to professions
		print '  attempting to navagate to professions overview'
		browser.visit('http://gateway.playneverwinter.com/#char(' + characterName + '@' + dwarfBeard.NW_ACCOUNT_NAME + ')/professions-tasks/' + taskPriorityArray[taskPrioritIndex]['taskProfession'])
		time.sleep(x)
	
	print '  begining search for the task'
	#here we search through the task list for what we want
	#when this is finished we will be on the first task we have found in the priority list
	lookingForTask = True
	while lookingForTask and (taskPrioritIndex <= len(taskPriorityArray)-1):
		
		#this will input into the filter box
		filterInput = browser.find_by_css('#tasklist_filter > label:nth-child(1) > input:nth-child(1)')
		filterInput.fill(taskPriorityArray[taskPrioritIndex]['taskName'])
		time.sleep(2)
	
		#collect a list of tasks
		listOfTasks = browser.find_by_css('div.task-list-entry.common')
		
		#look through the tasks for the one you want
		for idx, eachTask in enumerate(listOfTasks):
			if taskPriorityArray[taskPrioritIndex]['taskName'] and taskPriorityArray[taskPrioritIndex]['taskLevel'] in browser.find_by_css('div.task-list-entry.common')[idx].text:
				if not ' red' in browser.find_by_css('div.task-list-entry.common')[idx].html:
					print '  found the task'
					lookingForTask = False
					break
				else:
					print '  a task was found but requirments not met'
					break
		
		#if we didn't find the task
		#increment the taskPrioritIndex to search for the next in priority
		if lookingForTask:
			print " didn't find first priority, looking for the next"
			taskPrioritIndex += 1
			
		
	#if a task was matched in the priority list then we can start it
	#if the priority index has exceeded the array size then none was found
	if taskPrioritIndex <= len(taskPriorityArray)-1:
		#collect a list of tasks again to make sure they are current
		listOfTasks = browser.find_by_css('div.task-list-entry.common')
		
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
	
	#if this point is reached then no tasks were started
	return False
	

	







