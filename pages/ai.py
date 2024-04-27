import streamlit as st
from openai import OpenAI
from pymongo import MongoClient
import pandas as pd
import openai

# client2 = MongoClient(url)
# db_ = client2["biscaynebay"]
# collection_ = db_["mission_202404251553"]
def database_access():
    x = "swarm"
    # st.success("Amazing! The swarm is found and ready to deliver quality data. 🚤🏝️")
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
    this_client.close()
    return st.session_state['collection']


def fetch_latest_data_iot(x):
    records = x.find().sort("timestamp", -1).limit(100)  # Example: Get the latest 100 records
    return pd.DataFrame(list(records))



# data = data_df[["Temp (C)", "Sal (PPT)", "Depth (m)"]]

if __name__ == '__main__':
    with st.sidebar:
        openai_api_key = st.text_input("OpenAI API Key", key="Open Ai", type="password")
    st.title("BayBot 🤖")
    st.header("Making water quality data clear as Biscayne Bay.")

    data = fetch_latest_data_iot(database_access())
    if data:
        if "messages" not in st.session_state:
            st.session_state["messages"] = [
                {'role': 'system', "content": f"The data you should use to answer the questions is in {data}."},
                {"role": "assistant", "content": "I am BayBot, the smartest bot ever. I am here to bring Biscayne Bay's underwater secrets to the surface. How can I help you?"}]

        for msg in st.session_state.messages:
            if msg["role"] != "system":
                st.chat_message(msg["role"]).write(msg["content"])

        if prompt := st.chat_input():
            if not openai_api_key:
                st.info("Please add your OpenAI API key to continue.")
                st.stop()

            client = OpenAI(api_key=openai_api_key)

            st.session_state.messages.append({"role": "user", "content": prompt})
            st.chat_message("user").write(prompt)
            response = client.chat.completions.create(model="gpt-3.5-turbo", messages=st.session_state.messages)
            msg = response.choices[0].message.content
            st.session_state.messages.append({"role": "assistant", "content": msg})
            st.chat_message("assistant").write(msg)