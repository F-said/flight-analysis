import psycopg2
import pandas as pd
import numpy as np
from config import params

conn = psycopg2.connect(**params)

cursor = conn.cursor()
cursor.execute("SELECT * FROM real_flight WHERE '0'=cancelled and '0'=diverted;")
rows = cursor.fetchall()

cursor.close()

df = pd.DataFrame(rows, columns=[desc.name for desc in cursor.description])

# check for null values
print(df.isna().sum())

df["delayed"] = np.where(((df["arr_del15"] == '1') | (df["dep_del15"] == '1')), 1, 0)

# group by airline and compute the average ratio of delays
grouped_airline = df.groupby("op_unique_carrier")["delayed"].mean()

# df is sorted by delays
sorted_airlines = grouped_airline.sort_values()

# save to csv
sorted_airlines.to_csv("airline_delays.csv")

# make groups of ratios by airport
grouped_airport = df.groupby("origin")["delayed"].mean()

# df is sorted by delays
sorted_airport = grouped_airport.sort_values()

# save to csv
sorted_airport.to_csv("airport_delays.csv")