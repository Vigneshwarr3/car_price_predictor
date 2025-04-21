import streamlit as st
import requests
import pandas as pd
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

st.title("🚘 Car Price Predictor")
st.markdown("Enter car details and get a predicted selling price.")

#df = pd.read_csv('filter_data.csv')

API_KEY = os.getenv("API_KEY")
API_KEY_NAME = os.getenv("API_KEY_NAME")
# name: key
headers = {API_KEY_NAME: API_KEY}
url = "http://100.90.162.48:10000/get-filtered-data" #change this url to the docker's url
response = requests.get(url, headers=headers)
st.write(response.status_code)
#st.write(response.text)
st.write(response.request.headers)
#st.write(response.request.body)
df = pd.DataFrame(response.json())
st.write(df.head())

# --- Make and Model Dropdown ---
col1, col2, col3 = st.columns(3)
with col1:
    make = st.selectbox("Make", options=list(df['make'].sort_values().unique()))
with col2:
    model_mask = df['make']==make
    model = st.selectbox("Model", options=list(df[model_mask]['model'].sort_values().unique()))
with col3:
    body_mask = model_mask & (df['model']==model)
    bodyType = st.selectbox("Body Type", options=list(df[body_mask]['bodyType'].sort_values().unique()))


with col1:
    fuel_mask = body_mask & (df['bodyType']==bodyType)
    fuelType = st.selectbox("Fuel Type", options=list(df[fuel_mask]['fuelType'].sort_values().unique()))
with col2:
    drive_mask = fuel_mask & (df['fuelType']==fuelType)
    drivetrain = st.selectbox("Drive Train", options=list(df[drive_mask]['driveTrain'].unique()))
with col3:
    seats = st.number_input("No of Seats", df[body_mask]['seats'].min(), df[body_mask]['seats'].max(), value=df[body_mask]['seats'].min())

with col3:
    horsePower = st.slider(
    "Horse Power",
    min_value=int(df[body_mask]['horsePower'].min()),
    max_value=int(df[body_mask]['horsePower'].max())+10,
    value=int(df[body_mask]['horsePower'].min()),
    step=10
)
with col2:
    numOfOwners = st.slider("Number of Previous Owners", 0, 10, value=1)
with col1:
    transmission_mask = drive_mask & (df['driveTrain']==drivetrain)
    transmission = st.selectbox("Transmission", options=list(df[transmission_mask]['transmission'].unique()))

if fuelType in ['Gas', 'Flexible Fuel', 'Diesel']:

    with col1:
        mileage = st.slider("Miles Driven", 0, 500000, value=30000)
    with col2:
        mpgCity = st.slider("MPG City", 0, 200, value=120)
    with col3:
        mpgHighway = st.slider("MPG Highway", 0, 200, value=112)

    evRange, evMpgeCity, evMpgeHighway = 0, 0, 0

elif fuelType in ['Hybrid', 'Plug-In Hybrid']:

    with col1:
        mileage = st.slider("Miles Driven", 0, 500000, value=30000)
    with col2:
        mpgCity = st.slider("MPG City", 0, 200, value=120)
    with col3:
        mpgHighway = st.slider("MPG Highway", 0, 200, value=112)
    
    with col1:
        evRange = st.slider("EV Range (mi)", 0, 600, value=330)
    with col2:
        evMpgeCity = st.slider("EV MPGe City", 0, 150, value=121)
    with col3:
        evMpgeHighway = st.slider("EV MPGe Highway", 0, 150, value=106)

else:

    with col1:
        mileage = st.slider("Miles Driven", 0, 500000, value=30000)
    with col1:
        evRange = st.slider("EV Range (mi)", 0, 600, value=330)
    with col2:
        evMpgeCity = st.slider("EV MPGe City", 0, 150, value=121)
    with col3:
        evMpgeHighway = st.slider("EV MPGe Highway", 0, 150, value=106)
    
    mpgCity, mpgHighway = 0, 0

with col1:
    age = st.slider("Age (years)", 0, 50, value=2)
with col2:
    hasReportedAccident = st.selectbox("Has Reported Accident?", ["True", "False"])
   


# --- Submit Button ---
if st.button("🔍 Predict Price"):
    input_data = {
        "make": make,
        "model": model,
        "bodyType": bodyType,
        "seats": seats,
        "numOfOwners": numOfOwners,
        "fuelType": fuelType,
        "horsePower": horsePower,
        "driveTrain": drivetrain,
        "transmission": transmission,
        "mileage": mileage,
        "mpgCity": mpgCity,
        "mpgHighway": mpgHighway,
        "evRange": evRange,
        "evMpgeCity": evMpgeCity,
        "evMpgeHighway": evMpgeHighway,
        "hasReportedAccident": hasReportedAccident,
        "age": age
    }

    try:
        #res = requests.post("http://100.90.162.48:5000/predict", json=input_data, headers=headers)
        res = requests.post("http://100.90.162.48:10000/predict", json=input_data, headers=headers) # don't forget to add the port number 5000
        if res.status_code == 200:
            predicted_price = res.json().get("predicted_price", "N/A")
            st.success(f"💰 Predicted Price: ${predicted_price:,.2f}")
        else:
            st.error("Prediction failed. Please check your API or inputs.")
    except Exception as e:
        st.error(f"❌ Error calling API: {e}, Kindly contact [Vigneshwar R](https://www.linkedin.com/in/vigneshwarravirao/)")