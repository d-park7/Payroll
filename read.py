#!/usr/bin/env python3

import sqlite3
import argparse

parser = argparse.ArgumentParser(description="Read from the inputted database")
parser.add_argument("name", help="Input the name of the database")

args = parser.parse_args()

namedb = args.name

conn = sqlite3.connect(namedb)
cursor = conn.cursor()

employee = cursor.execute("SELECT * FROM Employee").fetchall()
record = cursor.execute("SELECT * FROM Record").fetchall()
pay = cursor.execute("SELECT * FROM Pay").fetchall()

print("Employee data: ", employee)
print("Records: ", record)
print("Pay: ", pay)

conn.commit()
cursor.close()
conn.close()
