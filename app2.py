import streamlit as st
import plotly.graph_objects as go

col1, col2 = st.columns([1,8])
with col2:
    st.markdown("""
    <h1 style='
        text-align:center;
        color:#60A5FA;
        font-weight:700;
        margin-top: 20px;
        letter-spacing:1px;
    '>
    Real Estate Dashboard
    </h1>
    """, unsafe_allow_html=True)
with col1:
    st.image("Image.png", width = 150)
col10, col11, col12 = st.sidebar.columns([1,2,1]) #columns for sidebar
with col11:
    st.image("image.png", use_container_width="true")
st.set_page_config(layout = "wide")
st.sidebar.markdown("""
<h2 style='color:#60A5FA; text-align:center;'>Dashboard Filters</h2>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")


st.write("---")

st.markdown("""
<h2 style='color:#60A5FA;'>💡 What-If Price Calculator</h2>
<p style='color:#9CA3AF;'>Adjust inputs in the sidebar to see real-time price prediction</p>
""", unsafe_allow_html=True)


#Price predictionssss + Sliders, filters
price = 2000000

st.sidebar.markdown("Prperty Basics")
st.sidebar.selectbox("Location", ["Mumbai", "Delhi", "Bengaluru", "Hyderabad", "Chennai", "Kolkata", "Pune", "Ahmedabad", "Jaipur", "Lucknow", "Kanpur", "Nagpur", "Indore", "Bhopal", "Patna", "Surat", "Vadodara", "Coimbatore", "Kochi", "Thiruvananthapuram", "Visakhapatnam", "Vijayawada", "Nashik", "Aurangabad", "Amritsar", "Chandigarh", "Ludhiana", "Jalandhar", "Ranchi", "Raipur", "Bhubaneswar", "Guwahati", "Shillong", "Imphal", "Agartala", "Aizawl", "Itanagar", "Panaji", "Dehradun", "Shimla", "Srinagar", "Jammu", "Udaipur", "Jodhpur", "Gwalior", "Varanasi", "Allahabad", "Meerut", "Noida", "Gurugram"])
st.sidebar.slider("Area sq.ft", 400, 10000, 1000)
st.sidebar.slider("Number of Bedrooms", 1, 6, 2)
st.sidebar.slider("Property Age", 0, 100, 5)

st.sidebar.markdown("Amenities")
parking = st.sidebar.checkbox("Parking")
gym = st.sidebar.checkbox("Gym")
pool = st.sidebar.checkbox("Swimming Pool")
security = st.sidebar.checkbox("24x7 Security")

st.markdown(f"""
<h1 style='text-align:center; color:#60A5FA; font-size:42px;'>
$ {price:,.0f}
</h1>
""", unsafe_allow_html=True)


#price prediction gaude
def price_gauge(price):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=price,
        title={'text': "Price Level"},
        number={'valueformat': ',d'},
        gauge={
            'axis': {'range': [0, 10000000]},  # adjust based on your data
            
            'bar': {'color': "#A0B9D7"},
            
            'steps': [
                {'range': [0, 3000000], 'color': "green"},
                {'range': [3000000, 7000000], 'color': "yellow"},
                {'range': [7000000, 10000000], 'color': "red"},
            ],
        }
    ))
    
    fig.update_layout(
        height=350,
        paper_bgcolor="rgba(0,0,0,0)",
        font={'color': "white"}
    )
    
    return fig

col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.plotly_chart(price_gauge(price), use_container_width="true")






#Metric cardsss

def card(title, value):
    st.markdown(f"""
    <div style="
        background: linear-gradient(145deg, #1e3a5f, #0f2a3f);
        padding:25px;
        border: 1px solid rgba(255,255,255,0.08);
        border-radius:40px;
        text-align:center;
        box-shadow: 0px 6px 25px rgba(0,0,0,0.6);
        transition: 0.3s;
    ">
        <h4 style="color:#9CA3AF; margin-bottom:10px;">{title}</h4>
        <h1 style="color:white; margin:0;">{value}</h1>
    </div>
    """, unsafe_allow_html=True)
st.write("---")
col3, col4, col5 = st.columns(3)
with col3:
    card("Average price", "$50k")
with col4:
    card("Max Price", "$90K")
with col5:
    card("Min Price", "$20K")
