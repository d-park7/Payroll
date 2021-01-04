#!/usr/bin/env python3

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
    dbExists = True
    # try to connect to the named db
    # if it does not exist quit the program
    try:
        conn = sqlite3.connect(db_name)
    except Exception:
        dbExists = False
        pass
    if dbExists == False:   
        print("Error: Database does not exist", file=sys.stderr)
        quit()

    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Employee VALUES (2 , 'asdf', 'Dsd')")
    cursor.execute("INSERT INTO Record VALUES (2, '2020-01-01 08:00:00', '2020-01-01 17:00:00')")
    cursor.execute("INSERT INTO Pay VALUES (2, 10, '2020-01-01', '2020-01-15')")
    conn.commit()
    conn.close()


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
