#!/usr/bin/env python3

from sqlalchemy import create_engine
import pandas as pd
import sqlite3

def add_data():
    """Connect to the database"""
    engine = create_engine(f"sqlite:///test.db")
    conn = engine.connect()
    """Add test data"""
    df = pd.DataFrame([(1, "John", "Doe")], columns = ["EmployeeId", "FirstName", "LastName"])
    df.to_sql("Employee", con=engine, if_exists="append")
    conn.commit()
    conn.close()

def main():
    """Driver function"""
    add_data()

if __name__ == "__main__":
    main()