import time
import streamlit as st
import numpy as np
import pandas as pd
from streamlit_autorefresh import st_autorefresh
from streamlit_extras.bottom_container import bottom


### TESTING CONTAINER THAT UPDATES INDIVIDUALLY
with st.spinner("Doing a slow thing"):
    time.sleep(2)

@st.experimental_fragment # Just add the decorator
def simple_chart():
    st_autorefresh(interval=5000, key='data_refresh')
    st.write("When you move the slider, only the chart updates")
    val = st.slider("Number of bars", 1, 20, 4)
    st.bar_chart(np.random.default_rng().random(val))

simple_chart()


with st.container():
    df = pd.DataFrame(
        np.random.randint(0, 100, size=(100, 4)),
        columns=list('ABCD')
    )
    st.line_chart(df)

with bottom():
    st.divider()
    st.write("This project is conducted by the MARINE Lab in collaboration with Boswell Lab and Mora Lab for the FDEP project. The goal of this initiative is to advance our understanding and management of marine ecosystems through innovative data analysis and visualization techniques.")
