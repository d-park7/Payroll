#!/usr/bin/env python3

import argparse
import sqlite3
import datetime
import pandas as pd
import os


def parse_args():
    # argument parser
    parser = argparse.ArgumentParser(description="Read from the inputted database")
    parser.add_argument(
        "-d",
        "--dbname",
        type=str,
        required=True,
        help="Name of db file")
    parser.add_argument(
        "-c",
        "--csvname",
        type=str,
        required=True,
        help="Name of csv file to read"
    )

    args = parser.parse_args()
    return args


def calculate_pay(args):
    """
    Calculates data from the database
    :param db_name:
    :return sqlite3 connection:
    """
    # try to connect to the named db
    # if it does not eist quit the program
    db_name = add_filename_extension(args.dbname)
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

    if args.csvname:
        # accept a csv file name and then put the csv into a dataframe using pandas
        csv_name = args.csvname
        conn = sqlite3.connect(db_name)
        df = pd.read_csv(csv_name)
        # isolate the DateTimeIn/DateTimeOut columns from the df and change the objects into a datetime variable type
        df['DateTimeIn'] = pd.to_datetime(df.DateTimeIn)
        df['DateTimeOut'] = pd.to_datetime(df.DateTimeOut)
        print(df)
        print(df.dtypes)
        print("time in hours: ", df.DateTimeIn.dt.hour)
        print("time out hours: ", df.DateTimeOut.dt.hour)
        
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
    calculate_pay(args)
    input()


if __name__ == "__main__":
    main()