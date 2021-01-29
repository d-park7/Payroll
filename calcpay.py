#!/usr/bin/env python3

from initdb import add_filename_extension
import argparse
import sqlite3
import datetime
import pandas as pd
import os
import sys


def parse_args():
    parser = argparse.ArgumentParser(description="Read from the database")
    parser.add_argument(
        "-n",
        "--dbname",
        type=str,
        required=True,
        help="Name of db file")

    args = parser.parse_args()
    return args


def create_dataframe(db_name: str, sql_query: str):
    """
    Creates dataframe to hold data
    :param db_name:
    :return df:
    """
    db_name = add_filename_extension(db_name)
    conn = sqlite3.connect(db_name)
    df = pd.read_sql(sql_query, conn)
    conn.close()
    return df


def calculate_pay(df_record, df_pay):
    """
    Calculates daily pay from data in the database
    :param df_record, df_pay:
    :return df_record:
    """
    times_in = pd.Series(df_record["DateTimeIn"])
    times_out = pd.Series(df_record["DateTimeOut"])
    df_record["DateTimeIn"] = pd.to_datetime(df_record["DateTimeIn"])
    df_record["DateTimeOut"] = pd.to_datetime(df_record["DateTimeOut"])

    hours_worked = (df_record["DateTimeOut"] - df_record["DateTimeIn"]).dt.seconds / 3600
    df_record["DailyWage"] = df_pay["PayPerHour"] * hours_worked
    
    return df_record


# this function currently doesn't do what it needs to do... idky its not working
def update_database_daily_wage(df_record, db_name: str):
    conn = sqlite3.connect(db_name)
    curr = conn.cursor()
    curr.execute(
        f'UPDATE Record SET DailyWage = "{df_record.DailyWage}" WHERE RecordId = "{df_record.RecordId}"'
    )
    conn.commit()
    conn.close()


def main():
    args = parse_args()

    query_record = "SELECT * FROM Record"
    query_pay = "SELECT * FROM Pay"
    df_record = create_dataframe(args.dbname, query_record)
    df_pay = create_dataframe(args.dbname, query_pay)

    df_record = calculate_pay(df_record, df_pay)
    print(df_record)
    update_database_daily_wage(df_record, args.dbname)


if __name__ == "__main__":
    main()
