import folium
from folium.plugins import Draw
import streamlit as st

from streamlit_folium import st_folium

st.set_page_config(
    page_title="ARBormics-KG Worldmap",
    layout="wide",
    initial_sidebar_state="expanded"
)

## Queries

geosparql_query = f"""
    prefix sf: <http://www.opengis.net/ont/sf#>
    prefix geo: <http://www.opengis.net/ont/geosparql#>
    
    SELECT ?s 
    WHERE {{
        ?s rdf:type sf:Point ;
        geo:asWKT ?geoMonument .
        
        ?s2 rdf:type sf:Polygon ;
        geo:asWKT ?geoNationalPoly .
        
        FILTER(bif:st_intersects(?geoMonument, ?geoNationalPoly, 0))
    }}
"""


st.title("ABRomics samples worldmap")

st.markdown("")


m = folium.Map(location=[48.85661400, 2.35222190], zoom_start=5)

## Allows to draw shapes on the map
Draw(export=True).add_to(m)

## Renders the folium map in Streamlit the infos about the map are stored in st_data
## st_data is a state
st_data = st_folium(m, width=725)

col1, col2 = st.columns(2)

with col1:
    st.write(st_data)

with col2:
    st.write(st_data["last_active_drawing"])

if st_data["last_active_drawing"] != None:
    st.markdown("draw a polygon on the map to check whether there are samples within the region you are interested in")
    for position in st_data["last_active_drawing"]["geometry"]["coordinates"][0]:
        st.write(position[0])
        st.write(position[1])
