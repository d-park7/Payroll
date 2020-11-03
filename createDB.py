#!/usr/bin/env python3

import sqlite3

conn = sqlite3.connect("payclock.db")

# verify database is connected
if conn.total_changes != 0:
    print("Failed to create database.")
    quit()

# create the cursor obj
cursor = conn.cursor()

# create the employee info table
cursor.execute("CREATE TABLE Employee (EmployeeId int, FirstName text, LastName text)")

# create the records table
cursor.execute("CREATE TABLE Record (RecordId int, DateTimeIn text, dateTimeOut text)")

# create the pay info table
cursor.execute("CREATE TABLE Pay (PayId int, pay unsigned int, BiWeeklyStartDate text, BiWeeklyEndDate text)")

# close the cursor
cursor.close()
# close the connection
conn.close()
