import sqlite3 as lite
import sys



con = lite.connect('SmartlockUser.db')

with con:

		cur = con.cursor()
		cur.execute("DROP TABLE IF EXISTS SmartlockUser")
		cur.execute("DROP TABLE IF EXISTS Raspip")
		cur.execute("DROP TABLE IF EXISTS Raspkey")
		cur.execute("CREATE TABLE SmartlockUser( Username TEXT,Password TEXT, Regiskey TEXT)")
		cur.execute("CREATE TABLE Raspip(IP TEXT)")
		cur.execute("CREATE TABLE Raspkey(KEY TEXT)")
