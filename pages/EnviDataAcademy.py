import streamlit as st
from openai import OpenAI
from pymongo import MongoClient
import pandas as pd
import openai
from typing import List
from streamlit_extras.bottom_container import bottom


st.set_page_config(page_title="EnviData Academy", layout="wide")
st.sidebar.page_link("streamlit_app.py", label="Home", icon="🏠")
st.sidebar.page_link("pages/realTime.py", label="Real-Time Data", icon="🚢")
st.sidebar.page_link("pages/historicalData.py", label="Historical Data", icon="📊")
st.sidebar.page_link("pages/ai3.py", label="BayBot (AI Tool)", icon="🤖")
st.sidebar.page_link("pages/EnviDataAcademy.py", label="EnviData Academy", icon="🏫")
st.sidebar.divider()

st.sidebar.subheader("Choose a Dataset")
dataset = None

st.title("EnviData Academy")
st.header("Advancing Environmental Innovation with Data Science")
st.write("""
Welcome to the EnviData Academy's introductory course on Data Science. This app is designed to give you a hands-on experience with basic data science concepts, using real-world environmental data. 
You will learn how to load data, clean data, visualize data, and perform basic statistical analysis. Let's get started!
""")