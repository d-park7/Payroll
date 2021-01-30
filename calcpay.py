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
    parser.add_argument(
        "-i",
        "--employee_id",
        type=int,
        required=True,
        help="Employee specific ID"
    )
    parser.add_argument(
        "-f",
        "--firstday",
        type=str,
        required=True,
        help="Starting date to calculate pay"
    )
    parser.add_argument(
        "-l",
        "--lastday",
        type=str,
        required=True,
        help="Ending date to calculate pay"
    )
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


def calculate_pay(employee_id: int, start_date: str, end_date:str, df_employee, df_record, df_pay):
    """ Calculates daily pay from data in the database
    
    :param start_date, end_date, df_employee, df_record, df_pay:
    :return wage:
    """
    df_merged = df_pay.merge(df_record, how='inner', on=['EmployeeId', 'Date'])

    # Getting employee's first + last name based on id
    selected_row = df_employee.loc[df_employee['EmployeeId'] == employee_id]
    first_name = selected_row['FirstName'][0]
    last_name = selected_row['LastName'][0]

    # Date worked and time in & out
    df_merged.Date = pd.to_datetime(df_merged.Date)
    df_merged.TimeIn = pd.to_datetime(df_merged.TimeIn)
    df_merged.TimeOut = pd.to_datetime(df_merged.TimeOut)

    # Dates inputted by user to calculate
    first_date = pd.to_datetime(start_date, format="%Y-%m-%d")
    last_date = pd.to_datetime(end_date, format="%Y-%m-%d")
    
    # Checks if the worked dates fall between the selected start and end date. Also check if employee id matches
    # NOTE: Using binary (&) operator to make comparison between datetime.timestamp and datetime64
    #  - Returns a parallel dataframe with true/false that show if the row in df_merged matches
    mask = ((df_merged.Date >= first_date) & (df_merged.Date <= last_date)) & (df_merged.EmployeeId == employee_id)
    df_merged = df_merged.loc[mask]

    # Calculate total wage for employee
    df_wage = ((df_merged.TimeOut- df_merged.TimeIn).dt.seconds / 3600) * df_merged.PayPerHour
    return df_merged, df_wage.sum()


def main():
    args = parse_args()

    query_employee = "SELECT * FROM Employee"
    query_record = "SELECT * FROM Record"
    query_pay = "SELECT * FROM Pay"
    df_employee = create_dataframe(args.dbname, query_employee)
    df_record = create_dataframe(args.dbname, query_record)
    df_pay = create_dataframe(args.dbname, query_pay)

    df_merged, wage = calculate_pay(args.employee_id, args.firstday, args.lastday, df_employee, df_record, df_pay)
    print(f'df_merged: \n{df_merged}\n===================')
    print(f'wage: ${wage:.2f}')

if __name__ == "__main__":
    main()
