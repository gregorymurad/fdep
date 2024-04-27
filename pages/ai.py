import streamlit as st
from openai import OpenAI
from pymongo import MongoClient
import pandas as pd
import openai
from typing import List


# client2 = MongoClient(url)
# db_ = client2["biscaynebay"]
# collection_ = db_["mission_202404251553"]


# DATA BY LOCATION
# |-> BBC
# |--> Data by date
# |---> 1 - September 18th 2020
bbc_sep_2020_1 = "Logs/BBC/1 - Biscayne Bay - September 18th 2020/20200918_105724_Mission1_09_11_IVER2-218.csv"
bbc_sep_2020_2 = "Logs/BBC/1 - Biscayne Bay - September 18th 2020/20200918_105852_TrianglePathMission_IVER2-218.csv"
bbc_sep_2020_3 = "Logs/BBC/1 - Biscayne Bay - September 18th 2020/20200918_110002_TrianglePathMission_IVER2-218.csv"
bbc_sep_2020_4 = "Logs/BBC/1 - Biscayne Bay - September 18th 2020/20200918_115659_PleaseWork_IVER2-218.csv"
bbc_sep_2020_5 = "Logs/BBC/1 - Biscayne Bay - September 18th 2020/20200918_120605_PleaseWorkSRP_IVER2-218.csv"
bbc_sep_2020_6 = "Logs/BBC/1 - Biscayne Bay - September 18th 2020/ManualLog_11_05_09_92.csv"
bbc_sep_2020_7 = "Logs/BBC/1 - Biscayne Bay - September 18th 2020/ManualLog_12_19_47_14.csv"
# |---> 2 - October 4th 2020
bbc_oct_2020_1 = "Logs/BBC/2 - Biscayne Bay - October 4th 2020/20201004_171844_TestForLittleRiver_IVER2-218.csv"
bbc_oct_2020_2 = "Logs/BBC/2 - Biscayne Bay - October 4th 2020/20201004_180324_LittleRiverOct4_IVER2-218.csv"
bbc_oct_2020_3 = "Logs/BBC/2 - Biscayne Bay - October 4th 2020/ManualLog_17_00_45_64.csv"
# |---> 3 - January 30th 2021
bbc_jan_2021_1 = "Logs/BBC/3 - Biscayne Bay - January 30th 2021/20210130_124101_jan302021_bbc_IVER2-218.csv"
bbc_jan_2021_2 = "Logs/BBC/3 - Biscayne Bay - January 30th 2021/20210130_130339_jan302021_bbc_IVER2-218.csv"
bbc_jan_2021_3 = "Logs/BBC/3 - Biscayne Bay - January 30th 2021/20210130_131335_jan302021_bbc_IVER2-218.csv"
bbc_jan_2021_4 = "Logs/BBC/3 - Biscayne Bay - January 30th 2021/20210130_135713_jan302021_bbc_IVER2-218.csv"
bbc_jan_2021_5 = "Logs/BBC/3 - Biscayne Bay - January 30th 2021/20210130_140634_jan302021_bbc_IVER2-218.csv"
bbc_jan_2021_6 = "Logs/BBC/3 - Biscayne Bay - January 30th 2021/20210130_143547_jan302021_bbc_IVER2-218.csv"
# |---> 4 - February 13th 2021
bbc_feb_2021_1 = "Logs/BBC/4 - Biscayne Bay - February 13th 2021/20210213_150135_feb132021_bbc_IVER2-218.csv"
bbc_feb_2021_2 = "Logs/BBC/4 - Biscayne Bay - February 13th 2021/20210213_155452_feb132021_b_bbc_IVER2-218.csv"
# |---> 5 - March 16th 2021
bbc_mar_2021_1 = "Logs/BBC/5 - Biscayne Bay - March 16th 2021/20210316_112824_onthespot_mar16_IVER2-218.csv"
# |---> 6 - June 9th 2021
bbc_jun_2021_1 = "Logs/BBC/6 - Biscayne Bay - June 9th 2021/20210609_105413_mongabay2_IVER2-218.csv"
bbc_jun_2021_2 = "Logs/BBC/6 - Biscayne Bay - June 9th 2021/20210609_110304_mongabay2_IVER2-218.csv"
bbc_jun_2021_3 = "Logs/BBC/6 - Biscayne Bay - June 9th 2021/20210609_112348_mongabay_IVER2-218.csv"
# |---> 7 - September 2nd 2021
bbc_sep_2021_1 = "Logs/BBC/7 - Biscayne Bay - September 2nd 2021/sep2_2021_bbc_mission_1.csv"
bbc_sep_2021_2 = "Logs/BBC/7 - Biscayne Bay - September 2nd 2021/sep2_2021_bbc_mission_2.csv"
bbc_sep_2021_test = "Logs/BBC/7 - Biscayne Bay - September 2nd 2021/sep2_2021_bbc_test.csv"
# |---> 8 - October 21st 2021
bbc_oct_2021_1 = "Logs/BBC/8 - Biscayne Bay - October 21st 2021/20211021_dataset1.csv"
bbc_oct_2021_2 = "Logs/BBC/8 - Biscayne Bay - October 21st 2021/20211021_dataset2.csv"
bbc_oct_2021_3 = "Logs/BBC/8 - Biscayne Bay - October 21st 2021/20211021_dataset3.csv"
# |---> 9 - December 16th 2021
bbc_dec_2021 = "Logs/BBC/9 - Biscayne Bay - December 16th 2021/20211216_dataset.csv"
# |---> 10 - February 4th 2022
bbc_feb_2022 = "Logs/BBC/10 - Biscayne Bay - February 4th 2022/20220204_dataset.csv"
# |---> 11 - August 28th 2022
bbc_aug_2022_1 = "Logs/BBC/11 - Biscayne Bay - August 28th 2022/08-28-22-mission1.csv"
bbc_aug_2022_2 = "Logs/BBC/11 - Biscayne Bay - August 28th 2022/08-28-22-mission2.csv"
bbc_aug_2022_3 = "Logs/BBC/11 - Biscayne Bay - August 28th 2022/08-28-22-mission3.csv"
# |---> 12 - October 7th 2022
bbc_oct_2022_1 = "Logs/BBC/12 - Biscayne Bay - October 7th 2022/10-7-22-mission1.csv"
bbc_oct_2022_2 = "Logs/BBC/12 - Biscayne Bay - October 7th 2022/10-7-22-mission2.csv"
bbc_oct_2022_3 = "Logs/BBC/12 - Biscayne Bay - October 7th 2022/10-7-22-mission3.csv"
# |---> 13 - November 16th 2022
bbc_nov_2022_1 = "Logs/BBC/13 - Biscayne Bay - November 16th 2022/11-16-22-mission1.csv"
bbc_nov_2022_2 = "Logs/BBC/13 - Biscayne Bay - November 16th 2022/11-16-22-mission2.csv"

