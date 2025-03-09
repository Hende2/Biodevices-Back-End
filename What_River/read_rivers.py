import geopandas as gpd
import pandas as pd

def extract_river_coordinates(shapefile, river_name_column, river_name):
    """
    Extract longitude and latitude of points from a river LineString geometry in a Shapefile.

    Parameters:
        shapefile (str): Path to the Shapefile (.shp).
        river_name_column (str): Column name containing river names.
        river_name (str): The river name to filter by.

    Returns:
        pd.DataFrame: A DataFrame containing latitude and longitude points along the river.
    """
    # Load dataset
    gdf = gpd.read_file(shapefile)

    # Filter dataset for the specified river
    river_gdf = gdf[gdf[river_name_column] == river_name]

    # Ensure the geometry is in WGS84 (EPSG:4326)
    river_gdf = river_gdf.to_crs(epsg=4326)

    # Extract coordinates from LineString geometries
    coords = []
    for geom in river_gdf.geometry:
        if geom.geom_type == "LineString":  # If the river is stored as a LineString
            for point in geom.coords:
                coords.append({"Latitude": point[1], "Longitude": point[0]})
        elif geom.geom_type == "MultiLineString":  # If the river has multiple segments
            for line in geom.geoms:
                for point in line.coords:
                    coords.append({"Latitude": point[1], "Longitude": point[0]})

    return pd.DataFrame(coords)



# Example usage
shapefile = "WatercourseLink.shp"  # File path
river_name_column = "name1"  # Select the column containing the river names
river_name = "Burn of Sulerdale"  # Specific river
    
coordinates_gdf = extract_river_coordinates(shapefile, river_name_column, river_name)
print(coordinates_gdf)