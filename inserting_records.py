import mysql.connector as msql
from mysql.connector import Error
import incident 
try:
    conn = msql.connect(host='localhost', database='USCIncidents', user='root', password='Vincenzo!98')
    if conn.is_connected():
        cursor = conn.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("You're connected to database: ", record)
        cursor.execute('DROP TABLE IF EXISTS incident_data;')
        print('Creating table....')
# in the below line please pass the create table statement which you want #to create
        cursor.execute("CREATE TABLE incident_data(Alert_index varchar(255),Crime varchar(255),Date varchar(255),Weekday varchar(255),Location varchar(255))")
        print("Table is created....")
        #loop through the data frame
        for i,row in incident.crimes_data.iterrows():
            #here %S means string values
            sql = "INSERT INTO USCIncidents.incident_data VALUES (%s,%s,%s,%s,%s)"
            cursor.execute(sql, tuple(row))
            print("Record inserted")
            # the connection is not auto committed by default, so we must commit to save our changes
            conn.commit()
except Error as e:
            print("Error while connecting to MySQL", e)
