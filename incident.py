import pandas as pd
crimes_data = pd.read_csv('USCcrimes.csv', encoding='latin1')
crimes_data.fillna('N/A', inplace=True)

import mysql.connector as msql
from mysql.connector import Error
try:
    conn = msql.connect(host='localhost', user='root',password='Vincenzo!98')
    if conn.is_connected():
        cursor = conn.cursor()
        cursor.execute("CREATE DATABASE USCIncidents")
        print("Database is created")
except Error as e:
    print("Error while connecting to MySQL", e)
