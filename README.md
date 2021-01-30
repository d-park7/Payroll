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

## Usage
1. Clone project to desired directory (or download .zip and extract)
2. Navigate to directory where .py files are located
3. Run the following commands:
  - python initdb.py -n payroll.db 
  - python testinput.py -n payroll.db
  - python calcpay.py -n payroll.db -i \<employee-id\> -f \<start-date\> -l \<end-date\>
  
Note: \<start-date\> and \<end-date\> format: 'YYYY-MM-DD'

## Additional Notes

You may need to run: 

- pip install pandas