#!/usr/bin/env python3

import argparse
import sqlite3

def init_db(db_name: str):
    """
    One line of what this function

    More detailed info if necessary

    :param db_name:
    :return:
    """
    conn = sqlite3.connect(db_name)

    # verify database is connected
    if conn.total_changes != 0:
        print("Failed to create database.")
        quit()

    # Create the cursor obj
    cursor = conn.cursor()

    # Create the employee info table
    cursor.execute("CREATE TABLE employeeInfo (id int, firstName text, lastName text)")

    # create the records table
    cursor.execute("CREATE TABLE records (id int, dateTimeIn text, dateTimeOut text)")

    # create the pay info table
    cursor.execute("CREATE TABLE payInfo (id int, pay unsigned int, biWeeklyStartDate text, biWeeklyEndDate text)")


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--db-name",
        type=str,
        required=True,
        help="Name of the database you want to connect to"
    )
    # can add more arguments
    return parser.parse_args()


def main():
    args = parse_args()
    init_db(args.db_name)


if __name__ == '__main__':
    main()
