import streamlit as st
import pandas as pd
import numpy as np

from shapely.geometry import Point, Polygon
#import geopandas as gpd
import geopy
import geocoder

from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

from streamlit_option_menu import option_menu

import streamlit.components.v1 as html
from  PIL import Image

import plotly.express as px
import io

import pydeck as pdk

from streamlit_folium import folium_static
import folium

import datetime
import sqlite3


# connect to database
crimes_data = pd.read_csv('USCcrimes.csv', encoding='latin1')
crimes_data.fillna('N/A', inplace=True)
crimes_data.replace(to_replace =["Date"],
                            value ="To_Date")
crimes_data_df = pd.DataFrame(crimes_data, columns = ['Crime', 'Date', 'Weekday', 'Location', 'Latitude', 'Longitude'])

conn = sqlite3.connect("data_incident.db")
c = conn.cursor()
print("Successfully Connected to SQLite")

c.execute("DROP TABLE if exists usc_incident_data")
crimes_data_df.to_sql(name='usc_incident_data', con=conn, index = False)
conn.commit()

def view_all_notes():
	c.execute('SELECT * FROM usc_incident_data')
	data = c.fetchall()
	return data

#pd.set_option('display.max_colwidth', None)
#clean_db = pd.DataFrame(view_all_notes(), columns = ['Crime', 'Date', 'Weekday', 'Location', 'Latitude', 'Longitude'])
#st.dataframe(clean_db)

def insertVaribleIntoTable(crime, date, weekday, location, latitude, longitude):
    try:
        #sqliteConnection = sqlite3.connect('data_incident.db')
        #cursor = sqliteConnection.cursor()
        #print("Connected to SQLite")
        conn = sqlite3.connect("data_incident.db")
        c = conn.cursor()

        sqlite_insert_with_param = """INSERT OR IGNORE INTO usc_incident_data
                          (crime, date, weekday, location, latitude, longitude)
                          VALUES (?, ?, ?, ?, ?, ?);"""

        data_tuple = (crime, date, weekday, location, latitude, longitude)
        c.execute(sqlite_insert_with_param, data_tuple)
        conn.commit()
        print("Python Variables inserted successfully into SqliteDb_developers table")
        #result = view_all_notes()
        #st.write(result)

        c.close()

    except sqlite3.Error as error:
        print("Failed to insert Python variable into sqlite table", error)
    finally:
        if conn:
            conn.close()
            print("The SQLite connection is closed")



with st.sidebar:
    choose = option_menu("TrojanMaps", ["About", "Crime Reports", "Crime Map", "Report a Crime", "Emergency Contacts"],
                         icons=['house', 'kanban', 'arrow-90deg-right', 'upload', 'person lines fill'],
                         menu_icon="app-indicator", default_index=0,
                         styles={
        "container": {"padding": "5!important", "background-color": "#fafafa"},
        "icon": {"color": "gold", "font-size": "25px"},
        "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "crimson"},
    }
    )

logo = Image.open(r'trojan.png')
profile = Image.open(r'usclogo.png')
if choose == "About":
    col1, col2 = st.columns( [0.8, 0.2])
    with col1:               # To display the header text using css style
        st.markdown(""" <style> .font {
        font-size:35px ; font-family: 'Cooper Black'; color: #FF9633;}
        </style> """, unsafe_allow_html=True)
        st.markdown('<p class="font">About TrojanMaps</p>', unsafe_allow_html=True)
    with col2:               # To display brand log
        st.image(logo, width=100 )

    st.write("TrojanMaps is an app you can use to be more aware of crimes happening around you.\n")

    st.write("Use the **Crime Reports** tab to check regularly updated crime data by day, month, year and more!\n")
    st.write("Use the **Crime Map** tab to input your currect location or a location you are planning on going around campus to see the recent crimes that have occured in those areas. \n")
    st.write("Use the **Report a Crime** tab to submit crime reports which will be added to our database and displayed on the Crime Map once submitted!\n")
    st.write("Use the **Emergency Contacts** tab to find helpful phone numbers and resources in case of an emergency or any time you feel you are in an unsafe situation.")

    st.write("Created By: Karolina Michalewska, Zahin Roja, Jack Weyer")
    st.image(profile, width=500 )

crimeDaily = Image.open(r'crimeDaily.png')
crimeType = Image.open(r'crimeType.png')
crimeYearly = Image.open(r'crimeYearly.png')
crimeMonthly = Image.open(r'crimeMonths.png')
if choose == "Crime Reports":
    col1, col2 = st.columns( [0.8, 0.2])
    with col1:               # To display the header text using css style
        st.markdown(""" <style> .font {
        font-size:35px ; font-family: 'Cooper Black'; color: #FF9633;}
        </style> """, unsafe_allow_html=True)
        st.markdown('<p class="font">USC Crime Reports</p>', unsafe_allow_html=True)
    with col2:               # To display brand log
        st.image(logo, width=100 )


    st.markdown(""" <style> .graphs {
    font-size:25px ; font-family: 'Cooper Black'; color: #FF9633;}
    </style> """, unsafe_allow_html=True)
    st.markdown('<p class="graphs">Crime Types</p>', unsafe_allow_html=True)
    #st.markdown('<p class="font">Crime Types</p>', unsafe_allow_html=True)
    st.image(crimeType, width=600 )
    st.write("**Rape, drug violations, and burglary are the most common crime reports at the USC University Park campus according to the 2021 Annual Security & Fire Safety Report.**")
    st.markdown('<p class="graphs">Crime By Day</p>', unsafe_allow_html=True)
    st.image(crimeDaily, width=600 )
    st.write("**More crime alerts occur on Saturday than any other day of the week.**")
    st.markdown('<p class="graphs">Crime By Month</p>', unsafe_allow_html=True)
    st.image(crimeMonthly, width=600 )
    st.write("**The number of crime alerts reported by the Department of Public Safety follows a cyclical pattern, with outliers in April, August, and November.**")
    st.markdown('<p class="graphs">Crime By Year</p>', unsafe_allow_html=True)
    st.image(crimeYearly, width=600 )
    st.write("**The University Park campus averaged over 400 reported offenses per year from 2017-2020.**")

