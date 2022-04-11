import streamlit as st
import pandas as pd
import pydeck as pdk

# read data
df = pd.read_csv("western_cvi.csv")

# getting unique values for filters
district = df['District'].drop_duplicates()
ds = df['DS'].drop_duplicates()


# adding filters
district_choice = st.sidebar.multiselect('Select district:', district, default=district)
population_choice = st.sidebar.slider('population_2020:', min_value=0.0, max_value=30000.0, step=500.0, value=0.0)
poi_count_choice = st.sidebar.slider('poi_count_choice:', min_value=0, max_value=50, step=2, value = 0)


# assign filters to the dataframe
df = df[df['District'].isin(district_choice)]
df = df[df['poi_count'] >= poi_count_choice]
df = df[df['population_2020'] >= population_choice]

# color coding
def color_selector(norm_score):
    if norm_score >= .8:
        col = [71, 45, 48]
    elif norm_score >= .6:
        col = [114, 61, 70]
    elif norm_score >= .4:
        col = [226, 109, 92]
    elif norm_score >= .2:
        col = [255, 225, 168]
    else:
        col = [201, 203, 163]

    return col

# applying color coding function
df['color'] = df['norm_score'].apply(color_selector)

# Define a layer to display on a map
layer = pdk.Layer(
    "H3HexagonLayer",
    df,
    pickable=True,
    stroked=True,
    filled=True,
    extruded=False,
    get_hexagon="h3",
    get_fill_color="color",
    #get_fill_color="[((10-rank)/5)*55, 255, ((10-rank)/3)*75]",
    opacity = .5,
    #get_fill_color="color",
    get_line_color=[255, 255, 255],
    line_width_min_pixels=1,
)

# Set the viewport location
view_state = pdk.ViewState(latitude=6.9271, longitude=79.8612, zoom=10, bearing=0, pitch=0)


# Render
r = pdk.Deck(layers=[layer], initial_view_state=view_state,map_style='road',tooltip={"text": "Score: {norm_score} \nGN: {GN} \npopulation: {population_2020}"})


# Creating visual layer
st.title(f"City Vitality Index")
st.markdown('Geo view')
st.write(r)
st.markdown('Table')

st.dataframe(df.sort_values('score',
             ascending=False).reset_index(drop=True))
