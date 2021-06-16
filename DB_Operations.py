import os
import sqlite3
import threading


class DbQueries:

    create_path_table = "CREATE TABLE IF NOT EXISTS paths(serial_no INTEGER PRIMARY KEY AUTOINCREMENT," \
                        " path VARCHAR(200));"
    create_file_table = "CREATE TABLE IF NOT EXISTS file(serial_no INTEGER PRIMARY KEY, file VARCHAR(100)," \
                        " currentlyplaying  BOOLEAN NOT NULL CHECK (currentlyplaying IN (0, 1))," \
                        "'delete' BOOLEAN NOT NULL CHECK ('delete' IN (0, 1)), collection VARCHAR(30));"

    insert_path = "INSERT INTO paths(path) VALUES(?);"
    insert_file = "INSERT INTO file(file, currentlyplaying, delete, collection) VALUES(?, ?, ?, ?);"

    delete_all_paths = "DELETE FROM paths;"
    delete_all_files = "DELETE FROM file;"

    display_all_paths = "SELECT * FROM paths;"
    display_all_files = "SELECT * FROM file;"


class DBHandler:

    _sql_file = r"UserResources\paths.db"
    _resource_folder = "UserResources"

    def __init__(self, *args):

        if not os.path.exists(self._resource_folder):
            os.mkdir(self._resource_folder)

        for table in [DbQueries.create_path_table, DbQueries.create_file_table]:
            self.createTable(table)

    def createTable(self, sqlQuery):
        with sqlite3.connect(self._sql_file, check_same_thread=False) as conn:
            conn.execute(sqlQuery)
            conn.commit()

    def getFiles(self):
        with sqlite3.connect(self._sql_file) as conn:
            curr = conn.cursor()
            curr.execute(DbQueries.display_all_files)
            items = curr.fetchall()

        return items

    def getPaths(self):
        with sqlite3.connect(self._sql_file) as conn:
            curr = conn.cursor()
            curr.execute(DbQueries.display_all_paths)
            items = curr.fetchall()

        return items

    def deleteAllFiles(self):

        with sqlite3.connect(self._sql_file) as conn:
            conn.execute(DbQueries.delete_all_files)
            conn.commit()

    def deleteAllPaths(self):

        with sqlite3.connect(self._sql_file) as conn:
            conn.execute(DbQueries.delete_all_paths)
            conn.commit()

    def _insertPaths(self, dirs):
        self.deleteAllPaths()
        with sqlite3.connect(self._sql_file) as conn:
            for dir in dirs:
                conn.execute(DbQueries.insert_path, (dir, ))

            conn.commit()

    def insertToPaths(self, dirs: set):
        thread = threading.Thread(target=self._insertPaths, args=(dirs,))
        thread.start()

    def _insertFiles(self, files):
        self.deleteAllFiles()
        with sqlite3.connect(self._sql_file) as conn:
            for file in files:
                conn.execute(DbQueries.insert_file, (file, ))

            conn.commit()

    def insertToFiles(self, files: set):
        thread = threading.Thread(target=self._insertFiles, args=(files, ))