# |-> LITTLE RIVER
# |--> Data by date
# |---> October 2020
lr_oct_2020_1 = "Logs/LittleRiver/ManualLog_17_00_45_64.csv" #oct3
lr_oct_2020_2 = "Logs/LittleRiver/20201004_171844_TestForLittleRiver_IVER2-218.csv"
lr_oct_2020_3 = "Logs/LittleRiver/20201004_180324_LittleRiverOct4_IVER2-218.csv"


# st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    loc_option = st.selectbox("Choose a location:",
                              ("Biscayne Bay", "Little River"))

with col2:
    if loc_option == "Biscayne Bay":
        ds_data = st.selectbox("Date:", options=["November 16th 2022", "October 7th 2022",
                                                          "August 28th 2022", "February 4th 2022",
                                                          "December 16th 2021", "October 21st 2021",
                                                          "September 2nd 2021", "June 9th 2021",
                                                          "March 16th 2021", "February 13th 2021",
                                                          "January 30th 2021", "October 4th 2020",
                                                          "September 18th 2020"])


    elif loc_option == "Little River":
        ds_data = st.selectbox("Date:", options=["October 4th 2020", "October 3rd 2020"])

with col3:
    if loc_option == "Biscayne Bay" and ds_data:
        if ds_data == "September 18th 2020":
            ds_option = st.selectbox("Select a Dataset:", options=["sep_2020_1", "sep_2020_2", "sep_2020_3",
                                                                   "sep_2020_4", "sep_2020_5", "sep_2020_6",
                                                                   "sep_2020_7"])
        elif ds_data == "October 4th 2020":
            ds_option = st.selectbox("Select a Dataset:", options=["oct_2020_1", "oct_2020_2", "oct_2020_3"])
        elif ds_data == "January 30th 2021":
            ds_option = st.selectbox("Select a Dataset:", options=["jan_2021_1", "jan_2021_2", "jan_2021_3",
                                                                   "jan_2021_4", "jan_2021_5", "jan_2021_6"])
        elif ds_data == "February 13th 2021":
            ds_option = st.selectbox("Select a Dataset:", options=["feb_2021_1", "feb_2021_2"])
        elif ds_data == "March 16th 2021":
            ds_option = st.selectbox("Select a Dataset:", options=["mar_2021_1"])
        elif ds_data == "June 9th 2021":
            ds_option = st.selectbox("Select a Dataset:", options=["jun_2021_1", "jun_2021_2", "jun_2021_3"])
        elif ds_data == "September 2nd 2021":
            ds_option = st.selectbox("Select a Dataset:", options=["sep_2021_1", "sep_2021_2", "sep_2021_test"])
        elif ds_data == "October 21st 2021":
            ds_option = st.selectbox("Select a Dataset:", options=["oct_2021_1", "oct_2021_2", "oct_2021_3"])
        elif ds_data == "December 16th 2021":
            ds_option = st.selectbox("Select a Dataset:", options=["dec_2021"])
        elif ds_data == "February 4th 2022":
            ds_option = st.selectbox("Select a Dataset:", options=["feb_2022"])
        elif ds_data == "August 28th 2022":
            ds_option = st.selectbox("Select a Dataset:", options=["aug_2022_3", "aug_2022_2", "aug_2022_1"])
        elif ds_data == "October 7th 2022":
            ds_option = st.selectbox("Select a Dataset:", options=["oct_2022_1", "oct_2022_2", "oct_2022_3"])
        elif ds_data == "November 16th 2022":
            ds_option = st.selectbox("Select a Dataset:", options=["nov_2022_1", "nov_2022_2"])
        if ds_option:
            # get the value of a variable given its name in a string
            dataset = locals()['bbc_' + ds_option]

    elif loc_option == "Little River" and ds_data:
        if ds_data == "October 3rd 2020":
            ds_option = st.selectbox("Select a Dataset:", options=["oct_2020_1"])
        elif ds_data == "October 4th 2020":
            ds_option = st.selectbox("Select a Dataset:", options=["oct_2020_3", "oct_2020_2"])
        if ds_option:
            # get the value of a variable given its name in a string
            dataset = locals()['lr_' + ds_option]

