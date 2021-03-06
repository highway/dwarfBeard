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
from time import strftime
from random import randint
from threading import Timer

import os
import sys
from lib.configobj import ConfigObj
import sqlite3
if sys.version_info < (2, 5):
	sys.exit("Sorry, requires Python 2.5, 2.6 or 2.7.")

try:
	import Cheetah
	if Cheetah.Version[0] != '2':
		raise ValueError
except ValueError:
	sys.exit("Sorry, requires Python module Cheetah 2.1.0 or newer.")
except:
	sys.exit("The Python module Cheetah is required")

import dwarfBeard
from dwarfBeard.webServerInit import initWebServer
from dwarfBeard import browserControl
from dwarfBeard import artificingControl
from dwarfBeard import professionGeneral
from dwarfBeard import general
from dwarfBeard.general import TaskTimer
from dwarfBeard.db import DBConnection


def executeTaskActionList(timer):

	#signal the task is in execution
	dwarfBeard.taskExecRunning = 1
	
	#stop the task timer during execution
	#this is done to prevent a second execution from firing while we are still executing and 
	#the timer will be restarted when this function is finished which will result in a
	#more accurate logout time
	timer.stop()
	
	#get a connection to the db
	mainDB = DBConnection(dwarfBeard.DB_FILE)
	
	#get character names from the db
	cnDict = mainDB.action('SELECT * FROM characterNames')
	
	#put the character names into a list
	characterList = []
	for row in cnDict:
		characterList.append(str(row['characterName']))
	
	#open a browser
	print 'running openAbrowser'
	browser = browserControl.openAbrowser(dwarfBeard.FF_PROFILE_PATH)

	#login
	print 'running loginToSite'
	browserControl.loginToSite(browser, dwarfBeard.NW_USER_NAME, dwarfBeard.NW_PASSWORD)

	#manage the tasks for each character
	for eachCharacter in characterList:
		#run the manager
		professionGeneral.runTaskManagment(browser, eachCharacter)

	#poll ad exchange rates, only one character name is needed
	print 'running logZenExchange'
	general.logZenExchange(browser, characterList[0])
		
	#running decide log out time
	print 'running decideLogoutTime'
	logoutTime = professionGeneral.decideLogoutTime(browser, characterList)

	#running endSession
	print 'running end session'
	browserControl.closeAbrowser(browser)

	#calculate out the h, m, s, for the logout to make a nice message
	h = logoutTime / 3600
	m = (logoutTime % 3600) / 60
	s = (logoutTime % 3600) % 60

	#sleep until next run
	print 'sleeping for', h, 'h', m, 'm', s, 's', ' @', strftime("%Y-%m-%d %H:%M:%S")
	
	#set the timer interval to the logoutTime
	timer.interval = logoutTime
	
	if dwarfBeard.runTasks:
		#start the timer
		timer.start()
	else:
		print 'run tasks disabled. not starting login timer'
	
	#signal the task is finished
	dwarfBeard.taskExecRunning = 0
	
	return 
	

