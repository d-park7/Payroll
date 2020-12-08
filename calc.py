#!/usr/bin/env python3

import sqlite3
import datetime

conn = sqlite3.connect("payclock.db")
cursor = conn.cursor()

timeIn = cursor.execute("SELECT dateTimeIn FROM records ORDER BY ROWID ASC LIMIT 1").fetchall()
timea, = timeIn
print(timea)

timeOut = cursor.execute("SELECT dateTimeOut FROM records ORDER BY ROWID ASC LIMIT 1").fetchall()
timeb, = timeOut
print(timeb)

a = datetime.datetime.strptime(timea, "%Y-%m-%d %H:%M:%S")
b = datetime.datetime.strptime(timeb, "%Y-%m-%d %H:%M:%S")
print("out - in ", b - a)
