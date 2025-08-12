

import pandas as pd
import plotly.express as px
import json

# Load your GeoJSON data
with open('National_Forest_Boundaries.geojson') as f:
    geojson_data = json.load(f)


# Assuming you have a DataFrame with data linked to your GeoJSON features
# For example, if your GeoJSON features have an 'id' property and your DataFrame has a matching 'location_id' column
df = pd.read_csv('FS_National_Forests_Dataset_csv.csv')

print(df.columns)




# campgrounds
campground_df = pd.read_csv('Campgrounds_CA_GeoLoc.csv')


#lakes
with open ('California_Lakes.geojson') as f:
    lakes_geojson = json.load(f)

lakes_df = pd.DataFrame([[feature["properties"]["LAT_NAD83"],feature["properties"]["LON_NAD83"],\
                        feature["properties"]["NAME"], feature["properties"]["QUAD_NAME"],\
                        feature["properties"]["elev_ft"],feature["properties"]["COUNTY"]] \
                        for feature  in lakes_geojson['features']],  \
                        columns = ['lat', 'lon', 'name', 'quad_name', 'elev_ft', 'county']) 


#hunting zones






import plotly.graph_objects as go


#fig = go.Figure()
#

fig = px.choropleth_mapbox(
    #df,
    geojson=geojson_data,
    locations=[feature["properties"]["OBJECTID"] for feature in geojson_data['features']],  # Column in DataFrame matching GeoJSON feature ID
    featureidkey="properties.OBJECTID",  # Key in GeoJSON features for matching
    #color="GIS_ACRES",  # Column in DataFrame for coloring the MultiPolygons
    mapbox_style="carto-positron",
    zoom=7,
    center={"lat": 38, "lon": -120},  # Adjust center as needed
    opacity=0.5
)

fig.add_trace(
    go.Choroplethmapbox(
        geojson=geojson_data,
        locations=[feature["properties"]["OBJECTID"] for feature in geojson_data['features']],
        featureidkey="properties.OBJECTID",
        #color="GIS_ACRES",
        #mapbox_style="carto-positron",
        #zoom=7,
        #center={"lat": 38, "lon": -120},
        #opacity=0.5
    )
)


fig.add_trace(
    go.Scattermapbox(
        lat=lakes_df['lat'],
        lon=lakes_df['lon'],
        mode='markers',
        marker={"size": 3, "color": "blue"},
        text=lakes_df['name'],
        name='Lakes'
    )



)
fig.add_trace(
    go.Scattermapbox(
        lat=campground_df['y'],
        lon=campground_df['x'],
        mode='markers',
        marker={"size": 3, "color": "red"},
        text=campground_df['UNITNAME'],
        name='Campgrounds'
    )
)

fig.update_layout(
    #mapbox_style="carto-positron",
    mapbox_style = "open-street-map",
        mapbox_zoom=7,
        
        mapbox_center={"lat": 42.5887, "lon": -128.00} # Center the map
    )

fig.show()

