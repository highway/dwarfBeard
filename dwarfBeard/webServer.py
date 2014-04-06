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
		

class Manage:
	
	@cherrypy.expose
	def index(self):
	
		myDB = DBConnection(dwarfBeard.DB_FILE)
		
		t = PageTemplate(file="manage.tmpl")
		
		results = myDB.action('SELECT * FROM characterNames')
		charList = []
		for eachName in results:
			charList.append(str(eachName['characterName']))
		
		t.characterResults = charList
		
		characterTasksList = []
		
		for eachName in charList:
			results = myDB.action('SELECT * FROM tasks WHERE characterName=?', (eachName,))
			taskList = []
			for eachTask in results:
				taskList.append(eachTask)
			characterTasksList.append([eachName, taskList])
		
		t.taskResults = characterTasksList
		
		return _munge(t)
		
		
	@cherrypy.expose
	def addNewTask(self, character_Name=None, task_Name=None, task_Level=None, prof_Select=None, is_Alchemy=None, is_Platesmithing=None,
					is_Weaponsmithing=None, is_Mailsmithing=None, is_Artificing=None, is_Tailoring=None, 
					is_Leadership=None, is_Leatherworking=None):
		
		if prof_Select == "Alchemy": 
			is_Alchemy = 1 
		else: 
			is_Alchemy = 0
			
		if prof_Select == "Platesmithing":
			is_Platesmithing = 1
		else:
			is_Platesmithing = 0
			
		if prof_Select == "Weaponsmithing":
			is_Weaponsmithing = 1
		else:
			is_Weaponsmithing = 0
			
		if prof_Select == "Mailsmithing":
			is_Mailsmithing = 1
		else:
			is_Mailsmithing = 0
			
		if prof_Select == "Artificing":
			is_Artificing = 1
		else:
			is_Artificing = 0
			
		if prof_Select == "Tailoring":
			is_Tailoring = 1
		else:
			is_Tailoring = 0
			
		if prof_Select == "Leadership":
			is_Leadership = 1
		else:
			is_Leadership = 0
			
		if prof_Select == "Leatherworking":
			is_Leatherworking = 1
		else:
			is_Leatherworking = 0
			
		if prof_Select == None:
			print 'no proff selected'
		
		myDB = DBConnection(dwarfBeard.DB_FILE)
		
		queryString = "INSERT INTO tasks (characterName, taskName, taskLevel, isAlchemy, isPlatesmithing, isWeaponsmithing, isMailsmithing, isArtificing, isTailoring, isLeadership, isLeatherworking) VALUES (?,?,?,?,?,?,?,?,?,?,?)"
		
		myDB.action(queryString,(character_Name, task_Name, task_Level, is_Alchemy, is_Platesmithing, is_Weaponsmithing, is_Mailsmithing, is_Artificing, is_Tailoring, is_Leadership, is_Leatherworking))
		
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
					launch_browser=None, web_username=None, web_password=None, version_notify=None,
					ff_profile_path=None, nw_user_name=None, nw_password=None, nw_account_name=None):
					
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
		
		dwarfBeard.save_config()
		
		redirect("/config/")
					
	

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
	