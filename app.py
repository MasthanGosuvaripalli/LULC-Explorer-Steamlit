import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt     

import geopandas as gpd
import streamlit as st     
import rasterio as rio
import plotly.express as px

### STAC planetary library
from utils.utils import get_items_from_stac

with st.sidebar:
    st.header("📊 ESA LULC Explorer🌏")

    st.markdown("""
    This app lets you:

    - 🗺️ **Select any Indian state and district**
    - 🛰️ **View ESA Land Use Land Cover (LULC)** stats from **2017–2024**
    - 📈 **Visualize class-wise percentage distribution**
    - 🧠 Understand **spatial land use patterns** for agriculture, urban, forest, and water bodies.

    ---
    **Instructions:**
    1. Select a **State** and **District**
    2. Click **Submit**
    3. View the map
    4. Choose a **LULC Year**
    5. Click **Generate LULC Chart**

    Stats are fetched dynamically from Microsoft's Planetary Computer using **STAC API**.

    📬 For queries, contact: `masthanwali1234@gmail.com`
    """)

    with st.expander("ℹ️ STAC Collection Details"):
        st.markdown("""
        **Collection**:  
        [io-lulc-annual-v02](https://planetarycomputer.microsoft.com/api/stac/v1/collections/io-lulc-annual-v02)
        [link](https://planetarycomputer.microsoft.com/dataset/io-lulc-annual-v02)
                    
        **Data Providers**:
            - **Esri** *(Licensor)*
            - **Microsoft** *(Host)*

        **License**:  
        [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
        """)


st.title("🗺️ Distwise ESA LULC Data Visualization App 🚀 ")
st.write("This app allows you to visualize LULC class stats using Streamlit.")

@st.cache_data()
def load_data():
    return gpd.read_file('data/2011_Dist.shp')

# Load shapefile
gdf = load_data()

# Initialize state
if "submitted" not in st.session_state:
    st.session_state["submitted"] = False

# UI: Select State and District
states = gdf['ST_NM'].unique()
selected_state = st.selectbox('Select a State', states)
districts = gdf[gdf['ST_NM'] == selected_state]['DISTRICT'].unique()
selected_dist = st.selectbox(f'Select a District from {selected_state}', districts)

# Filter GeoDataFrame
dist_df = gdf[(gdf['ST_NM'] == selected_state) & (gdf['DISTRICT'] == selected_dist)]
dist_df_proj = dist_df.to_crs(epsg=4326)

# --- Submit Button ---
if st.button("Submit"):
    st.session_state["submitted"] = True
    st.session_state["selected_state"] = selected_state
    st.session_state["selected_dist"] = selected_dist
    st.session_state["dist_df"] = dist_df
    st.session_state["year_selected"] = None  # Reset year on new submit

# --- Display Plotly Map ---
if st.session_state["submitted"]:
    dist_df = st.session_state["dist_df"]
    dist_df_proj = dist_df.to_crs(epsg=4326)
    geojson = dist_df_proj.__geo_interface__

    fig = px.choropleth_mapbox(
        dist_df_proj,
        geojson=geojson,
        locations=dist_df_proj.index,
        color_discrete_sequence=["blue"],
        labels={'DISTRICT':'District name'},
        mapbox_style="carto-positron",
        center={
            "lat": dist_df_proj.geometry.centroid.y.values[0],
            "lon": dist_df_proj.geometry.centroid.x.values[0],
        },
        zoom=7.5,
        opacity=0.5,
    )
    fig.update_layout(margin={"r":0, "t":0, "l":0, "b":0})
    st.plotly_chart(fig, use_container_width=True)

    # --- Select Year ---
    years_list = ['2017','2018','2019','2020', '2021', '2022', '2023', '2024']
    selected_year = st.selectbox('Select a Year for LULC', years_list)

    if st.button("Generate LULC Chart"):
        st.session_state["year_selected"] = selected_year

# --- Show Chart ---
if st.session_state.get("year_selected"):
    dist_df = st.session_state["dist_df"]
    selected_year = st.session_state["year_selected"]
    selected_dist = st.session_state["selected_dist"]
    with st.spinner("Please wait (dont rerun Generate LULC)...", show_time=True):
        with st.status('Running LULC stats generation ...',expanded=False) as status:


            def update(msg):
                st.write(msg)
            status.update(
                label="Drop down for ongoing Steps !", state="complete", expanded=False)
            # Get LULC Data
            df = get_items_from_stac(year=selected_year, dist_df=dist_df,status_callback=update)
            df = df.sort_values("frac", ascending=False)

            labels = df["class_label"].values
            values = df["frac"].values
            colors = df["color"].values

            fig, ax = plt.subplots(figsize=(14, 8))
            bars = ax.bar(labels, values, color=colors, edgecolor='black')

            for bar in bars:
                height = bar.get_height()
                ax.annotate(f'{height:.2f}%', 
                            xy=(bar.get_x() + bar.get_width() / 2, height),
                            xytext=(0, 3),
                            textcoords="offset points",
                            ha='center', va='bottom')

            ax.set_title(f"{selected_dist} - {selected_year} LULC Class-wise % Distribution ")
            ax.set_xlabel("Land Cover Class")
            ax.set_ylabel("Percentage (%)")
            plt.xticks(rotation=30,)
    st.success("Done! Thanks for Patience ")
    st.pyplot(fig)
