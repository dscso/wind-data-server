import sys
import sqlite3

class database(object):
    def __init__(self, filename):
        print ("[info]   Opening SQLite file: '%s'..." % filename)
        try:
            self.db = sqlite3.connect(filename)
            self.cursor = self.db.cursor()
        except Exception as e:
            print ("[error]  can't open SQLite database: '%s'" % e)
            sys.exit(1);
    def getData(dateFrom, dataTo):
        pass

    def setData():
        pass

    def close(self):
        print ("[info]   Closing SQLite database...")
        try:
            self.cursor.close()
            self.db.commit()
            self.db.close()
        except Exception as e:
            print ("[error]  %s" % e)
