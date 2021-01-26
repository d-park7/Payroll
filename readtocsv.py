#!/usr/bin/env python3

import sqlite3
import argparse
import os
import pandas as pd


def pargse_args():
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
        help="Name of csv file"
    )

    args = parser.parse_args()
    return args


def read_to_csv(args):
    """
    Reads from db to a csv file
    :param db_name:
    :return sqlite3 connection:
    """
    # try to connect to the named db
    # if it does not eist quit the program
    db_name = add_filename_extension(args.dbname, "db")
    csv_name = add_filename_extension(args.csvname, "csv")
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

    conn = sqlite3.connect(db_name)
    # query database for data
    SQLQuery = 'SELECT * FROM Record;'
    # create a dataframe from database using pandas
    df = pd.read_sql_query(SQLQuery, conn)
    df.to_csv(csv_name)

    conn.close()


def add_filename_extension(datafile: str, file_type: str):
    """
    Adds the .db or .csv ext if the name does not contain it
    :param args:
    :return full_file_name:
    """
    if file_type == "db":
        filename, file_extension = os.path.splitext(datafile)
        if file_extension:
            full_file_name = datafile
        else:
            full_file_name = args.dbname + ".db"
    elif file_type == "csv":
        filename, file_extension = os.path.splitext(datafile)
        if file_extension:
            full_file_name = datafile
        else:
            full_file_name = args.csvname + ".csv"
            
    return full_file_name


def main():
    args = pargse_args()
    read_to_csv(args)


if __name__ == "__main__":
    main()
