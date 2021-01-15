#!/usr/bin/env python3

import sqlite3
import argparse
import os
import pandas as pd


def pargse_args():
    # argument parser
    parser = argparse.ArgumentParser(description="Read from the inputted database")
    parser.add_argument(
        "-n",
        "--name",
        type=str,
        required=True,
        help="Name of db file")
    parser.add_argument(
        "-r",
        "--read",
        action="store_true",
        help="Read the data into a csv"
    )

    args = parser.parse_args()
    return args


def read(args):
    """
    Reads from db to a csv file
    :param db_name:
    :return sqlite3 connection:
    """
    # try to connect to the named db
    # if it does not eist quit the program
    db_name = add_filename_extension(args.name)
    dbExists = True
    try:
        conn = sqlite3.connect(db_name)
    except Exception:
        dbExists = False
        pass
    if dbExists == False:
        print("Error: Datababse does not exist", file=sys.stderr)
        os.system("PAUSE")
        quit()
    db_name = add_filename_extension(args.name)
    if args.read:
        conn = sqlite3.connect(db_name)

        # query database for data
        SQLQuery = 'SELECT * FROM Record'

        # create a dataframe from database using pandas
        df = pd.read_sql_query(SQLQuery, conn)
        df.to_csv('testInfo.csv')
        print(df)

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
    args = pargse_args()
    read(args)
    os.system("PAUSE")


if __name__ == "__main__":
    main()