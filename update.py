#!/usr/bin/env python3

import pandas as pd
import sqlite3

conn = sqlite3.connect("payclock.db")
df = pd.read_sql_query("SELECT * FROM 
cursor.execute("DELETE FROM payInfo WHERE id = ?", num)

conn.commit()
conn.close()
