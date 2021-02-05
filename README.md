# Payroll
A payroll program that lets employees clock in and out and then calculates a biweekly paycheck based on the times and wage.

TO USE THIS:
1. First initialize your database with the initdb.py file.
2. Put in the test information with testinput.py.
3. Calculate the pay with calcpay.py.

# Payroll

This program calculates a given employee's wages from 2 selected dates.

### File description
initdb.py - Initializes the database tables.
 - Create the Employee, Pay, and Record tables.

testinput.py - Loads the db tables with test data

calcpay.py - Calculates wages for a specific employee during a time period.

## Setup
1. Download Docker desktop (verify your installation using "docker -v")
2. For windows: Download and enable WSL 2 

## Usage
1. Clone project to desired directory (or download .zip and extract)
2. Navigate to directory where .py files are located
3. Run the following commands:
  - **docker-compose build** (this will take a bit for the first time)
  - **docker-compose up** (This will start the container)
4. In your browser, open up **localhost:5000** (You should be able to see some text)

## Features
1. Run the following commands (if you want):
  - python calcpay.py -n payroll.db -i \<employee-id\> -f \<start-date\> -l \<end-date\>
  
Note: \<start-date\> and \<end-date\> format: 'YYYY-MM-DD'

## Additional Notes

You may need to run: 

- pip install pandas
