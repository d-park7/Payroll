#!/usr/bin/env python3

from initdb import add_filename_extension
import sqlite3
import argparse
import sys
import os


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-n",
        "--name",
        type=str,
        required=True,
        help="Name of database"
    )
    args = parser.parse_args()
    return args


def input_data(args):
    """
    Inputs test data into the database
    :param db_name:
    :return sqlite3 connection:
    """
    db_name = add_filename_extension(args.name)
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Employee VALUES (1, 'John', 'Doe')")
    cursor.execute("INSERT INTO Record VALUES (1, '2021-01-01 08:00:01', '2021-01-01 17:00:02', NULL)")
    cursor.execute("INSERT INTO Pay VALUES (1, 10, '2021-01-01', '2021-01-15')")
    conn.commit()
    conn.close()


def test_database_connection(db_name: str):
    """
    Tests the database connection
    :param db_name:
    :return void:
    """
    dbExists = True
    try:
        conn = sqlite3.connect(db_name)
    except Exception as e:
        dbExists = False
        pass
    if dbExists == False:   
        print("Error: Database does not exist", file=sys.stderr)
        quit()


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


def main():
    args = parse_args()
    input_data(args)


if __name__ == "__main__":
    main()
