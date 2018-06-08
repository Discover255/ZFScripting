# -*- coding:utf8 -*-
import sqlite3

class DBService :
    __connect = object()
    __cursor = object()
    def __init__(self):
        self.__connect = sqlite3.connect("label.db")
        self.__cursor =self.__connect.cursor()

    def getMaxIndex(self):
        self.__cursor.execute("SELECT MAX(ind) FROM main")
        return self.__cursor.fetchall()[0][0] + 1

    def getLabel(self, index):
        self.__cursor.execute("SELECT label FROM main WHERE ind="+str(index))
        return self.__cursor.fetchall()[0][0]

    def __del__(self):
        print("Closing Sqlite3 connection")
        self.__cursor.close()
        self.__connect.close()