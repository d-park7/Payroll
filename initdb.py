#!/usr/bin/env python3

import sqlite3
import argparse
import sys
import os


def init_db(args):
    # use 'name' to connect to the db
    db_name = add_filename_extension(args.name)

    # create the database with these tables
    # --create -c is an optional arg and raise an error if db specified does not exist
    if args.create:
        conn = create_new_db(db_name)
        
    # make the --override an optional arg
    if args.override:
        conn = delete_existing_db(db_name)
        conn = create_new_db(db_name)

    # verify database is connected
    if conn.total_changes != 0:
        print("Failed to create database.", file=sys.stderr)
        quit()

    # commit and close the db
    conn.commit()
    conn.close()
    return


def add_filename_extension(db_name: str):
    """
    Adds the .db ext if the name does not contain it
    :param db_name:
    :return:
    """
    filename, file_extension = os.path.splitext(db_name)
    if file_extension:
        return db_name
    else:
        return filename + ".db"


def parse_args():
    # argument parser
    parser = argparse.ArgumentParser(description="Initialize the db")
    parser.add_argument(
        "-n",
        "--name",
        type=str,
        required=True,
        help="Name of db file"
    )
    parser.add_argument(
        "-c", "--create", action="store_true", help="Create the db if not existing"
    )
    parser.add_argument(
        "-o", "--override", action="store_true", help="Override the specified db"
    )

    # create variable to hold all args
    args = parser.parse_args()
    return args


def create_new_db(db_name: str):
    """
    Creates a new database if not already made
    :param db_name:
    :return sqlite3 connection:
    """
    dbExists = True
    # try to connect to the named db
    # if it already exists quit the program
    try:
        conn = sqlite3.connect("file:{}?mode=rw".format(db_name), uri=True)
    except Exception:
        dbExists = False
        pass
    if dbExists == True:
        print("Error: Database already exists", file=sys.stderr)
        quit()
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    create_tables(cursor)
    return conn


def delete_existing_db(db_name: str):
    """
    Deletes existing db and replaces it
    :param db_name:
    :return sqlite3 connection:
    """
    # try to delete the db file
    if os.path.exists(db_name):
            os.remove(db_name)
    else:
        print("Error: Database does not exist", file=sys.stderr)
        quit()


def create_tables(cursor):
    cursor.execute(
        "CREATE TABLE Employee (EmployeeId int, FirstName text, LastName text)"
    )
    cursor.execute(
         "CREATE TABLE Record (RecordId int, DateTimeIn text, DateTimeOut text)"
    )
    cursor.execute(
        "CREATE TABLE Pay (PayId int, Pay unsigned int, BiWeeklyStartDate text, BiWeeklyEndDate text)"
    )


def main():
    args = parse_args()
    init_db(args)


if __name__ == "__main__":
    main()
