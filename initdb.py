#!/usr/bin/env python3

import sqlite3
import argparse
import sys


def init_db(args):
    # use 'name' to connect to the db
    db_name = args.name

    # create the database with these tables
    # --create -c is an optional arg and raise an error if db specified does not exist
    if args.create:
        dbExists = True
        # try to connect to the named db
        # if it already exists quit the program
        try:
            conn = sqlite3.connect('file:{}?mode=rw'.format(db_name), uri=True)
        except Exception:
            dbExists = False
            pass
        if (dbExists == True):
            print("Error: Database already exists", file=sys.stderr)
            quit()

        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE Employee (EmployeeId int, FirstName text, LastName text)")
        cursor.execute("CREATE TABLE Record (RecordId int, DateTimeIn text, dateTimeOut text)")
        cursor.execute("CREATE TABLE Pay (PayId int, pay unsigned int, BiWeeklyStartDate text, BiWeeklyEndDate text)")


    # make the --override an optional arg
    if args.override:
        conn = sqlite3.connect(db_name)
        curosr = conn.cursor()
        cursor.execute("CREATE TABLE Employee (EmployeeId int, FirstName text, LastName text)")
        cursor.execute("CREATE TABLE Record (RecordId int, DateTimeIn text, dateTimeOut text)")
        cursor.execute("CREATE TABLE Pay (PayId int, pay unsigned int, BiWeeklyStartDate text, BiWeeklyEndDate text)")

    # verify database is connected
    if conn.total_changes != 0:
        print("Failed to create database.", file=sys.stderr)
        quit()

    # commit changes to db
    conn.commit()
    # close the connection
    conn.close()


def parse_args():
    # argument parser
    parser = argparse.ArgumentParser(description='Initialize the db')
    parser.add_argument("--name", type=str, required=True, help="Name of db file including the .db")
    parser.add_argument("-c", "--create", action='store_true', help="Create the db if not existing")
    parser.add_argument('-o', "--override", action='store_true', help="Override the specified db")

    # create variable to hold all args
    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    init_db(args)


if __name__ == "__main__":
    main()