def selectDataframe(dataset: str, selected_parameters: List[str]):
    entire_ds = pd.read_csv(dataset)  # read the entire dataset as a dataframe
    # print(entire_ds.columns) #to print the head of the dataframe

    selected_parameters.insert(0, "Latitude")
    selected_parameters.insert(1, "Longitude")
    selected_parameters.insert(2, "Time hh:mm:ss")

    try:
        partial_ds = entire_ds[selected_parameters]
        #print("The dataframe was successfully created!")
        #print(partial_ds.columns) #to print the head of the dataframe
        partial_ds=partial_ds.rename(columns={"Latitude": "lat", "Longitude": "lon"})
        return partial_ds, entire_ds
    except ValueError:
        st.error("Oops! Some selected water parameters do not exist in this dataset. Try again...")

parameters = [1,2,3,4]
water_parameters = {1: "ODO mg/L",
                    2: "Temperature (c)",
                    3: "pH",
                    4: "Total Water Column (m)"}
                    # 5: "Salinity (ppt)",
                    # 6: "Turbid+ NTU",
                    # 7: "BGA-PC cells/mL"}
selected_parameters = [water_parameters.get(key) for key in
                       parameters]
# print("selected_parameters: ", selected_parameters)
partial_ds, entire_ds = selectDataframe(dataset, selected_parameters)  # calling function selectDataframe
def fetch_latest_data_iot(x):
    records = x.find().sort("timestamp", -1).limit(100)  # Example: Get the latest 100 records
    return pd.DataFrame(list(records))

# data = fetch_latest_data_iot(collection_)
# data = data_df[["Temp (C)", "Sal (PPT)", "Depth (m)"]]
data = partial_ds


with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="Open Ai", type="password")


st.title("BayBot 🤖")
st.header("Making water quality data clear as Biscayne Bay.")

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

