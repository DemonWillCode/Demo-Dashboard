import streamlit as st
st.set_page_config(layout="wide")

import plotly.graph_objects as go
import joblib
import pandas as pd
import numpy as np
import gdown
import os

# Download model
if not os.path.exists("delhi_price_model.pkl"):
    gdown.download(
        "https://drive.google.com/uc?id=1cbRacehmhW0PippvxCY5bejg3gwdpII6",
        "delhi_price_model.pkl",
        quiet=False
    )

# Download columns
if not os.path.exists("delhi_model_columns.pkl"):
    gdown.download(
        "https://drive.google.com/uc?id=1f4Ze50-X08zkjeCG4Gui6Vux0WkI8h6w",
        "delhi_model_columns.pkl",
        quiet=False
    )


# Load model
model = joblib.load("delhi_price_model.pkl")
columns = joblib.load("delhi_model_columns.pkl")
columns = list(columns)



# ---------------- HEADER ----------------
col1, col2 = st.columns([4.5,8])
with col2:
    st.markdown("""
    <h1 style='
        text-align:left;
        color:#60A5FA;
        font-weight:700;
        margin-top: 20px;
        letter-spacing:1px;
    '>
    Real Estate Dashboard
    </h1>
    """, unsafe_allow_html=True)
with col1:
    st.image("image.png", width=300)

# Sidebar image
col10, col11, col12 = st.sidebar.columns([1,10,1])
with col11:
    st.image("image.png", use_container_width=True)

