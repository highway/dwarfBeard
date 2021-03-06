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


import os.path

import time
import urllib
import re
import threading
import datetime
import random

from Cheetah.Template import Template
import cherrypy.lib

import dwarfBeard
from dwarfBeard import notifiers
from dwarfBeard.db import DBConnection

try:
    import json
except ImportError:
    from lib import simplejson as json



class PageTemplate (Template):
	def __init__(self, *args, **KWs):
		KWs['file'] = os.path.join(dwarfBeard.PROG_DIR, "webData/interfaces/default/", KWs['file'])
		super(PageTemplate, self).__init__(*args, **KWs)
		self.siteRoot = dwarfBeard.WEB_ROOT
		self.siteHttpPort = dwarfBeard.WEB_PORT
		
		if cherrypy.request.headers['Host'][0] == '[':
			self.siteHost = re.match("^\[.*\]", cherrypy.request.headers['Host'], re.X|re.M|re.S).group(0)
		else:
			self.siteHost = re.match("^[^:]+", cherrypy.request.headers['Host'], re.X|re.M|re.S).group(0)
        
		self.projectHomePage = "https://github.com/highway/dwarfBeard"

		if "X-Forwarded-Host" in cherrypy.request.headers:
			self.siteHost = cherrypy.request.headers['X-Forwarded-Host']
		if "X-Forwarded-Port" in cherrypy.request.headers:
			self.siteHttpPort = cherrypy.request.headers['X-Forwarded-Port']
			self.siteHttpsPort = self.sbHttpPort
		if "X-Forwarded-Proto" in cherrypy.request.headers:
			self.siteHttpsEnabled = True if cherrypy.request.headers['X-Forwarded-Proto'] == 'https' else False

		logPageTitle = 'Logs &amp; Errors'
		self.logPageTitle = logPageTitle
		self.sitePID = str(dwarfBeard.PID)
		self.siteMenu = [
			{ 'title': 'Home',            'path': 'home/'           },
			{ 'title': 'Manage',          'path': 'manage/'         },
			{ 'title': 'AD Exchange',     'path': 'adexchange/'         },
			{ 'title': 'Config',          'path': 'config/'         },
			]

			

def redirect(abspath, *args, **KWs):
    assert abspath[0] == '/'
    raise cherrypy.HTTPRedirect(dwarfBeard.WEB_ROOT + abspath, *args, **KWs)


def _munge(string):
    return unicode(string).encode('utf-8', 'xmlcharrefreplace')


	
class Home:

	@cherrypy.expose
	def is_alive(self, *args, **kwargs):
		if 'callback' in kwargs and '_' in kwargs:
			callback, _ = kwargs['callback'], kwargs['_']
		else:
			return "Error: Unsupported Request. Send jsonp request with 'callback' variable in the query string."
		cherrypy.response.headers['Cache-Control'] = "max-age=0,no-cache,no-store"
		cherrypy.response.headers['Content-Type'] = 'text/javascript'
		cherrypy.response.headers['Access-Control-Allow-Origin'] = '*'
		cherrypy.response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'

		if dwarfBeard.started:
			return callback + '(' + json.dumps({"msg": str(dwarfBeard.PID)}) + ');'
		else:
			return callback + '(' + json.dumps({"msg": "nope"}) + ');'

	@cherrypy.expose
	def index(self):
		t = PageTemplate(file="home.tmpl")
		return _munge(t)
		
	@cherrypy.expose
	def runTasks(self):
		#toggle task run
		dwarfBeard.runTasks = not dwarfBeard.runTasks
		redirect("/home/")
		
	@cherrypy.expose
	def twitterStep1(self):
		cherrypy.response.headers['Cache-Control'] = "max-age=0,no-cache,no-store"

		return notifiers.twitter_notifier._get_authorization()

	@cherrypy.expose
	def twitterStep2(self, key):
		cherrypy.response.headers['Cache-Control'] = "max-age=0,no-cache,no-store"

		result = notifiers.twitter_notifier._get_credentials(key)
		print u"result:", str(result)
		if result:
			return "Key verification successful"
		else:
			return "Unable to verify key"

	@cherrypy.expose
	def testTwitter(self):
		cherrypy.response.headers['Cache-Control'] = "max-age=0,no-cache,no-store"

		result = notifiers.twitter_notifier.test_notify()
		if result:
			return "Tweet successful, check your twitter to make sure it worked"
		else:
			return "Error sending tweet"

