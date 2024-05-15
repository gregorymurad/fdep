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
st.title("BayBot 🤖")
st.header("Making water quality data clear as Biscayne Bay.")
st.subheader("The first AI powered water quality monitoring app")


def database_access(x):
    db_url = None
    if x == "iot":
        db_url = ""
        db_name = "db"
    elif x == "swarm":
        st.success("Amazing! The swarm is found and ready to deliver quality data. 🚤🏝️")
        db_url = st.secrets["SWARM_CONNECTION_STRING"]
        # db_name = "swarm_exo"
        db_name = "biscaynebay"

    if db_url is None:
        st.error(f"Missing environment variable: '{x.upper()}_CONNECTION_STRING'")
        raise ValueError(f"Missing environment variable: '{x.upper()}_CONNECTION_STRING'")

    this_client = MongoClient(db_url)
    this_client.admin.command('ismaster')  # checks for successful connection
    this_db = this_client[db_name]

    collection_names = this_db.list_collection_names()
    collection_names.insert(0, "")
    collection_name = st.selectbox("Select a collection", collection_names)

    if collection_name:
        st.success("You selected a great mission! 🎉")
        st.session_state['collection'] = this_db[collection_name]  # Set session state here
        if st.button("Update Data"):

            print("Session state collection type:", type(st.session_state['collection']))
            # st.switch_page(f"pages/real_time_stream_{x}.py")  # Make sure the state is already updated
            st.switch_page(f"pages/dashboard5.py")
    this_client.close()


if __name__ == '__main__':
    database_access('swarm')

    with bottom():
        st.divider()
        st.write(
            "This project is conducted by the MARINE Lab in collaboration with Boswell Lab and Mora Lab for the FDEP project. The goal of this initiative is to advance our understanding and management of marine ecosystems through innovative data analysis and visualization techniques.")
