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


def dbFilename(filename="dwarf.db", suffix=None):
    """
    @param filename: The sqlite database filename to use. If not specified,
                     will be made to be dwarf.db
    @param suffix: The suffix to append to the filename. A '.' will be added
                   automatically, i.e. suffix='v0' will make dbfile.db.v0
    @return: the correct location of the database file.
    """
    if suffix:
        filename = "%s.%s" % (filename, suffix)
    return ek.ek(os.path.join, dwarfBeard.DATA_DIR, filename)


class InitialSchema (db.SchemaUpgrade):
	def test(self):
		return self.hasTable("tv_shows") and self.hasTable("db_version") and self.checkDBVersion() >= MIN_DB_VERSION and self.checkDBVersion() <= MAX_DB_VERSION

	def execute(self):
		if not self.hasTable("tv_shows") and not self.hasTable("db_version"):
			queries = [
				"CREATE TABLE history (action NUMERIC, date NUMERIC, showid NUMERIC, season NUMERIC, episode NUMERIC, quality NUMERIC, resource TEXT, provider TEXT);",
				"CREATE TABLE info (last_backlog NUMERIC, last_tvdb NUMERIC);",
				"CREATE TABLE tv_episodes (episode_id INTEGER PRIMARY KEY, showid NUMERIC, tvdbid NUMERIC, name TEXT, season NUMERIC, episode NUMERIC, description TEXT, airdate NUMERIC, hasnfo NUMERIC, hastbn NUMERIC, status NUMERIC, location TEXT, file_size NUMERIC, release_name TEXT);",
				"CREATE TABLE tv_shows (show_id INTEGER PRIMARY KEY, location TEXT, show_name TEXT, tvdb_id NUMERIC, network TEXT, genre TEXT, runtime NUMERIC, quality NUMERIC, airs TEXT, status TEXT, flatten_folders NUMERIC, paused NUMERIC, startyear NUMERIC, tvr_id NUMERIC, tvr_name TEXT, air_by_date NUMERIC, lang TEXT, last_update_tvdb NUMERIC);",
				"CREATE INDEX idx_tv_episodes_showid_airdate ON tv_episodes (showid,airdate);",
				"CREATE INDEX idx_showid ON tv_episodes (showid);",
				"INSERT INTO db_version (db_version) VALUES (14);"
			]

			for query in queries:
				self.connection.action(query)



class DBConnection:
    def __init__(self, filename="dwarf.db", suffix=None, row_type=None):

        self.filename = filename
        self.connection = sqlite3.connect(dbFilename(filename), 20)
        if row_type == "dict":
            self.connection.row_factory = self._dict_factory
        else:
            self.connection.row_factory = sqlite3.Row

    def checkDBVersion(self):
        try:
            result = self.select("SELECT db_version FROM db_version")
        except sqlite3.OperationalError, e:
            if "no such table: db_version" in e.args[0]:
                return 0

        if result:
            return int(result[0]["db_version"])
        else:
            return 0

    def mass_action(self, querylist, logTransaction=False):

        with db_lock:

            if querylist == None:
                return

            sqlResult = []
            attempt = 0

            while attempt < 5:
                try:
                    for qu in querylist:
                        if len(qu) == 1:
                            if logTransaction:
                                logger.log(qu[0], logger.DEBUG)
                            sqlResult.append(self.connection.execute(qu[0]))
                        elif len(qu) > 1:
                            if logTransaction:
                                logger.log(qu[0] + " with args " + str(qu[1]), logger.DEBUG)
                            sqlResult.append(self.connection.execute(qu[0], qu[1]))
                    self.connection.commit()
                    logger.log(u"Transaction with " + str(len(querylist)) + u" query's executed", logger.DEBUG)
                    return sqlResult
                except sqlite3.OperationalError, e:
                    sqlResult = []
                    if self.connection:
                        self.connection.rollback()
                    if "unable to open database file" in e.args[0] or "database is locked" in e.args[0]:
                        logger.log(u"DB error: " + ex(e), logger.WARNING)
                        attempt += 1
                        time.sleep(1)
                    else:
                        logger.log(u"DB error: " + ex(e), logger.ERROR)
                        raise
                except sqlite3.DatabaseError, e:
                    sqlResult = []
                    if self.connection:
                        self.connection.rollback()
                    logger.log(u"Fatal error executing query: " + ex(e), logger.ERROR)
                    raise

            return sqlResult

    def action(self, query, args=None):

        with db_lock:

            if query == None:
                return

            sqlResult = None
            attempt = 0

            while attempt < 5:
                try:
                    if args == None:
                        logger.log(self.filename + ": " + query, logger.DEBUG)
                        sqlResult = self.connection.execute(query)
                    else:
                        logger.log(self.filename + ": " + query + " with args " + str(args), logger.DEBUG)
                        sqlResult = self.connection.execute(query, args)
                    self.connection.commit()
                    # get out of the connection attempt loop since we were successful
                    break
                except sqlite3.OperationalError, e:
                    if "unable to open database file" in e.args[0] or "database is locked" in e.args[0]:
                        logger.log(u"DB error: " + ex(e), logger.WARNING)
                        attempt += 1
                        time.sleep(1)
                    else:
                        logger.log(u"DB error: " + ex(e), logger.ERROR)
                        raise
                except sqlite3.DatabaseError, e:
                    logger.log(u"Fatal error executing query: " + ex(e), logger.ERROR)
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
