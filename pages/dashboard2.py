import streamlit as st
import pandas as pd
import random
import plotly.graph_objects as go
from streamlit_autorefresh import st_autorefresh
import folium
from streamlit_folium import folium_static
import time
from streamlit_option_menu import option_menu


st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

menu = option_menu(
    menu_title=None,
    options=["Map - Real Time Visualization", "Charts - Real Time Visualization"],
    icons=["map-fill", "bi-bar-chart-line-fill"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal"
)

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

# st.title("Real-time")
# st.subheader("Real-Time Sensor Data Visualization")


def fetch_latest_data_iot(x):
    records = x.find().sort("timestamp", -1).limit(100)
    return pd.DataFrame(list(records))


st_autorefresh(interval=5000, key='data_refresh')

if 'collection' in st.session_state:
    df = fetch_latest_data_iot(st.session_state['collection'])
    df = df.drop(columns=['_id'])


    # Formatting Date and Time
    df['Date'] = pd.to_datetime(df['Date']).dt.strftime('%B %d, %Y')
    df['Time'] = pd.to_datetime(df['Time']).dt.strftime('%H:%M:%S')
    # Combine Date and Time into a single datetime column
    df['DateTime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'])

    # tab1, tab2 = st.tabs(["Real Time Visualization on Map", "Real Time Visualization with Charts"])
    # with tab1:
    if menu == "Map - Real Time Visualization":

        def create_map(data):
            # Create a map centered around an average coordinate
            if not data.empty:
                center_lat, center_lon = data['latitude'].mean(), data['longitude'].mean()
            else:
                # Default to some location if there's no data
                center_lat, center_lon = 0, 0

            # Start map at the computed average location
            my_map = folium.Map(location=[center_lat, center_lon], zoom_start=20)

            # Add points from the data
            for index, item in data.iterrows():
                tooltip = (
                    f"Date: {item.get('Date', 'N/A')}, Time: {item.get('Time', 'N/A')}, \n"
                    f"Chl (ug/L): {item.get('Chl (ug/L)', 'N/A')}, BGA-PE (ug/L): {item.get('BGA-PE (ug/L)', 'N/A')}, \n"
                    f"Turb (FNU): {item.get('Turb (FNU)', 'N/A')}, TSS (mg/L): {item.get('TSS (mg/L)', 'N/A')}, \n"
                    f"ODO (%sat): {item.get('ODO (%sat)', 'N/A')}, ODO (mg/l): {item.get('ODO (mg/l)', 'N/A')}, \n"
                    f"Temp (C): {item.get('Temp (C)', 'N/A')}, Cond (uS/cm): {item.get('Cond (uS/cm)', 'N/A')}, \n"
                    f"Sal (PPT): {item.get('Sal (PPT)', 'N/A')}, Pressure (psi a): {item.get('Pressure (psi a)', 'N/A')}, \n"
                    f"Depth (m): {item.get('Depth (m)', 'N/A')}, latitude: {item.get('latitude', 'N/A')}, "
                    f"longitude: {item.get('longitude', 'N/A')}"
                )
                folium.Marker(
                    [item['latitude'], item['longitude']],
                    tooltip=tooltip
                ).add_to(my_map)

            return my_map
        data= fetch_latest_data_iot(st.session_state['collection'])
        my_map = create_map(data)  # Create the map
        folium_static(my_map, width=1550, height=800)  # Display the map in Streamlit
        # time.sleep(5)
    if menu == "Charts - Real Time Visualization":
    # with tab2:
        # Variables to plot (excluding Date, Time, and DateTime)
        variables_to_plot = ['Chl (ug/L)', 'BGA-PE (ug/L)', 'Turb (FNU)', 'TSS (mg/L)',
                             'ODO (%sat)', 'ODO (mg/l)', 'Temp (C)', 'Cond (uS/cm)',
                             'Sal (PPT)', 'Pressure (psi a)', 'Depth (m)']

        # Streamlit selectbox widget
        selected_variable = st.selectbox(
            'Choose a variable to plot:',
            variables_to_plot)

        # variable to plot
        var = selected_variable

        # create plot
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
        st.plotly_chart(fig, use_container_width=True)
    st.divider()
    with st.expander("See table with Raw Data", expanded=False):
        st.dataframe(df)
    if st.button('Reset Session'):
        st.session_state.clear()
        st.switch_page("streamlit_app.py")
else:
    st.error("No collection selected or session expired.")
    st.button("Go Back", on_click=st.switch_page, args=("streamlit_app.py",))

