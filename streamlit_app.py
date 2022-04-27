##### This app maps out the ski resorts with tool tips that provide summary information

import streamlit as st
import pydeck as pdk
import pandas as pd
import matplotlib.pyplot as plt

##### Title and intro

st.title( 'Ski Resort Dashboard' )
st.write( '''
This dashboard has dual functionality. If you are interested in learning what resorts
you can ski on an Epic or Ikon pass, filter the map and explore resort info for both.
If you are interested in the snowfall history of a particular resort, take a look at 
the Average Annual Snowfall graph below.
''' )


##### Inputs

st.header( 'Resort Map' )
st.write( '''
The map below provides information on ski resorts that belong to the Epic or Ikon passes.
''' )
pass_input = st.radio('Which pass are you interested in?', ['Epic', 'Ikon'])


##### Output
MAPKEY = {"mapbox": "pk.eyJ1IjoicGhlbmV5OTkiLCJhIjoiY2wyZ3RyN2o2MDNkcTNkbW11MWFpZjhvdCJ9.dgUEOaTXqL6eQYigFlUEUQ"}
#Filter the dataframe on the pass column based on user input
df_map=pd.read_csv('/work/Map_Data.csv')
df_map2 = df_map[df_map['Pass'] == pass_input]

#Set the view state for starting position
vstate = pdk.ViewState(
   latitude = df_map2['Resort_Lat'].mean(),
   longitude = df_map2['Resort_Long'].mean(),
   zoom=1,
   pitch=0)

#Create the layer of resort markings
layer1 = pdk.Layer("ScatterplotLayer",
   data=df_map2,
   get_position="[Resort_Long, Resort_Lat]",
   get_radius = 10000,
   opacity = 0.4,
   get_color=(0,0,250),
   pickable=True)

#Create a tooltip
tool_tip = {"html": "Resort Name: {Resort} <br /> Vertical Drop: {Vertical Drop} <br /> Skiable Terrain: {Skiable Terrain} <br /> Average Snowfall: {Average Snowfall}",
            "style": {"backgroundColor":"white", "color":"blue"}}

#Create the map
map1 = pdk.Deck(
   map_style='mapbox://styles/mapbox/light-v9',
   initial_view_state=vstate,
   tooltip=tool_tip,
   api_keys=MAPKEY,
   layers=[layer1])

st.pydeck_chart(map1)

###This new section will allow a user to select a resort and see a graphical depiction 
###of its annual snowfall history.

st.header('Annual Snowfall by Resort')
st.write('The graph below will display the past decade of annual snowfall data.')

#Import the annual data and create a resort list
df_graph = pd.read_csv('/work/Graph_Data.csv')
resort_list = list(df_graph['Resort'].unique())
resort_list_sorted = sorted(resort_list)

#Allow the user to select a resort
resort_input = st.selectbox('Which resort are you interested in?', resort_list_sorted)

#Graph the data as a bar chart
data_to_graph = df_graph[df_graph['Resort'] == resort_input][['Year', 'Total Snowfall']]
xs = list(data_to_graph['Year'])
ys = list(data_to_graph['Total Snowfall'])
fig, ax = plt.subplots()
plt.xticks(rotation = 45, ha = 'right', rotation_mode = 'anchor')
plt.xlabel('Ski Season')
plt.ylabel('Total Snowfall (Inches)')
ax.bar(xs, ys)
st.pyplot(fig)
