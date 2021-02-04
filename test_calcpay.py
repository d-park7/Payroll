#!/usr/bin/env python3

import unittest
import calcpay
import pandas as pd

class TestCalcPay(unittest.TestCase):

    def test_wage(self):
        employees = {
            "EmployeeId": [1, 2],
            "FirstName": ["John", "Bob"],
            "LastName": ["Doe", "Guy"]
            }
        pay = {
            "EmployeeId": [1, 1, 1, 2, 2, 2], 
            "Date": ["2021-01-01", "2021-01-02", "2021-01-03", "2021-01-01", "2021-01-02", "2021-01-03"], 
            "PayPerHour": [10, 10, 10, 5, 5, 5]
        }
        record = {
            "EmployeeId": [1, 1, 1, 2, 2, 2],
            "Date": ["2021-01-01", "2021-01-02", "2021-01-03", "2021-01-01", "2021-01-02", "2021-01-03"],
            "TimeIn": ["09:00:00", "09:00:00", "09:00:00", "10:00:00", "10:00:00", "10:00:00"],
            "TimeOut": ["05:00:00", "05:00:00", "05:00:00", "06:00:00", "06:00:00", "06:00:00"]
        }
        df_employee = pd.DataFrame.from_dict(employees)
        df_record = pd.DataFrame.from_dict(record)
        df_pay = pd.DataFrame.from_dict(pay)
        result = calcpay.calculate_pay(1, "2021-01-01", "2021-01-02", df_employee, df_record, df_pay)


if __name__ == "__main__":
    unittest.main()