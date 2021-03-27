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


def merge_dataframes(employee_id: int, start_date: str, end_date:str, df_employee, df_record, df_pay):
    """
    Merges all of the dataframes into one manageable dataframe with the necessary information
    Assumptions: Times are in order for each given date

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
    :return df_merged:
    :rtype df_merged: pandas.dataframe
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

    df_merged = df_pay.merge(df_record, how='inner', on=['EmployeeId', 'Date'])
    df_merged.Date = pd.to_datetime(df_merged.Date)
    df_merged.TimeIn = pd.to_datetime(df_merged.TimeIn)
    df_merged.TimeOut = pd.to_datetime(df_merged.TimeOut)

    first_date = pd.to_datetime(start_date, infer_datetime_format=True)
    last_date = pd.to_datetime(end_date, infer_datetime_format=True)

    # Checks if the worked dates fall between the selected start and end date. Also check if employee id matches
    # NOTE: Using binary (&) operator to make comparison between datetime.timestamp and datetime64
    #  - Returns a parallel dataframe with true/false that show if the row in df_merged matches
    mask = ((df_merged.Date >= first_date) & (df_merged.Date <= last_date)) & (df_merged.EmployeeId == employee_id)
    df_merged = df_merged.loc[mask]
    print(pd.__version__)
    #df_merged = df_merged.sort_values(by='Date', ignore_index=True)
    print(df_merged)

    df_merged['HoursWorked'] = (df_merged.TimeOut - df_merged.TimeIn).dt.seconds / 3600
    df_merged['WeekNumber'] = df_merged.Date.dt.isocalendar().week
    # df_merged['DayNumber'] = df_merged.Date.dt.weekday
    print(df_merged)
    print(df_merged.groupby(by=['Date']))

    return df_merged


# def validate_userinput(df_merged):
#     """
#     Checks to see if the user inputted data is in a weekly format and reformates if not
#     """
#     if df_merged.iloc[-1].DayNumber != 6:
#         week_number = df_merged.iloc[-1].WeekNumber
#         mask = (df_merged.WeekNumber == week_number)
#         print(df_merged.loc[week_number])

#     return df_merged


def calculate_overtime(df_merged, regular_hours_limit: int):
    """
    Calculates the overtime pay if necessary. Overtime is given if the weekly hours exceed 40.
    Overtime pay is 1.5 * normal pay.
    
    :param df_merged: the merged dataframe of pay and record dataframes
    :type df_merged: pandas.Dataframe
    :param regular_hours_limit: number of hours before overtime begins
    :type regular_hours_limit: int
    :return wage: the calculated total wage
    :rtype wage: numpy.float64
    """
    df_hours_worked = (df_merged.TimeOut - df_merged.TimeIn).dt.seconds / 3600

    if df_hours_worked.sum() > regular_hours_limit:
        # Locates the index where regular hour limit <= hours worked
        overtime_index = pd.Index(df_hours_worked.cumsum()).get_loc(regular_hours_limit, "pad")
        df_regular_pay = df_hours_worked.loc[:overtime_index] * df_merged.PayPerHour.loc[:overtime_index]
        hours_overtime = df_hours_worked.sum() - regular_hours_limit

        # Splits the index that contains both regular hours and overtime hours
        split_regular_time = regular_hours_limit - df_hours_worked.loc[:overtime_index].sum()
        split_overtime = df_hours_worked.loc[overtime_index+1] - split_regular_time

        end_index = len(df_hours_worked.index)
        df_overtime_wage = df_merged.PayPerHour.iloc[overtime_index + 1:end_index] * 1.5

        wage = df_regular_pay.sum() + (split_regular_time * df_merged.PayPerHour.loc[overtime_index + 1])
        wage += split_overtime * df_merged.PayPerHour.loc[overtime_index+1] * 1.5
        wage += (df_hours_worked.iloc[overtime_index+2:end_index] * df_overtime_wage).sum()

    return wage
    

def calculate_pay(df_merged):
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
    regular_hours_limit = 20 

    df_hours_worked_by_week = df_merged.groupby(by=['WeekNumber'], as_index=False)['HoursWorked'].sum()
    print('\n', df_hours_worked_by_week)

    values = df_hours_worked_by_week.HoursWorked > regular_hours_limit
    print(values)

    df_hours_worked_by_week['HoursOvertime'] = df_hours_worked_by_week.HoursWorked - regular_hours_limit
    df_hours_worked_by_week[df_hours_worked_by_week < 0] = 0
    print(df_hours_worked_by_week)
    # outcome = df_merged.groupby(pd.Grouper(key='Date', freq='1W')).HoursWorked.sum()
    # print(outcome)
    # Assume that the user only is given the option of calculating the pay over a biweekly period
    # meaning that calcpay function does not need to take into account the number of weeks
    # Currently set to 20 instead of 40 for easier testing purposes    
    
    # if df_hours_worked_by_week.HoursWorked >= regular_hours_limit:
    #     wage = calculate_overtime(df_merged, regular_hours_limit)
    # else:
    #     wage = ((df_merged.TimeOut - df_merged.TimeIn).dt.seconds / 3600) * df_merged.PayPerHour
    #     wage = wage.sum()

    wage = (df_hours_worked_by_week.HoursWorked - df_hours_worked_by_week.HoursOvertime) * df_merged.PayPerHour

    return wage


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

    df_merged = merge_dataframes(args.employee_id, args.firstday, args.lastday, df_employee, df_record, df_pay)
    # validate_userinput(df_merged)
    wage = calculate_pay(df_merged)
    
    logging.info(f"wage: ${wage:.2f}")
    logging.info("Ended\n================")


if __name__ == "__main__":
    main()