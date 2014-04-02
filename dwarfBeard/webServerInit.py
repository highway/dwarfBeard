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


import cherrypy.lib.auth_basic
import os.path

import dwarfBeard

from dwarfBeard.webServer import WebInterface



def initWebServer(options={}):
	options.setdefault('port', 8083)
	options.setdefault('host', '0.0.0.0')
	options.setdefault('log_dir', None)
	options.setdefault('username', '')
	options.setdefault('password', '')
	options.setdefault('web_root', '/')
	assert isinstance(options['port'], int)
	assert 'data_root' in options

	def http_error_401_hander(status, message, traceback, version):
		""" Custom handler for 401 error """
		if status != "401 Unauthorized":
			print "CherryPy caught an error: %s %s" % (status, message)
		return r'''<!DOCTYPE html>
<html>
    <head>
        <title>%s</title>
    </head>
    <body>
        <br/>
        <font color="#0000FF">Error %s: You need to provide a valid username and password.</font>
    </body>
</html>
''' % ('Access denied', status)

	def http_error_404_hander(status, message, traceback, version):
		""" Custom handler for 404 error, redirect back to main page """
		return r'''<!DOCTYPE html>
<html>
    <head>
        <title>404</title>
    </head>
    <body>
        <br/>
		Page not found 	<br/>
    </body>
</html>
'''

    # cherrypy setup
	mime_gzip = ('text/html',
				 'text/plain',
				 'text/css',
				 'text/javascript',
				 'application/javascript',
				 'text/x-javascript',
				 'application/x-javascript',
				 'text/x-json',
				 'application/json'
				 )

	options_dict = {
				'server.socket_port': options['port'],
				'server.socket_host': options['host'],
				'log.screen': False,
				'engine.autoreload.on': False,
				'engine.autoreload.frequency': 100,
				'engine.reexec_retry': 100,
				'tools.gzip.on': True,
				'tools.gzip.mime_types': mime_gzip,
				'error_page.401': http_error_401_hander,
				'error_page.404': http_error_404_hander,
				}

	protocol = "http"

	cherrypy.config.update(options_dict)

	# setup cherrypy logging
	if options['log_dir'] and os.path.isdir(options['log_dir']):
		cherrypy.config.update({ 'log.access_file': os.path.join(options['log_dir'], "cherrypy.log") })
		print 'Using %s for cherrypy log' % cherrypy.config['log.access_file']

	conf = {
			'/': {
				'tools.staticdir.root': options['data_root'],
				'tools.encode.on': True,
				'tools.encode.encoding': 'utf-8',
			},
				'/images': {
				'tools.staticdir.on': True,
				'tools.staticdir.dir': 'images'
			},
				'/js': {
				'tools.staticdir.on': True,
				'tools.staticdir.dir': 'js'
			},
				'/css': {
				'tools.staticdir.on': True,
				'tools.staticdir.dir': 'css'
			},
			}
	
	app = cherrypy.tree.mount(WebInterface(), options['web_root'], conf)

	# auth
	if options['username'] != "" and options['password'] != "":
		checkpassword = cherrypy.lib.auth_basic.checkpassword_dict({options['username']: options['password']})
		app.merge({
			'/': {
				'tools.auth_basic.on': True,
				'tools.auth_basic.realm': 'dwarfBeard',
				'tools.auth_basic.checkpassword': checkpassword
			},
				'/api': {
				'tools.auth_basic.on': False
			},
				'/api/builder': {
				'tools.auth_basic.on': True,
				'tools.auth_basic.realm': 'dwarfBeard',
				'tools.auth_basic.checkpassword': checkpassword
			}
		})

	cherrypy.server.start()
	cherrypy.server.wait()
