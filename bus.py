import streamlit as st
import datetime
from suntime import Sun
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
import pytz

# Function to get latitude & longitude of a location
def get_lat_lon(location):
    geolocator = Nominatim(user_agent="geo_locator")
    loc = geolocator.geocode(location)
    if loc:
        return loc.latitude, loc.longitude
    else:
        return None, None

# Function to get sunrise and sunset times for a location
def get_sun_times(lat, lon):
    sun = Sun(lat, lon)
    today = datetime.date.today()
    sunrise = sun.get_sunrise_time().time()  # UTC time
    sunset = sun.get_sunset_time().time()  # UTC time
    return sunrise, sunset

# Function to determine the best seat side
def get_best_seat_side(travel_time, sunrise, sunset):
    try:
        time_obj = datetime.datetime.strptime(travel_time.strip(), "%H:%M").time()

        # Morning: Sun rises in the EAST (sit on LEFT)
        if sunrise <= time_obj < sunset:
            return "LEFT (Sun in the east, avoid glare)"
        else:
            return "RIGHT (Sun in the west, avoid glare)"
    
    except ValueError:
        return "Invalid time format! Please enter time as HH:MM (24-hour format)."

st.title("Best Bus Seating Position Based on Sun Exposure")

from_address = st.text_input("Enter FROM location:")
to_address = st.text_input("Enter TO location:")
travel_time = st.text_input("Enter travel time (HH:MM in 24-hour format):")

if st.button("Find Best Seat"):
    lat, lon = get_lat_lon(from_address)
    if lat and lon:
        # Get sunrise & sunset times
        sunrise, sunset = get_sun_times(lat, lon)

        # Convert sunrise & sunset to local timezone
        tf = TimezoneFinder()
        timezone_str = tf.timezone_at(lng=lon, lat=lat)
        timezone = pytz.timezone(timezone_str)

        sunrise_local = datetime.datetime.combine(datetime.date.today(), sunrise).astimezone(timezone).time()
        sunset_local = datetime.datetime.combine(datetime.date.today(), sunset).astimezone(timezone).time()

        # Get best seat side
        best_seat = get_best_seat_side(travel_time, sunrise_local, sunset_local)

        # Display results
        st.success(f"Traveling from {from_address} to {to_address} at {travel_time}")
        st.info(f"🌅 Sunrise: {sunrise_local} | 🌇 Sunset: {sunset_local}")
        st.success(f"✅ Best seat: Sit on the {best_seat} side of the bus.")
    else:
        st.error("❌ Could not find location. Please enter a valid city or place.")