class Manage:
	
	@cherrypy.expose
	def index(self):
	
		#get a db connection
		myDB = DBConnection(dwarfBeard.DB_FILE)
		
		#load the page template
		t = PageTemplate(file="manage.tmpl")
		
		#get a list of the character names as strings
		results = myDB.action('SELECT * FROM characterNames')
		charList = []
		for eachName in results:
			charList.append(str(eachName['characterName']))
		
		#set the character name list to the page template
		t.characterResults = charList
		
		#create a blank task list to hold tasks sorted by character
		characterTasksList = []
		#get a seperate task list for each character
		for eachName in charList:
			results = myDB.action('SELECT * FROM tasks WHERE characterName=?', (eachName,))
			taskList = []
			for eachTask in results:
				taskList.append(eachTask)
			#append each characters task list to the main list sorted by character
			characterTasksList.append([eachName, taskList])
		
		#set the sorted task list to the tamplate
		t.taskResults = characterTasksList
		
		return _munge(t)
		
		
	@cherrypy.expose
	def addNewTask(self, character_Name=None, task_Name=None, task_Level=None, task_Profession="Alchemy"):
		
		myDB = DBConnection(dwarfBeard.DB_FILE)
		
		queryString = "INSERT INTO tasks (characterName, taskName, taskLevel, taskProfession) VALUES (?,?,?,?)"
		
		myDB.action(queryString,(character_Name, task_Name, task_Level, task_Profession))
		
		redirect("/manage/")
		
	@cherrypy.expose
	def addNewCharacter(self, character_Name=None):
		myDB = DBConnection(dwarfBeard.DB_FILE)
		queryString = "INSERT INTO characterNames (characterName) VALUES (?)"
		myDB.action(queryString,(character_Name,))
		redirect("/manage/")
		
	@cherrypy.expose
	def deleteCharacter(self, character_Name=None):
		myDB = DBConnection(dwarfBeard.DB_FILE)
		queryString = "DELETE FROM characterNames WHERE characterName=?"
		myDB.action(queryString,(character_Name,))
		queryString = "DELETE FROM tasks WHERE characterName=?"
		myDB.action(queryString,(character_Name,))
		redirect("/manage/")
		
	@cherrypy.expose
	def deleteTask(self, character_Name=None, task_Name=None, task_Level=None):
		myDB = DBConnection(dwarfBeard.DB_FILE)
		queryString = "DELETE FROM tasks WHERE characterName=? AND taskName=? AND taskLevel=?"
		myDB.action(queryString,(character_Name, task_Name, task_Level))
		redirect("/manage/")
		
	

class Config:

	@cherrypy.expose
	def index(self):
		t = PageTemplate(file="config.tmpl")
		return _munge(t)
		
	@cherrypy.expose
	def saveGeneral(self, log_dir=None, web_port=8083, web_log=0, web_ipv6=0,
					launch_browser=True, web_username=None, web_password=None, version_notify=None,
					ff_profile_path=None, nw_user_name=None, nw_password=None, nw_account_name=None,
					blackout_en=False, blackout_start_hour=22, blackout_end_hour=7):
					
		if launch_browser == "on":
			launch_browser = 1
		else:
			launch_browser = 0
			
		if version_notify == "on":
			version_notify = 1
		else:
			version_notify = 0
			
		dwarfBeard.LAUNCH_BROWSER = launch_browser

		dwarfBeard.WEB_PORT = int(web_port)
		dwarfBeard.WEB_IPV6 = web_ipv6
		dwarfBeard.WEB_USERNAME = web_username
		dwarfBeard.WEB_PASSWORD = web_password
		
		dwarfBeard.FF_PROFILE_PATH = ff_profile_path
		dwarfBeard.NW_USER_NAME = nw_user_name
		dwarfBeard.NW_PASSWORD = nw_password
		dwarfBeard.NW_ACCOUNT_NAME = nw_account_name
		
		if blackout_en == "on":
			blackout_en = 1
		else:
			blackout_en = 0
			
		dwarfBeard.BLACKOUT_EN = blackout_en
		dwarfBeard.BLACKOUT_START_HOUR = blackout_start_hour
		dwarfBeard.BLACKOUT_END_HOUR = blackout_end_hour
		
		dwarfBeard.save_config()
		
		redirect("/config/")
		
		
	@cherrypy.expose
	def saveNotifications(self, use_twitter=None, twitter_notify_on_levelup=None, twitter_notify_on_raretask=None):

		#twitter
		dwarfBeard.USE_TWITTER = use_twitter == 'on'
		dwarfBeard.TWITTER_NOTIFY_ON_LEVELUP = twitter_notify_on_levelup == 'on'
		dwarfBeard.TWITTER_NOTIFY_ON_RARETASK = twitter_notify_on_raretask == 'on'

		dwarfBeard.save_config()	
		
		print 'Configuration Saved'

		redirect("/config/")
					
	
	
class AdExchange:

	@cherrypy.expose
	def index(self):
		t = PageTemplate(file="adexchange.tmpl")
		
		myDB = DBConnection(dwarfBeard.DB_FILE)
		
		results = myDB.action('SELECT * FROM adExchange')
		
		adData = []
		for eachRow in results:
			adData.append({'adPrice': int(eachRow['adPrice']), 'zenPrice': int(eachRow['zenPrice']), 'timestamp': str(eachRow['timestamp'])})
		
		t.adData = adData
		
		return _munge(t)
	
	
	

class WebInterface:

	@cherrypy.expose
	def robots_txt(self):
		""" Keep web crawlers out """
		cherrypy.response.headers['Content-Type'] = 'text/plain'
		return 'User-agent: *\nDisallow: /\n'

	@cherrypy.expose
	def index(self):
		redirect("/home/")
		
	home = Home()
	manage = Manage()
	config = Config()
	adexchange = AdExchange()
	