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
#import cv2
#from st_aggrid import AgGrid
import plotly.express as px
import io



with st.sidebar:
    choose = option_menu("TrojanMaps", ["About", "Crime Reports", "Find a Route", "Emergency Contacts"],
                         icons=['house', 'kanban', 'arrow-90deg-right', 'person lines fill'],
                         menu_icon="app-indicator", default_index=0,
                         styles={
        "container": {"padding": "5!important", "background-color": "#fafafa"},
        "icon": {"color": "gold", "font-size": "25px"},
        "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "crimson"},
    }
    )

logo = Image.open(r'/Users/karolinamichalewska/Documents/DSCI551/final_project/trojan.png')
profile = Image.open(r'/Users/karolinamichalewska/Documents/DSCI551/final_project/usclogo.png')
if choose == "About":
    col1, col2 = st.columns( [0.8, 0.2])
    with col1:               # To display the header text using css style
        st.markdown(""" <style> .font {
        font-size:35px ; font-family: 'Cooper Black'; color: #FF9633;}
        </style> """, unsafe_allow_html=True)
        st.markdown('<p class="font">About TrojanMaps</p>', unsafe_allow_html=True)
    with col2:               # To display brand log
        st.image(logo, width=100 )

    st.write("TrojanMaps is an app you can use to find the safest routes from one destination to another around the USC campus!")
    st.write("*** Add a more detailed app description!")
    st.write("Created By: Karolina Michalewska, Zahin Roja, Jack Weyer")
    st.image(profile, width=500 )

crimeDaily = Image.open(r'/Users/karolinamichalewska/Documents/DSCI551/final_project/crimeDaily.png')
crimeType = Image.open(r'/Users/karolinamichalewska/Documents/DSCI551/final_project/crimeType.png')
crimeYearly = Image.open(r'/Users/karolinamichalewska/Documents/DSCI551/final_project/crimeYearly.png')
crimeMonthly = Image.open(r'/Users/karolinamichalewska/Documents/DSCI551/final_project/crimeMonthly.png')
if choose == "Crime Reports":
    col1, col2 = st.columns( [0.8, 0.2])
    with col1:               # To display the header text using css style
        st.markdown(""" <style> .font {
        font-size:35px ; font-family: 'Cooper Black'; color: #FF9633;}
        </style> """, unsafe_allow_html=True)
        st.markdown('<p class="font">USC Crime Reports</p>', unsafe_allow_html=True)
    with col2:               # To display brand log
        st.image(logo, width=100 )

    st.write("Crime Types")
    st.image(crimeType, width=600 )
    st.write("Crime by Day")
    st.image(crimeDaily, width=600 )
    st.write("Crime by Month")
    st.image(crimeMonthly, width=600 )
    st.write("Crime by Year")
    st.image(crimeYearly, width=600 )

if choose == "Find a Route":
    col1, col2 = st.columns( [0.8, 0.2])
    with col1:               # To display the header text using css style
        st.markdown(""" <style> .font {
        font-size:35px ; font-family: 'Cooper Black'; color: #FF9633;}
        </style> """, unsafe_allow_html=True)
        st.markdown('<p class="font">Find a Route</p>', unsafe_allow_html=True)
    with col2:               # To display brand log
        st.image(logo, width=80 )

    with st.form(key='columns_in_form2',clear_on_submit=True):
        start_street=st.text_input(label='Please Enter Your Current Location')
        end_street=st.text_input(label='Please Enter Your Destination')
        submitted = st.form_submit_button('Search')
        if submitted:
            st.write('According to recent crime reports, the following is the safest route to your destination!')

    city = "Los Angeles"
    state = "California"
    country = "USA"

    geolocator = Nominatim(user_agent="GTA Lookup")
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
    location = geolocator.geocode(start_street+", "+city+", "+state+", "+country)

    g = geocoder.ip('me')
    print(g.latlng)

    lat = location.latitude
    lon = location.longitude

    map_data = pd.DataFrame({'lat': [lat], 'lon': [lon]})
    st.map(map_data, zoom = 15)

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