def main():

	#initial settings
	dwarfBeard.MY_FULLNAME = os.path.normpath(os.path.abspath(__file__))
	dwarfBeard.MY_NAME = os.path.basename(dwarfBeard.MY_FULLNAME)
	dwarfBeard.PROG_DIR = os.path.dirname(dwarfBeard.MY_FULLNAME)
	dwarfBeard.DATA_DIR = dwarfBeard.PROG_DIR
	
	#load the config file path if it is not loaded
	if not dwarfBeard.CONFIG_FILE:
		dwarfBeard.CONFIG_FILE = os.path.join(dwarfBeard.DATA_DIR, "config.ini")
		
	#load the path to the db if it is not loaded
	if not dwarfBeard.DB_FILE:
		dwarfBeard.DB_FILE = os.path.join(dwarfBeard.DATA_DIR, "dwarf.db")
	
	# Make sure that we can create the data dir
	if not os.access(dwarfBeard.DATA_DIR, os.F_OK):
		try:
			os.makedirs(dwarfBeard.DATA_DIR, 0744)
		except os.error:
			sys.exit("Unable to create data directory: " + dwarfBeard.DATA_DIR + " Exiting.")
	
	# Make sure we can write to the data dir
	if not os.access(dwarfBeard.DATA_DIR, os.W_OK):
		sys.exit("Data directory: " + dwarfBeard.DATA_DIR + " must be writeable (write permissions). Exiting.")
		
	# Make sure we can write to the config file
	if not os.access(dwarfBeard.CONFIG_FILE, os.W_OK):
		if os.path.isfile(dwarfBeard.CONFIG_FILE):
			sys.exit("Config file: " + dwarfBeard.CONFIG_FILE + " must be writeable (write permissions). Exiting.")
		elif not os.access(os.path.dirname(dwarfBeard.CONFIG_FILE), os.W_OK):
			sys.exit("Config file directory: " + os.path.dirname(dwarfBeard.CONFIG_FILE) + " must be writeable (write permissions). Exiting")
	
	#change the working directory
	os.chdir(dwarfBeard.DATA_DIR)
	
	# Load the config and publish it to the dwarfBeard package
	dwarfBeard.CFG = ConfigObj(dwarfBeard.CONFIG_FILE)
	
	#if the db does not exist create it.
	if not os.path.isfile(dwarfBeard.DB_FILE):
		dbConn = sqlite3.connect(dwarfBeard.DB_FILE)
		dbConn.close()
		
	#init the db if needed
	myDb = DBConnection(dwarfBeard.DB_FILE)
	if not myDb.initTest():
		myDb.createInitialSchema()
	
	# Initialize dwarfBeard and the config
	dwarfBeard.initialize()
	
	# Use this PID for everything
	dwarfBeard.PID = os.getpid()

	#set the log dir
	if dwarfBeard.WEB_LOG:
		log_dir = dwarfBeard.LOG_DIR
	else:
		log_dir = None

	#try to init the web server
	try:
		initWebServer({
					  'port': dwarfBeard.WEB_PORT,
					  'host': dwarfBeard.WEB_HOST,
					  'data_root': os.path.join(dwarfBeard.PROG_DIR, 'webData'),
					  'web_root': dwarfBeard.WEB_ROOT,
					  'log_dir': log_dir,
					  'username': dwarfBeard.WEB_USERNAME,
					  'password': dwarfBeard.WEB_PASSWORD,
					  })
	except IOError:
		dwarfBeard.launchBrowser(dwarfBeard.WEB_PORT)
		print "Unable to start web server, is something else running on port: " + str(dwarfBeard.WEB_PORT)

	# Launch browser if we're supposed to
	if dwarfBeard.LAUNCH_BROWSER:
		dwarfBeard.launchBrowser(dwarfBeard.WEB_PORT)
		
	#create a task timer that executes the task action list at a set interval
	#this is how we will control the time between profession jobs
	taskActionTimer = TaskTimer(1, executeTaskActionList)
	
	#create a bool for use during blackout hours
	#this is to simulate the user getting some sleep
	blackoutActive = False
	blackoutActiveLastScan = False #used for edge detection
	
	#here is the run loop
	while True:

		#decide if the current local time is within the black out time
		blackoutActive = ((time.localtime()[3] >= int(dwarfBeard.BLACKOUT_START_HOUR)) or (time.localtime()[3] < int(dwarfBeard.BLACKOUT_END_HOUR))) and dwarfBeard.BLACKOUT_EN
		
		#signal when black out becomes active
		if blackoutActive and not blackoutActiveLastScan:
			print 'Blackout just became active @', time.localtime()[3]
		elif blackoutActiveLastScan and not blackoutActive:
			print 'Blackout just ended @', time.localtime()[3]
			
		
		#when we get the runTasks signal start the task timer 
		#if its not already running
		#if task collection is in progress the timer will not be running
		if dwarfBeard.runTasks and not blackoutActive:
			if not (taskActionTimer.running or dwarfBeard.taskExecRunning):
				print 'starting task timer'
				#set a default interval. this will be reset by the log out function
				taskActionTimer.interval = 1
				taskActionTimer.start()
		else:
			if taskActionTimer.running:
				if blackoutActive:
					print 'stopping task timer during blackout period'
				else:
					print 'stopping task timer'
				taskActionTimer.stop()
		
		
		
		#set any vars for edge detection
		blackoutActiveLastScan = blackoutActive
		
		#sleep at the end of each scan so processor time is not consumed
		time.sleep(1.0)
			
	
	
if __name__ == "__main__":
	
	main()

	