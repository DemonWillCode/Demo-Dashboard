import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")
st.markdown("""
    <h1 style='text-align: center; color: #4CAF50;'>
    Real Estate Dashboard
    </h1>
""", unsafe_allow_html=True)
st.image("https://imgs.search.brave.com/IXVZYh0738NkrDOK2C7PRAZRu3h4DvE8i_3jz8YpPmA/rs:fit:860:0:0:0/g:ce/aHR0cHM6Ly9tZWRp/YS5nZXR0eWltYWdl/cy5jb20vaWQvODcy/OTkyNjMvcGhvdG8v/b3ZlcndlaWdodC1t/YW4uanBnP3M9NjEy/eDYxMiZ3PTAmaz0y/MCZjPU9YZzdUcUlr/MGNGa3ZLSGpxMW15/dU9KZ1R5aUZ4OHdB/TFdveko1MGVNeGM9" use_container_width="true")
df = pd.read_csv("data.csv")
st.subheader("Sample Data")
st.write(df)
st.sidebar.header("Enter House details")



area = st.sidebar.slider("Area (sq ft)", 500, 5000, 2000    )
bedrooms = st.sidebar.slider("Enter number of bedroos", 1, 6, 2)
location = st.sidebar.selectbox("Enter the location", ["Electronic City", "Hebbagodi", "Yelahanka", "Anekal"])

price = area * 300 + bedrooms * 50000

if location == "Electronic City":
    price += 200000
elif location == "Hebbagodi":
    price += 100000
elif location == "Yelahanka":
    price += 300000

st.subheader("Predicted price based on the selection")

st.success(f"$ {price:,.0f}")

col1, col2, = st.columns(2)
with col1:
    st.metric("Avg Price", "₹ 50L")


with col2:
    st.metric("Total Houses", "120")

st.success("This is green ✅")
st.error("This is red ❌")
st.warning("This is yellow ⚠️")
st.info("This is blue ℹ️")

st.subheader("Price distribution")

st.bar_chart(df["price"])

avg_price = df.groupby("location")["price"].mean()
st.bar_chart(avg_price)