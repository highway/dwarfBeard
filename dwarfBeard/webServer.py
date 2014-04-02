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
	
	