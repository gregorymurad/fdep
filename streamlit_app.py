import streamlit as st
from pymongo import MongoClient
import os
import utils
from streamlit_extras.bottom_container import bottom


st.set_page_config(page_title="Real-Time Data Dashboard", layout="wide")

st.sidebar.page_link("streamlit_app.py", label="Home", icon="🏠")
st.sidebar.page_link("pages/realTime.py", label="Real-Time Data", icon="🚢")
st.sidebar.page_link("pages/historicalData.py", label="Historical Data", icon="📊")
st.sidebar.page_link("pages/ai3.py", label="BayBot (AI Tool)", icon="🤖")

# Placeholder for dynamic updates
placeholder = st.empty()
st.title("The Ultimate Data Dashboard for Biscayne Bay Water Quality Data")
st.header("The first dashboard powered with AI capabilities")
st.subheader("Developed by the Marine Robotics Lab at Florida International University")

st.image("Images/FDEP Infrastructure Diagram 2024.png")

with bottom():
    st.divider()
    st.write("This project is conducted by the MARINE Lab in collaboration with Boswell Lab and Mora Lab for the FDEP project. The goal of this initiative is to advance our understanding and management of marine ecosystems through innovative data analysis and visualization techniques.")

