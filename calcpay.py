#!/usr/bin/env python3

from initdb import add_filename_extension
import argparse
import sqlite3
import datetime
import time
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


def convert_db_to_easier_calculations(df_record):
    """
    Changes the record dataframe into one that is more managable to calculate the pay.
    To be used in the calculate_pay function.
    Assumptions: Times are in order for each given date

    :param df_record: the record dataframe from the database
    :type df_record: pandas.Dataframe
    :return df_record: modified record dataframe
    :rtype df_record: pandas.Dataframe
    """
    timein_mask = df_record.TimeInFlag == 1
    timeout_mask = df_record.TimeInFlag == 0
    df_timein = df_record.loc[timein_mask]
    df_timeout = df_record.loc[timeout_mask]

    df_timein.reset_index(inplace=True, drop=True)
    df_timeout.reset_index(inplace=True, drop=True)

    df_record = df_timein.merge(df_timeout, how='inner', on=[df_timeout.index, 'Date', 'EmployeeId'])
    df_record.drop(columns=['TimeInFlag_x', 'TimeInFlag_y', 'key_0'], axis='columns', inplace=True)
    df_record.rename(columns={'Time_x': 'TimeIn', 'Time_y': 'TimeOut'}, inplace=True)
    return df_record


def calculate_pay(employee_id: int, start_date: str, end_date:str, df_employee, df_record, df_pay):
    """ 
    Calculates employee pay from chosen data form the database.
    
    :param employee_id: the employee's id
    :type employee_id: int
    :param start_date: the date you want to calculate the employee's pay from (inclusive)
    :type start_date: string
    :param end_date: the date you want to calculate the employee's pay to (inclusive)
    :type end_date: string
    :param df_employee: created dataframe of the Employee table
    :type df_employee: pandas.Dataframe
    :param df_record: a dataframe of the Record table from the database
    :type df_record: pandas.Dataframe
    :param df_pay: created dataframe of the Pay table
    :type df_pay: pandas.Dataframe
    :return df_wage.sum(): the total wage for the employee from the chosen dates
    :rtype df_wage.sum(): numpy.float64
    """
    df_record = convert_db_to_easier_calculations(df_record)
    df_merged = df_pay.merge(df_record, how='inner', on=['EmployeeId', 'Date'])

    df_merged.Date = pd.to_datetime(df_merged.Date)
    df_merged.TimeIn = pd.to_datetime(df_merged.TimeIn)
    df_merged.TimeOut = pd.to_datetime(df_merged.TimeOut)

    first_date = pd.to_datetime(start_date, format="%Y-%m-%d")
    last_date = pd.to_datetime(end_date, format="%Y-%m-%d")
    
    # Checks if the worked dates fall between the selected start and end date. Also check if employee id matches
    # NOTE: Using binary (&) operator to make comparison between datetime.timestamp and datetime64
    #  - Returns a parallel dataframe with true/false that show if the row in df_merged matches
    mask = ((df_merged.Date >= first_date) & (df_merged.Date <= last_date)) & (df_merged.EmployeeId == employee_id)
    df_merged = df_merged.loc[mask]

    df_wage = ((df_merged.TimeOut - df_merged.TimeIn).dt.seconds / 3600) * df_merged.PayPerHour
    return df_wage.sum()


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
    wage = calculate_pay(args.employee_id, args.firstday, args.lastday, df_employee, df_record, df_pay)
    
    logging.info(f"wage: ${wage:.2f}")
    logging.info("Ended\n================")


if __name__ == "__main__":
    main()
