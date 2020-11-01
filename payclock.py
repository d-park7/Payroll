#!/usr/bin/env python3

import sqlite3

conn = sqlite3.connect("payclock.db")

# verify database is connected
if conn.total_changes != 0:
    print("Failed to create database.")
    quit()

# Create the cursor obj
cursor = conn.cursor()

# Create the employee info table
cursor.execute("CREATE TABLE employeeInfo (id int, firstName text, lastName text)")

# create the records table
cursor.execute("CREATE TABLE records (id int, dateTimeIn text, dateTimeOut text)")

#create the pay info table
cursor.execute("CREATE TABLE payInfo (id int, biWeeklyStartDate text, biWeeklyEndDate text)")
