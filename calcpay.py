#!/usr/bin/env python3

from initdb import add_filename_extension
import argparse
import sqlite3
import datetime
import pandas as pd
import os
import sys
import logging


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
        help="Starting date to calculate pay with format: year-month-date ex: 2021-01-15"
    )
    parser.add_argument(
        "-l",
        "--lastday",
        type=str,
        required=True,
        help="Ending date to calculate pay with format: year-month-date ex: 2021-01-15"
    )
    args = parser.parse_args()
    return args


def sql_to_dataframe(db_name: str, sql_query: str):
    """ 
    Return the created dataframe from the sqlite3 table.
    """
    db_name = add_filename_extension(db_name)
    conn = sqlite3.connect(db_name)
    df = pd.read_sql(sql_query, conn)
    conn.close()
    return df


def calculate_pay(employee_id: int, start_date: str, end_date:str, df_employee, df_record, df_pay):
    """ 
    Calculates employee pay from chosen data form the database.
    
    :param employee_id: the employee's id
    :type employee_id: int
    :param start_date: the date you want to calculate the employee's pay from (inclusive)
    :type start_date: string
    :param end_date: the date you want to calculate the employee's pay to (inclusive)
    :type end_date: string
    :df_record: a dataframe of the Record table from the databse
    :df_employee: created dataframe of the Employee table
    :df_pay: created dataframe of the Pay table
    :return df_merged: the merged dataframe of the calculated daily wages from df_pay and df_record 
    :rtype df_merged: pandas.dataframe (for debugging purposes)
    :return df_wage.sum(): the total wage for the employee from the chosen dates
    :rtype df_wage.sum(): numpy.float64
    """
    df_merged = df_pay.merge(df_record, how='inner', on=['EmployeeId', 'Date'])

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
    df_wage = ((df_merged.TimeOut - df_merged.TimeIn).dt.seconds / 3600) * df_merged.PayPerHour
    return df_merged, df_wage.sum()


def main():
    logging.basicConfig(filename="calcpay.log", level=logging.INFO)
    logging.info("Started")
    args = parse_args()

    query_employee = "SELECT * FROM Employee"
    query_record = "SELECT * FROM Record"
    query_pay = "SELECT * FROM Pay"
    df_employee = sql_to_dataframe(args.dbname, query_employee)
    df_record = sql_to_dataframe(args.dbname, query_record)
    df_pay = sql_to_dataframe(args.dbname, query_pay)

    df_merged, wage = calculate_pay(args.employee_id, args.firstday, args.lastday, df_employee, df_record, df_pay)
    logging.info(f'df_merged: \n{df_merged}\n===================')
    logging.info(f'wage: ${wage:.2f}')
    logging.info("Ended")
if __name__ == "__main__":
    main()
