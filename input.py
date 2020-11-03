#!/usr/bin/env python3

import sqlite3

conn = sqlite3.connect("payclock.db")
cursor = conn.cursor()

cursor.execute("INSERT INTO Employee VALUES (1, 'John', 'Doe')")
cursor.execute("INSERT INTO Record VALUES (1, '2020-01-01 08:00:00', '2020-01-01 17:00:00')")
cursor.execute("INSERT INTO Pay VALUES (1, 10, '2020-01-01', '2020-01-15')")

# commit the changes
conn.commit()

# close the connection
conn.close()