if choose == "Crime Map":
    col1, col2 = st.columns( [0.8, 0.2])
    with col1:               # To display the header text using css style
        st.markdown(""" <style> .font {
        font-size:35px ; font-family: 'Cooper Black'; color: #FF9633;}
        </style> """, unsafe_allow_html=True)
        st.markdown('<p class="font">Crime Map</p>', unsafe_allow_html=True)
    with col2:               # To display brand log
        st.image(logo, width=80 )


    with st.form(key='columns_in_form2',clear_on_submit=True):
        start_street=st.text_input(label='Please Enter Your Current Location To View Reported Crimes Near You')
        submitted = st.form_submit_button('Submit')
        if submitted:
            st.write('Reported Crimes Near You.')

            city = "Los Angeles"
            state = "California"
            country = "USA"

            geolocator = Nominatim(user_agent="GTA Lookup")
            geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
            start_location = geolocator.geocode(start_street+", "+city+", "+state+", "+country)

            start_lat = start_location.latitude
            start_lon = start_location.longitude
            start_latlng = (start_lat, start_lon)

            m = folium.Map(location=[start_lat, start_lon], zoom_start=17)

            tooltip = "You Are Here"
            folium.Marker(
                [start_lat, start_lon], popup= "You Are Here", tooltip=tooltip, icon=folium.Icon(color='red')).add_to(m)

            #output a map with all crimes in database
            #data = view_all_notes()
            #df_data = pd.read_sql(data)
            all_crime = pd.read_sql_query('select Crime, Date, Latitude, Longitude from usc_incident_data', conn)

            #map_lat_lon = pd.read_sql_query('select Latitude, Longitude from usc_incident_data', conn)
            all_crime.rename(columns={'Latitude': 'lat', 'Longitude': 'lon'}, inplace=True)
            #map_lat_lon.astype({'lat':'float','lon':'float'})
            #map_lat_lon.to_csv('map_lat_lon.csv')
            all_crime['lat'].astype(float)
            all_crime['lon'].astype(float)

            #st.map(map_lat_lon, zoom = 15)

            for (index, row) in all_crime.iterrows():
                lat = row['lat']
                lon = row['lon']
                tooltip = row['Crime']
                popup = row['Crime'], row['Date']
                print(row['lat'])
                folium.Marker(
                    [lat, lon], popup= popup, tooltip=tooltip, icon=folium.Icon(color='blue')).add_to(m)
            folium_static(m)


if choose == "Report a Crime":

    col1, col2 = st.columns( [0.8, 0.2])
    with col1:               # To display the header text using css style
        st.markdown(""" <style> .font {
        font-size:35px ; font-family: 'Cooper Black'; color: #FF9633;}
        </style> """, unsafe_allow_html=True)
        st.markdown('<p class="font">Report a Crime</p>', unsafe_allow_html=True)
    with col2:               # To display brand log
        st.image(logo, width=80 )

    with st.form(key='columns_in_form2',clear_on_submit=True):
        #result = view_all_notes()
        #st.write(result)
        crime_type = st.selectbox('Type of Crime',
        ('Rape', 'Drug Violation', 'Burglary', 'Robbery', 'Liquor Law Violation',
        'Motor Vehicle Theft', 'Fondling', 'Aggravated Assault', 'Stalking',
        'Dating Violance', 'Domestic Violence', 'Weapons Violation', 'Statutory Rape', 'Other'))
        #other_crime = st.text_input(label = 'If you selected other please enter the crime type below.')

        crime_date = st.date_input("Date of Crime")
        crime_time=st.time_input('Time of Crime')
        crime_location = st.text_input(label = 'Crime Location (please enter the street address of where the crime occured)')
        submitted = st.form_submit_button('Submit')
        #derive weekday, lat, lon
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        crime_weekday = days[crime_date.weekday()]

        city = "Los Angeles"
        state = "California"
        country = "USA"

        geolocator = Nominatim(user_agent="GTA Lookup")
        geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
        crime_location_finder = geolocator.geocode(crime_location+", "+city+", "+state+", "+country)

        crime_lat = crime_location_finder.latitude
        crime_lon = crime_location_finder.longitude
        crime_latlng = (crime_lat, crime_lon)


        if submitted:
            st.write('Thank you, the crime report has been submitted!')
            insertVaribleIntoTable(crime_type, crime_date, crime_weekday, crime_location, crime_lat, crime_lon)
            # send input data to database!!!!


if choose == "Emergency Contacts":
    col1, col2 = st.columns( [0.8, 0.2])
    with col1:               # To display the header text using css style
        st.markdown(""" <style> .font {
        font-size:35px ; font-family: 'Cooper Black'; color: #FF9633;}
        </style> """, unsafe_allow_html=True)
        st.markdown('<p class="font">Emergency Contacts</p>', unsafe_allow_html=True)
    with col2:               # To display brand log
        st.image(logo, width=100 )

    st.write("If you feel you are in any type of danger please call one of the following numbers.")
    st.write("USC Public Safety: (213) 740-6000")
    st.write("Non-Emergency Los Angeles Police Department: (213) 485-2582")
    st.write("For any life threatening emergencies please call the emergency line of the Los Angeles Police Department: 911")
    st.image(profile, width=500 )
