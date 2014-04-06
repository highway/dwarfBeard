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


import os
import sys
import webbrowser
import cherrypy
import datetime
import re
import socket
import sqlite3
import subprocess
import urllib

from lib.configobj import ConfigObj
from threading import Lock
import cherrypy
from dwarfBeard.config import CheckSection, check_setting_str, check_setting_int

runTasks = 0

CONFIG_VERSION = 2
MY_FULLNAME = None
MY_NAME = None
PROG_DIR = ''
DATA_DIR = ''
CFG = None
CONFIG_FILE = None
DB_FILE = ''

FF_PROFILE_PATH = ''
NW_USER_NAME = ''
NW_PASSWORD = ''
NW_ACCOUNT_NAME = ''

WEB_PORT = None
WEB_HOST = None
WEB_IPV6 = None
WEB_LOG = None
WEB_ROOT = None
WEB_USERNAME = None
WEB_PASSWORD = None

LAUNCH_BROWSER = None

taskExecRunning = 0

INIT_LOCK = Lock()
__INITIALIZED__ = False



def initialize():

	with INIT_LOCK:

		global runTasks, ACTUAL_LOG_DIR, LOG_DIR, WEB_PORT, WEB_LOG, WEB_ROOT, WEB_USERNAME, WEB_PASSWORD, WEB_HOST, WEB_IPV6, \
			LAUNCH_BROWSER, FF_PROFILE_PATH, NW_USER_NAME, NW_PASSWORD, NW_ACCOUNT_NAME, taskExecRunning, __INITIALIZED__

		if __INITIALIZED__:
			return False
		
		CheckSection(CFG, 'General')

		ACTUAL_LOG_DIR = check_setting_str(CFG, 'General', 'log_dir', 'Logs')
		# put the log dir inside the data dir, unless an absolute path
		LOG_DIR = os.path.normpath(os.path.join(DATA_DIR, ACTUAL_LOG_DIR))
		
		try:
			WEB_PORT = check_setting_int(CFG, 'General', 'web_port', 8083)
		except:
			WEB_PORT = 8083

		if WEB_PORT < 21 or WEB_PORT > 65535:
			WEB_PORT = 8083
		
		WEB_HOST = check_setting_str(CFG, 'General', 'web_host', '0.0.0.0')
		WEB_IPV6 = bool(check_setting_int(CFG, 'General', 'web_ipv6', 0))
		WEB_ROOT = check_setting_str(CFG, 'General', 'web_root', '').rstrip("/")
		WEB_LOG = bool(check_setting_int(CFG, 'General', 'web_log', 0))
		WEB_USERNAME = check_setting_str(CFG, 'General', 'web_username', '')
		WEB_PASSWORD = check_setting_str(CFG, 'General', 'web_password', '')
		LAUNCH_BROWSER = bool(check_setting_int(CFG, 'General', 'launch_browser', 1))
		
		FF_PROFILE_PATH = check_setting_str(CFG, 'General', 'ff_profile_path', '')
		NW_USER_NAME = check_setting_str(CFG, 'General', 'nw_user_name', '')
		NW_PASSWORD = check_setting_str(CFG, 'General', 'nw_password', '')
		NW_ACCOUNT_NAME = check_setting_str(CFG, 'General', 'nw_account_name', '')
		
		if not os.path.isfile(CONFIG_FILE):
			print "Unable to find '" + CONFIG_FILE + "', all settings will be default!"
			save_config()
			
		
		__INITIALIZED__ = True
		return True
		

def save_config():

	new_config = ConfigObj()
	new_config.filename = CONFIG_FILE
	
	new_config['General'] = {}
	new_config['General']['config_version'] = CONFIG_VERSION
	new_config['General']['log_dir'] = ACTUAL_LOG_DIR if ACTUAL_LOG_DIR else 'Logs'
	new_config['General']['web_port'] = WEB_PORT
	new_config['General']['web_host'] = WEB_HOST
	new_config['General']['web_ipv6'] = int(WEB_IPV6)
	new_config['General']['web_log'] = int(WEB_LOG)
	new_config['General']['web_root'] = WEB_ROOT
	new_config['General']['web_username'] = WEB_USERNAME
	new_config['General']['web_password'] = WEB_PASSWORD
	new_config['General']['launch_browser'] = LAUNCH_BROWSER
	new_config['General']['ff_profile_path'] = FF_PROFILE_PATH
	new_config['General']['nw_user_name'] = NW_USER_NAME
	new_config['General']['nw_password'] = NW_PASSWORD
	new_config['General']['nw_account_name'] = NW_ACCOUNT_NAME
	new_config.write()
	
	
def launchBrowser(startPort=None):
    if not startPort:
        startPort = WEB_PORT
    browserURL = 'http://localhost:%d%s' % (startPort, WEB_ROOT)
    try:
        webbrowser.open(browserURL, 2, 1)
    except:
        try:
            webbrowser.open(browserURL, 1, 1)
        except:
            print "Unable to launch a browser"