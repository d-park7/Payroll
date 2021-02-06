#! /usr/bin/env python3

from initdb import add_filename_extension
import datetime
import argparse
import sqlite3


def parse_args():
    parser = argparse.ArgumentParser(description="Clock in your time and clock out your time")
    parser.add_argument(
        "-n",
        "--dbname",
        type=str,
        required=True,
        help="Name of db file")
    parser.add_argument(
        "-i",
        "--employee_id",
        type=int,
        required=True,
        help="Employee specific ID"
    )
    parser.add_argument(
        "-i",
        "--clockin",
        action="store_true",
        help="Clock in your time"
    )
    parser.add_argument(
        "-o",
        "--clockout",
        action="store_true",
        help="Clock out your time"
    )
    args = parser.parse_args()
    return args


def add_data_to_database(args):
    """
    Adds the clock in and clock out times for the employee into the database.
    """
    db_name = add_filename_extension(args.dbname)

    if args.clockin:
        conn = sqlite.connect(db_name)
        sql_statement = f"INSERT OR IGNORE INTO Record VALUES ({datetime.datetime.today()}, {datetime.datetime.today()}, {datetime.datetime.today()})", 
        conn.execute()
        conn.commit()
        conn.close()
    elif args.clockout:
        conn = sqlite3.connect(db_name)

        conn.commit()
        conn.close()

def main():
    args = parse_args()
    add_data_to_database(args)


if __name__ == "__main__":
    main()