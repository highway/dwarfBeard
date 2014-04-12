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

import dwarfBeard
import re
import time
from threading import Timer
from splinter import Browser
from random import randint
from dwarfBeard.db import DBConnection


class TaskTimer(object):
	def __init__(self, interval, function, *args, **kwargs):
		self._timer     = None
		self.interval   = interval
		self.function   = function
		self.args       = args
		self.kwargs     = kwargs
		self.running = False
		#self.start() #this will cause auto start

	def _run(self):
		self.running = False
		self.function(self, *self.args, **self.kwargs)
		self.start()
		
	def start(self):
		if not self.running:
			self._timer = Timer(self.interval, self._run)
			self._timer.start()
			self.running = True
			#self.function(self, *self.args, **self.kwargs) #this calls the function immediately at the start, not what we want at this time

	def stop(self):
		self._timer.cancel()
		self.running = False
		
		
def logZenExchange(browser, characterName):
	#first we get the purchase price
	#wait for the page to load
	reissueCount = 0
	while browser.is_text_not_present("Top ZEN Listings"):
		x = randint(3,10)
		#go to professions
		print '  attempting to navigate to zen exchange'
		browser.visit('http://gateway.playneverwinter.com/#char(' + characterName + '@' + dwarfBeard.NW_ACCOUNT_NAME + ')/exchange')
		reissueCount += 1
		if reissueCount > 4:
			browser.reload()
			x = 20
			reissueCount = 0
			print '  trying browser reload and sleeping for 20s'
		time.sleep(x)
		
	#collect the data from the zen purchase table, we only need the lowest price
	data = browser.find_by_css('TABLE#gatewayTableBuyZen.dataTable')
	purchaseText = str(data.text).split(" ")
	
	#pull out the lowest price
	lowZenPurchasePrice = filter(None, re.split(r'(\d+)', purchaseText[3]))[0]
	print '  lowest zen purchase price = ', lowZenPurchasePrice
	
	#now we get the sell price
	#wait for the page to load
	reissueCount = 0
	while browser.is_text_not_present("Top ZEN Purchase Requests"):
		x = randint(3,10)
		#go to professions
		print '  attempting to navigate to ad exchange'
		browser.visit('http://gateway.playneverwinter.com/#char(' + characterName + '@' + dwarfBeard.NW_ACCOUNT_NAME + ')/exchange-sellzen')
		if reissueCount > 4:
			browser.reload()
			x = 20
			reissueCount = 0
			print '  trying browser reload and sleeping for 20s'
		time.sleep(x)
		
	#collect the data from the zen purchase table, we only need the lowest price
	#this one is much easier to grab
	data = browser.find_by_css('TABLE#gatewayTableSellZen.dataTable')
	sellText = str(data.text).split(" ")
	lowAdPurchasePrice = sellText[8]
	print '   higest zen sell price = ', lowAdPurchasePrice
	
	#save the data to the db
	#make connection to db
	myDB = DBConnection(dwarfBeard.DB_FILE)
	
	queryString = "INSERT INTO adExchange (adPrice, zenPrice) VALUES (?,?)"
	myDB.action(queryString,(lowAdPurchasePrice, lowZenPurchasePrice))
	
	return
	
	
	
	
	
	
	
		
