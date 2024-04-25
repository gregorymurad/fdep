import streamlit as st
import pandas as pd
import random
import plotly.graph_objects as go
from streamlit_autorefresh import st_autorefresh


st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

color_dict = {'Chl (ug/L)': 'green',
              'BGA-PE (ug/L)': 'blue',
              'Turb (FNU)': 'brown',
              'TSS (mg/L)': 'grey',
              'ODO (%sat)': 'lightblue',
              'ODO (mg/l)': 'lightblue',
              'Temp (C)': 'red',
              'Cond (uS/cm)': '#FFD700',
              'Sal (PPT)': 'purple',
              'Pressure (psi a)': 'orange',
              'Depth (m)': 'darkblue'}

st.title("Real-time")
st.subheader("Real-Time Sensor Data Visualization")


def fetch_latest_data_iot(x):
    """
    Fetches the latest data using the provided parameter.

    :param x: The collection or table object to fetch the data from.
    :return: A pandas DataFrame containing the latest 100 records sorted by timestamp in descending order.
    """
    records = x.find().sort("timestamp", -1).limit(100)  # Example: Get the latest 100 records
    return pd.DataFrame(list(records))


st_autorefresh(interval=5000, key='data_refresh')

if 'collection' in st.session_state:
    df = fetch_latest_data_iot(st.session_state['collection'])
    df = df.drop(columns=['_id'])

    with st.expander("See table with Raw Data", expanded=False):
        st.dataframe(df)
    # Formatting Date and Time
    df['Date'] = pd.to_datetime(df['Date'], format='%m%d%y').dt.strftime('%B %d, %Y')
    df['Time'] = pd.to_datetime(df['Time'], format='%H%M%S').dt.strftime('%H:%M:%S')

    # Combine Date and Time into a single datetime column
    df['DateTime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'])

    # Variables to plot (excluding Date, Time, and DateTime)
    variables_to_plot = ['Chl (ug/L)', 'BGA-PE (ug/L)', 'Turb (FNU)', 'TSS (mg/L)',
                         'ODO (%sat)', 'ODO (mg/l)', 'Temp (C)', 'Cond (uS/cm)',
                         'Sal (PPT)', 'Pressure (psi a)', 'Depth (m)']

    for i in range(0, len(variables_to_plot), 2):  # looping through every two variables
        cols = st.columns(2)

        for j in range(2):  # looping through the current and the next variable
            if i + j < len(variables_to_plot):
                var = variables_to_plot[i + j]
                fig = go.Figure()

                fig.add_trace(go.Scatter(
                    x=df['Time'], y=df[var], mode='lines+markers',
                    name=var,
                    hoverinfo='y+name',
                    text=[f'{var}: {val}' for val in df[var]],
                    marker=dict(color=color_dict[var])  # Here is where we use the color
                ))

                fig.update_layout(
                    title=f'Sensor Data for {var} on {df["Date"].iloc[0]}',
                    xaxis_title='Time',
                    yaxis_title='Values',
                    legend_title='Parameters'
                )
                cols[j].plotly_chart(fig, use_container_width=True)
        st.divider()
    if st.button('Reset Session'):
        st.session_state.clear()
        st.switch_page("streamlit_app.py")
else:
    st.error("No collection selected or session expired.")
    st.button("Go Back", on_click=st.switch_page, args=("streamlit_app.py",))




