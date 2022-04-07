import mysql.connector as msql
from mysql.connector import Error
try:
    conn = msql.connect(host='localhost', user='root', password='Vincenzo!98')#give ur username, password
    if conn.is_connected():
        cursor = conn.cursor()
        sql="SELECT * FROM USCIncidents.incident_data"
        cursor.execute(sql)
        # Fetch all the records
        result = cursor.fetchall()
        for i in result:
            print(i)
except Error as e:
    print("Error while connecting to MySQL", e)


