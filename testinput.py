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
    :param args:
    :type args: argparse.Namespace
    :return void:
    """
    db_name = add_filename_extension(args.name)
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("INSERT or IGNORE INTO Employee VALUES (1, 'John', 'Doe')")
    cursor.execute("INSERT or IGNORE INTO Record VALUES (1, '2021-01-01', '09:00:00', '12:00:00')")
    cursor.execute("INSERT or IGNORE INTO Record VALUES (1, '2021-01-02', '09:00:00', '12:00:00')")
    cursor.execute("INSERT or IGNORE INTO Record VALUES (1, '2021-01-03', '09:00:00', '12:00:00')")
    cursor.execute("INSERT or IGNORE  INTO Pay VALUES (1, '2021-01-01', '10')")
    cursor.execute("INSERT or IGNORE  INTO Pay VALUES (1, '2021-01-02', '10')")
    cursor.execute("INSERT or IGNORE  INTO Pay VALUES (1, '2021-01-03', '10')")

    cursor.execute("INSERT or IGNORE INTO Employee VALUES (2, 'Bob', 'Guy')")
    cursor.execute("INSERT or IGNORE  INTO Record VALUES (2, '2021-01-01', '08:00:00', '12:00:00')")
    cursor.execute("INSERT or IGNORE  INTO Record VALUES (2, '2021-01-02', '08:00:00', '12:00:00')")
    cursor.execute("INSERT or IGNORE  INTO Record VALUES (2, '2021-01-03', '08:00:00', '12:00:00')")
    cursor.execute("INSERT or IGNORE  INTO Pay VALUES (2, '2021-01-01', '5')")
    cursor.execute("INSERT or IGNORE  INTO Pay VALUES (2, '2021-01-02', '5')")
    cursor.execute("INSERT or IGNORE  INTO Pay VALUES (2, '2021-01-03', '5')")
    conn.commit()
    conn.close()


def test_database_connection(db_name: str):
    """
    Tests the database connection
    :param db_name:
    :type db_name: string
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
    :type db_name: string
    :return db_name:
    :rtype db_name: string
    :return filename + ".db":
    :rtype filename + ".db": string
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
