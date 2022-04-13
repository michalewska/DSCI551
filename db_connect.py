import pandas as pd
import streamlit as st 
import sqlite3

crimes_data = pd.read_csv('USCcrimes.csv', encoding='latin1')
crimes_data.fillna('N/A', inplace=True)
crimes_data.replace(to_replace =["Date"], 
                            value ="To_Date")
crimes_data_df = pd.DataFrame(crimes_data, columns = ['Crime', 'Date', 'Weekday', 'Location', 'Latitude', 'Longitude'])

conn = sqlite3.connect("data_incident.db")
c = conn.cursor()
''''''
c.execute("DROP TABLE if exists usc_incident_data")
crimes_data_df.to_sql(name='usc_incident_data', con=conn, index = False)



def view_all_notes():
	c.execute('SELECT * FROM usc_incident_data')
	data = c.fetchall()
	return data

def main():
	result = view_all_notes()
	st.write(result)

	pd.set_option('display.max_colwidth', None)
	clean_db = pd.DataFrame(view_all_notes(), columns = ['Crime', 'Date', 'Weekday', 'Location', 'Latitude', 'Longitude'])
	st.dataframe(clean_db)

if __name__ == '__main__':
	main()
