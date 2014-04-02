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
from threading import Timer


def openAbrowser(profilePath):
	#open a browser and select a profile so that cookies will be used and saved
	browser = Browser('firefox', profile = profilePath)

	#return the browser
	return browser
	
#this closes the browser
def closeAbrowser(browser):
	
	x = randint(5,12)
	print '  waiting to close the browser', x, 's'
	time.sleep(x)
	print '  closing browser'
	browser.quit()
	
	return
	
def loginToSite(browser, userName, password):
	#enter the never winter url
	browser.visit('http://gateway.playneverwinter.com/')

	###########################################
	#wait for the page to load
	while browser.is_text_not_present('Please log in with'):
		print '  waiting for login page to load'
		time.sleep(10) # delays for 10 seconds

	#login credentials
	browser.fill('user', userName)
	browser.fill('pass', password)

	# enter the site
	browser.find_by_name('button').click()
	
	return
	