st.sidebar.markdown("""
<h2 style='color:#60A5FA; text-align:center;'>Dashboard Filters</h2>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")

st.markdown("<hr style='border:1px solid #1f2937'>", unsafe_allow_html=True)

st.markdown("""
<h2 style='color:#60A5FA;'>💡 What-If Price Calculator</h2>
<p style='color:#9CA3AF;'>Adjust inputs in the sidebar to see real-time price prediction</p>
""", unsafe_allow_html=True)

# ---------------- INPUTS ----------------
st.sidebar.markdown("Property Basics")

location = st.sidebar.selectbox("Location", [
"Burari", "Dwarka Mor", "Jamia Nagar", "Noida",
"Om Nagar", "Sector 10 Dwarka", "Sector 11 Dwarka",
"Sector 12 Dwarka", "Sector 19 Dwarka", "Sector 22 Dwarka",
"Sector 4 Dwarka", "Sector 6 Dwarka", "Uttam Nagar", "Vasant Kunj"
])

choice = st.sidebar.radio(
    "Select Input Type",
    ["Slider", "Manual Input"]
)

if choice == "Slider":
    area = st.sidebar.slider("Area sq.ft", 0, 10000, 400)

else:
    area = st.sidebar.number_input("Area sq.ft",min_value=0,max_value=10000,value=400,step=1)

bedroom = st.sidebar.slider("Number of Bedrooms", 1, 14, 2)
age = st.sidebar.slider("Property Age", 0, 100, 5)

st.sidebar.markdown("Amenities")

parking = st.sidebar.checkbox("Parking")
security = st.sidebar.checkbox("24x7 Security")
resale = st.sidebar.checkbox("Resale Property")
garden = st.sidebar.checkbox("Landscaped Gardens")
indoor = st.sidebar.checkbox("Indoor Games")
intercom = st.sidebar.checkbox("Intercom")
sports = st.sidebar.checkbox("Sports Facility")
club = st.sidebar.checkbox("Club House")
power = st.sidebar.checkbox("Power Backup")
gas = st.sidebar.checkbox("Gas Connection")
ac = st.sidebar.checkbox("AC")
wifi = st.sidebar.checkbox("Wifi")
children = st.sidebar.checkbox("Children Play Area")
lift = st.sidebar.checkbox("Lift Available")

# ---------------- CONVERSION ----------------
parking_val = 1 if parking else 0
security_val = 1 if security else 0
resale_val = 1 if resale else 0
garden_val = 1 if garden else 0
indoor_val = 1 if indoor else 0
intercom_val = 1 if intercom else 0
sports_val = 1 if sports else 0
club_val = 1 if club else 0
power_val = 1 if power else 0
gas_val = 1 if gas else 0
ac_val = 1 if ac else 0
wifi_val = 1 if wifi else 0
children_val = 1 if children else 0
lift_val = 1 if lift else 0

# ---------------- MODEL INPUT ----------------
input_data = dict.fromkeys(columns, 0)

# Basic
input_data["Area"] = area
input_data["No._of_Bedrooms"] = bedroom

# Amenities mapping
input_data["Resale"] = resale_val
input_data["LandscapedGardens"] = garden_val
input_data["IndoorGames"] = indoor_val
input_data["Intercom"] = intercom_val
input_data["SportsFacility"] = sports_val
input_data["ClubHouse"] = club_val
input_data["24X7Security"] = security_val
input_data["PowerBackup"] = power_val
input_data["CarParking"] = parking_val
input_data["Gasconnection"] = gas_val
input_data["AC"] = ac_val
input_data["Wifi"] = wifi_val
input_data["Children'splayarea"] = children_val
input_data["LiftAvailable"] = lift_val

#---------------- ENGINEERED FEATURES ----------------
total_amenities = (
    parking_val + security_val +
    garden_val + indoor_val + intercom_val + sports_val +
    club_val + power_val + gas_val + ac_val +
    wifi_val + children_val + lift_val
)

input_data["Total_Amenities"] = total_amenities
input_data["Amenity_Score"] = total_amenities * 10
input_data["Bedroom_Density"] = bedroom / area if area != 0 else 0
input_data["Price_per_sqft"] = 5000



# ---------------- LOCATION ----------------
location_col = f"Location_{location}"

if location_col in input_data:
    input_data[location_col] = 1

# ---------------- PREDICTION ----------------
input_df = pd.DataFrame([input_data])
input_df = input_df[columns]

price = model.predict(input_df)[0]

# Adjust age manually
price -= age * 10000

# Safety
if np.isnan(price) or np.isinf(price):
    price = 0

price = max(price, 0)

# ---------------- DISPLAY ----------------
st.markdown(f"""
<h1 style='
text-align:center;
color:#60A5FA;
text-shadow: 0px 0px 20px rgba(96,165,250,0.6);
'>
₹ {price:,.0f}
</h1>
""", unsafe_allow_html=True)

st.caption(" AI-powered price prediction")

# ---------------- GAUGE ----------------
def price_gauge(price):
    max_val = 25000000

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=price,
        number={'valueformat': ',d'},
        title={'text': "Price Level"},
        gauge={
            'axis': {'range': [0, max_val]},
            'bar': {'color': "#A0B9D7"},
            'steps': [
                {'range': [0, max_val*0.3], 'color': "green"},
                {'range': [max_val*0.3, max_val*0.7], 'color': "yellow"},
                {'range': [max_val*0.7, max_val], 'color': "red"},
            ],
        }
    ))

    fig.update_layout(
        height=350,
        paper_bgcolor="rgba(0,0,0,0)",
        font={'color': "white"}
    )

    return fig

col1, col2, col3 = st.columns([1,2,1])
with col2:
    st.plotly_chart(price_gauge(price), use_container_width=True)

# ---------------- CARDS ----------------
def card(title, value):
    st.markdown(f"""
    <div style="
        background: linear-gradient(145deg, #1e3a5f, #0f2a3f);
        padding:25px;
        border: 1px solid rgba(255,255,255,0.08);
        border-radius:40px;
        text-align:center;
        box-shadow: 0px 6px 25px rgba(0,0,0,0.6);
    ">
        <h4 style="color:#9CA3AF;">{title}</h4>
        <h1 style="color:white;">{value}</h1>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<hr style='border:1px solid #1f2937'>", unsafe_allow_html=True)

col3, col4, col5 = st.columns(3)

with col3:
    card("Average price", f"₹ {int(price*0.8):,}")
with col4:
    card("Max Price", f"₹ {int(price*1.2):,}")
with col5:
    card("Min Price", f"₹ {int(price*0.6):,}")

st.markdown("<hr style='border:1px solid #1f2937'>", unsafe_allow_html=True)

# ---------------- Charts ----------------

st.markdown("""
<h2 style='color:#60A5FA;'>
Amenities vs Property Price
</h2>
""", unsafe_allow_html=True)

df = pd.read_csv("d1.csv")


amenity_price = (
    df.groupby("Total_Amenities")["Price"]
    .mean()
)

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=amenity_price.index,
    y=amenity_price.values,
    mode='lines+markers'
))

fig.update_layout(
    title="Average Property Price by Amenities",

    font=dict(color="white"),

    xaxis=dict(
        title="Number of Amenities",
    ),

    yaxis=dict(
        title="Average Price",
    ),

    height=500
)

st.plotly_chart(fig, use_container_width=True)


#bar

location_price = (
    df.groupby("Location")["Price_per_sqft"]
    .mean()
    .sort_values(ascending=False)
)

fig = go.Figure()

fig.add_trace(go.Bar(
    x=location_price.index,
    y=location_price.values,
    marker_color="#60A5FA"
))

fig.update_layout(
    title="Average Price per Sqft by Location",

    xaxis=dict(
        title="Location",
       
    ),

    yaxis=dict(
        title="Price per Sqft",
    ),

    height=500
)

st.plotly_chart(fig, use_container_width=True)



fig = go.Figure()

fig.add_trace(go.Scatter(
    x=df["Area"],
    y=df["Price"],

    mode='markers',

    marker=dict(
        size=8,
        color="#60A5FA",
        opacity=0.7
    )
))

fig.update_layout(
    title="Area vs Property Price",

    xaxis=dict(
        title="Area (sq.ft)",
    ),

    yaxis=dict(
        title="Property Price",
    ),

    height=500
)

st.plotly_chart(fig, use_container_width=True)