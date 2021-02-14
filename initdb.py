#!/usr/bin/env python3

import sqlite3
import argparse
import sys
import os


def parse_args():
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

    args = parser.parse_args()
    return args


def init_db(args):
    """
    Creates the database.
    :param args:
    :type args: argparse.Namespace
    :return void:
    """
    db_name = add_filename_extension(args.name)

    conn = create_new_db(db_name)

    if args.override:
        delete_existing_db(db_name)
        conn = create_new_db(db_name)

    if args.create == True or args.override == True:
        conn.commit()
        conn.close()


def create_new_db(db_name: str):
    """
    Creates a new database if not already made
    :param db_name:
    :type db_name: string
    :return sqlite3.Connection:
    """
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    create_tables(cursor)
    return conn


def delete_existing_db(db_name: str):
    """
    Deletes the existing database
    :param db_name:
    :type db_name: string
    :return void:
    """
    if os.path.exists(db_name):
            os.remove(db_name)
    else:
        print("Error: Database does not exist", file=sys.stderr)
        quit()


def create_tables(cursor):
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS Employee (EmployeeId INTEGER PRIMARY KEY, FirstName TEXT, LastName TEXT)"
    )
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS Pay (EmployeeId INTEGER, Date TEXT, PayPerHour UNSIGNED FLOAT, PRIMARY KEY(EmployeeId, Date), FOREIGN KEY(EmployeeId) REFERENCES Employee(EmployeeId))"
    )
    cursor.execute(
         "CREATE TABLE IF NOT EXISTS Record (EmployeeId INTEGER, Date TEXT, Time TEXT, TimeInFlag INT, PRIMARY KEY(EmployeeId, Date, Time, TimeInFlag), FOREIGN KEY(EmployeeId) REFERENCES Employee(EmployeeId))"
    )


def add_filename_extension(db_name: str):
    """
    Adds the .db ext if the name does not contain it
    :param db_name:
    :type db_name: string
    :return db_name:
    :rtype string:
    :return filename + ".db":
    :rtype string:
    """
    filename, file_extension = os.path.splitext(db_name)
    if file_extension:
        return db_name
    else:
        return filename + ".db"


def main():
    args = parse_args()
    init_db(args)


if __name__ == "__main__":
    main()