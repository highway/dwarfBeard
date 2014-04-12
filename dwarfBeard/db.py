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
import re
import sqlite3
import time
import threading

import dwarfBeard


db_lock = threading.Lock()


class DBConnection:
	def __init__(self, filename="dwarf.db", suffix=None, row_type=None):

		self.filename = filename
		self.connection = sqlite3.connect(filename)
		if row_type == "dict":
		    self.connection.row_factory = self._dict_factory
		else:
		    self.connection.row_factory = sqlite3.Row

	def hasTable(self, tableName):
		return len(self.action("SELECT 1 FROM sqlite_master WHERE name = ?;", (tableName, )).fetchall()) > 0

	def initTest(self):
		return self.hasTable("characterNames") and self.hasTable("tasks") and self.hasTable("adExchange")

	def createInitialSchema(self):
		print 'creating initial db schema'
		if not self.hasTable("tv_shows") and not self.hasTable("db_version"):
			queries = [
				"CREATE TABLE characterNames (characterName TEXT);",
				"CREATE TABLE tasks (characterName TEXT, taskName TEXT, taskLevel TEXT, taskProfession TEXT);",
				"CREATE TABLE adExchange (adPrice TEXT, zenPrice TEXT, timestamp DATETIME DEFAULT (datetime('now','localtime')));",
			]

			for query in queries:
				self.action(query)

	def action(self, query, args=None):

		with db_lock:

			if query == None:
				return

			sqlResult = None
			attempt = 0

			while attempt < 5:
				try:
					if args == None:
						sqlResult = self.connection.execute(query)
					else:
						sqlResult = self.connection.execute(query, args)
						self.connection.commit()
					# get out of the connection attempt loop since we were successful
					break
				except sqlite3.OperationalError, e:
					if "unable to open database file" in e.args[0] or "database is locked" in e.args[0]:
						attempt += 1
						time.sleep(1)
					else:
						raise
				except sqlite3.DatabaseError, e:
					raise

			return sqlResult

	def select(self, query, args=None):

		sqlResults = self.action(query, args).fetchall()

		if sqlResults == None:
			return []

		return sqlResults

	def upsert(self, tableName, valueDict, keyDict):

		changesBefore = self.connection.total_changes

		genParams = lambda myDict: [x + " = ?" for x in myDict.keys()]

		query = "UPDATE " + tableName + " SET " + ", ".join(genParams(valueDict)) + " WHERE " + " AND ".join(genParams(keyDict))

		self.action(query, valueDict.values() + keyDict.values())

		if self.connection.total_changes == changesBefore:
			query = "INSERT INTO " + tableName + " (" + ", ".join(valueDict.keys() + keyDict.keys()) + ")" + \
					" VALUES (" + ", ".join(["?"] * len(valueDict.keys() + keyDict.keys())) + ")"
			self.action(query, valueDict.values() + keyDict.values())

	def tableInfo(self, tableName):
		# FIXME ? binding is not supported here, but I cannot find a way to escape a string manually
		cursor = self.connection.execute("PRAGMA table_info(%s)" % tableName)
		columns = {}
		for column in cursor:
			columns[column['name']] = { 'type': column['type'] }
		return columns

	# http://stackoverflow.com/questions/3300464/how-can-i-get-dict-from-sqlite-query
	def _dict_factory(self, cursor, row):
		d = {}
		for idx, col in enumerate(cursor.description):
			d[col[0]] = row[idx]
		return d
