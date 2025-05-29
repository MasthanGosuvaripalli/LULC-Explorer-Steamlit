
from matplotlib.colors import ListedColormap
import pystac_client
from shapely.geometry import box
import time
import numpy as np
import pandas as pd
import planetary_computer
import rasterio as rio
import rasterio.features
import stackstac
from odc.stac import load
import rioxarray as rxr
import geopandas as gpd

from exactextract import exact_extract


import plotly.express as px

# Custom RGBA color mapping
rgba_colors = {
    0: (0, 0, 0, 0),
    1: (65, 155, 223, 255),
    2: (57, 125, 73, 255),
    3: (0, 0, 0, 255),
    4: (122, 135, 198, 255),
    5: (228, 150, 53, 255),
    6: (0, 0, 0, 255),
    7: (196, 40, 27, 255),
    8: (165, 155, 143, 255),
    9: (168, 235, 255, 255),
    10: (97, 97, 97, 255),
    11: (227, 226, 195, 255)
}



values_to_label={0: 'No Data',
 1: 'Water',
 2: 'Trees',
 4: 'Flooded vegetation',
 5: 'Crops',
 7: 'Built area',
 8: 'Bare ground',
 9: 'Snow/ice',
 10: 'Clouds',
 11: 'Rangeland'}

# Function to convert RGBA to hex
def rgba_to_hex(rgba):
    return '#{:02x}{:02x}{:02x}'.format(rgba[0], rgba[1], rgba[2])



def get_items_from_stac(year, dist_df,status_callback=print):
    ''' 
    Function to get LULC and colourmap from STAC for a given year and district geometry.
        
    Args:
        year (int): The year for which to fetch the data.
        dist_df (GeoDataFrame): A GeoDataFrame containing the district geometry.
    
    Returns:
        xarray.DataArray: DataArray containing the LULC data for the specified year 
        cmap: ListedColormap for LULC class visualization
    '''

    # Connect to the Planetary Computer STAC API
    catalog = pystac_client.Client.open(
        "https://planetarycomputer.microsoft.com/api/stac/v1",
        modifier=planetary_computer.sign_inplace,
    )


    bbox_of_interest = dist_df.total_bounds.tolist()


    search = catalog.search(
        collections=["io-lulc-annual-v02"],
        bbox=bbox_of_interest,
        datetime=f"{year}-01-01/{year}-12-31",
        max_items=1
    )
    status_callback("1. Got the catalog...")
    items = search.item_collection()

    # Load the item as an xarray DataArray

    stack=load(items, chunks={"x": 1024, "y": 1024})
    crs_stack=stack['spatial_ref'].values

    status_callback("2. Reprojecting district...")
    dist_df=dist_df.to_crs(stack['spatial_ref'].values)

    time.sleep(2)
    status_callback("3. Clipping to district...")
    #Crop using bounding box (very fast & memory efficient)
    minx, miny, maxx, maxy = dist_df.total_bounds
    print(f'crs of dist is {dist_df.crs} nad bounds {dist_df.total_bounds}')
    stack_bbox = stack.rio.clip_box(minx=minx, miny=miny, maxx=maxx, maxy=maxy)


    stack_bbox=stack_bbox.compute()
    stack_bbox['spatial_ref']=stack['spatial_ref'].values

    status_callback("4. Extracting stats...")
    df=exact_extract(stack['data'],dist_df, ["unique", "frac"],
                    output='pandas' ).explode(["unique", "frac"])
    
    # Map numeric class codes to labels
    df['class_label'] = df['unique'].astype(int).map(values_to_label)

    # Convert to percent
    df['frac'] = df['frac'] * 100
    status_callback("5. Stats are ready to serve")
    # Add hex color column
    df["color"] = df["unique"].astype(int).map(lambda u: rgba_to_hex(rgba_colors[u]))



    return df

