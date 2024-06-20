import streamlit as st
import pandas as pd
import random
import plotly.graph_objects as go
from streamlit_autorefresh import st_autorefresh
import folium
from streamlit_folium import folium_static, st_folium
import time
from streamlit_option_menu import option_menu
import pydeck as pdk
import plotly.express as px
from streamlit_extras.bottom_container import bottom


st.set_page_config(layout="wide", initial_sidebar_state="collapsed")
st_autorefresh(interval=5000, key='wholePage_refresh')

st.sidebar.page_link("streamlit_app.py", label="Home", icon="🏠")
st.sidebar.page_link("pages/realTime.py", label="Real-Time Data", icon="🚢")
st.sidebar.page_link("pages/historicalData.py", label="Historical Data", icon="📊")
st.sidebar.page_link("pages/ai3.py", label="BayBot (AI Tool)", icon="🤖")
st.sidebar.page_link("pages/EnviDataAcademy.py", label="EnviData Academy", icon="🏫")

image_ = "Images/swarmIcon.png"
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
    records = x.find().sort("timestamp", -1).limit(1000)
    return pd.DataFrame(list(records))


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
        def create_map_alt2(dataframe):
            fig_map = px.scatter_mapbox(dataframe, lat='latitude', lon='longitude', hover_data=df, zoom=17,size_max=100)
            fig_map.update_layout(mapbox_style="open-street-map")
            st.plotly_chart(fig_map,use_container_width=True)
        def create_map_alt(partial_ds):
            center_lat, center_lon = partial_ds['latitude'].mean(), partial_ds['longitude'].mean()
            st.pydeck_chart(pdk.Deck(
                map_style= None,
                # map_style='mapbox://styles/mapbox/satellite-streets-v11',
                initial_view_state=pdk.ViewState(
                    latitude=center_lat,
                    longitude=center_lon,
                    zoom=25,
                    pitch=50,
                ),
                layers=[
                    pdk.Layer(
                        'ScatterplotLayer',
                        # data=partial_ds[['lat','lon']],
                        data=partial_ds,
                        get_position='[longitude, latitude]',
                        get_color='[26, 255, 0, 160]',
                        get_radius=0.25,
                        pickable=True,  # to show tooltip
                    ),
                ],
                tooltip={
                    # "html": "Lat: {lat} <br/> Long:{lon}",
                    # create 0s for the options when not selected
                    "html": "Lat: {latitude} <br/> Long:{longitude} <br/> Time: {Time}",
                    "style": {
                        "backgroundColor": "blue",
                        "color": "white"
                    }
                }
            ))
        def create_map(data):


            # Create a map centered around an average coordinate
            if not data.empty:
                center_lat, center_lon = data['latitude'].mean(), data['longitude'].mean()
            else:
                # Default to some location if there's no data
                center_lat, center_lon = 0, 0

            # Start map at the computed average location
            my_map = folium.Map(location=[center_lat, center_lon],
                                zoom_start=18,
                                control_scale=True,
                                prefer_canvas=True)

            # Add points from the data
            n_rows = len(data.index)
            for index, item in data.iterrows():
                tooltip = (
                    f"Date: {item.get('Date', 'N/A')} <br/> Time: {item.get('Time', 'N/A')} <br/>"
                    # f"Chl (ug/L): {item.get('Chl (ug/L)', 'N/A')}, BGA-PE (ug/L): {item.get('BGA-PE (ug/L)', 'N/A')}, \n"
                    # f"Turb (FNU): {item.get('Turb (FNU)', 'N/A')}, TSS (mg/L): {item.get('TSS (mg/L)', 'N/A')}, \n"
                    # f"ODO (%sat): {item.get('ODO (%sat)', 'N/A')}, ODO (mg/l): {item.get('ODO (mg/l)', 'N/A')}, \n"
                    # f"Temp (C): {item.get('Temp (C)', 'N/A')}, Cond (uS/cm): {item.get('Cond (uS/cm)', 'N/A')}, \n"
                    # f"Sal (PPT): {item.get('Sal (PPT)', 'N/A')}, Pressure (psi a): {item.get('Pressure (psi a)', 'N/A')}, \n"
                    f"Depth (m): {item.get('Depth (m)', 'N/A')} <br/> latitude: {item.get('latitude', 'N/A')} <br/>"
                    f"longitude: {item.get('longitude', 'N/A')}"
                )
                normal_marker=folium.Marker(
                    [item['latitude'], item['longitude']],
                    tooltip=tooltip,
                )
                circle_marker=folium.Circle(location=[item['latitude'], item['longitude']],
                              radius=0.3,
                              color='orange',
                              tooltip=tooltip,
                              fill=True)
                icon = folium.CustomIcon(
                    image_,
                    icon_size=(30, 45),
                    # icon_anchor=(22, 94),
                )
                swarm_marker = folium.Marker(
                    [item['latitude'], item['longitude']],
                    tooltip=tooltip,
                    icon=icon
                )

                if index != n_rows - 1:
                    circle_marker.add_to(my_map)
                else:
                    swarm_marker.add_to(my_map)
            return my_map
        # data= fetch_latest_data_iot(st.session_state['collection'])

        def plotFinally():
            my_map = create_map(df)  # Create the map
            folium_static(my_map,width=1200, height=800)

        def interactiveMap():
            my_map2 = create_map(df)  # Create the map
            st_folium(my_map2,key="interactive", use_container_width=True)  # width=1550, height=800

        with st.container():
            st.subheader("Updating Live 📊")
            plotFinally()
        with st.container():
            st.subheader("Interactive Map 🗺️")
            interactiveMap()

    if menu == "Charts - Real Time Visualization":

        variables_to_plot = ['Temp (C)', 'Chl (ug/L)', 'BGA-PE (ug/L)', 'Turb (FNU)', 'TSS (mg/L)',
                             'ODO (%sat)', 'ODO (mg/l)', 'Cond (uS/cm)',
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
    st.divider()
else:
    st.error("No collection selected or session expired.")
    st.button("Go Back", on_click=st.switch_page, args=("streamlit_app.py",))

with bottom():
    st.divider()
    st.write("This project is conducted by the MARINE Lab in collaboration with Boswell Lab and Mora Lab for the FDEP project. The goal of this initiative is to advance our understanding and management of marine ecosystems through innovative data analysis and visualization techniques.")
