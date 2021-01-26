#!/usr/bin/env python3

import argparse
import sqlite3
import datetime
import pandas as pd
import sqlalchemy
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
        "--calculate",
        action="store_true",
        help="Calculate the pay based on the time in and time out"
    )
    parser.add_argument(
        "-v",
        "--csvname",
        type=str,
        help="Name of csv file to read"
    )

    args = parser.parse_args()
    return args


def calculate_pay(args):
    """
    Calculates data from the database
    :param args:
    :return sqlite3 connection:
    """
    db_name = add_filename_extension(args.dbname, "db")

    if args.csvname:
        csv_name = add_filename_extension(args.csvname, "csv")
        df = read_csv_name(db_name, csv_name)
    else:
        conn = sqlite3.connect(db_name)
        SQLQuery = 'SELECT * FROM Record'
        sqlquery2 = "SELECT * FROM Pay"
        df = pd.read_sql_query(SQLQuery, conn)
        df2 = pd.read_sql_query(sqlquery2, conn)
    

    if args.calculate:
        times_in = pd.Series(df["DateTimeIn"])
        times_out = pd.Series(df["DateTimeOut"])
        df["DateTimeIn"] = pd.to_datetime(df["DateTimeIn"])
        df["DateTimeOut"] = pd.to_datetime(df["DateTimeOut"])
        hours_worked = (df["DateTimeOut"] - df["DateTimeIn"]).dt.seconds / 3600
        # insert the hours worked into the DailyWage column in table Record
        df["DailyWage"] = df2["PayPerHour"] * hours_worked
        print(df)
        # create an sqlalchemy for easier connections
        engine = sqlalchemy.create_engine("sqlite:///{}".format(db_name), echo=False)
        # replace the old Records table with the new Records dataframe in the db
        df.to_sql("Record", con=engine, if_exists="replace", index=False)


def read_csv_name(db_name: str, csv_name: str):
    """
    Reads the csv file and converts it into a dataframe format
    :param csv_name:
    :return df:
    """
    # try to connect to the named db
    # if it does not eist quit the program
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

    # accept a csv file name and then put the csv into a dataframe using pandas
    conn = sqlite3.connect(db_name)
    df = pd.read_csv(csv_name)
    conn.close()
    return df


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
    args = parse_args()
    calculate_pay(args)


if __name__ == "__main__":
    main()
