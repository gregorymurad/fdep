import streamlit as st
from pymongo import MongoClient
import os
import utils

st.set_page_config(page_title="Real-Time Data Dashboard", layout="wide")

# st.sidebar.page_link("streamlit_app.py", label="Home", icon="🏠")
# st.sidebar.page_link("https://www.google.com", label="Google", icon="🌎")

# Placeholder for dynamic updates
placeholder = st.empty()
st.title("Real-Time Data Dashboard")


def database_access(x):
    db_url = None
    if x == "iot":
        db_url = ""
        db_name = "db"
    elif x == "swarm":
        st.success("Amazing! The swarm is found and ready to deliver quality data. 🚤🏝️")
        db_url = st.secrets["SWARM_CONNECTION_STRING"]
        db_name = "swarm_exo"

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
            st.switch_page(f"pages/real_time_stream_{x}.py")  # Make sure the state is already updated

    this_client.close()



instrument = st.selectbox("Select a scientific instrument", ("", "Swarm", "Heron", "IoT"))
if instrument == "IoT":
    st.warning("In construction of IoT database 🚧. \n Please use another database")
elif instrument == "Heron":
    st.warning("In construction of Heron database 🚧. \n Please use another database")
elif instrument == "Swarm":
    database_access('swarm')
