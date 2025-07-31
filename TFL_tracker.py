import streamlit as st
import requests

# ---- CONFIG ----
BASE_URL = "https://api.tfl.gov.uk"

st.title("🚇 TfL Tube Status Tracker")
st.write("A simple Streamlit app to get current London Underground line status.")

# Step 1: Get available Tube lines
@st.cache_data
def get_tube_lines():
    url = f"{BASE_URL}/Line/Mode/tube"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return []

lines = get_tube_lines()

# Step 2: Let user select a line
line_names = [line["name"] for line in lines]
selected_line = st.selectbox("Select a Tube Line", line_names)

# Step 3: Fetch and display status
@st.cache_data
def get_line_status(line_id):
    url = f"{BASE_URL}/Line/{line_id}/Status"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return []

# Find the ID of the selected line
line_id = next((line["id"] for line in lines if line["name"] == selected_line), None)

if line_id:
    status_data = get_line_status(line_id)
    if status_data:
        line_status = status_data[0]["lineStatuses"][0]["statusSeverityDescription"]
        reason = status_data[0]["lineStatuses"][0].get("reason", "No additional info.")
        st.subheader(f"{selected_line} Line Status: {line_status}")
        st.write(reason)
    else:
        st.error("Could not fetch status.")