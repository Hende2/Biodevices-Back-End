# /c:/Users/Jamie/Documents/GitHub/Back-End/river identification/__init__.py
import read_rivers as rr
import get_satellite_images as gsi
import identification as id


def main(shapefile, river_name_column, river_name, n):
    try:
        # Read river data from file
        riverpoints = rr.extract_river_coordinates(shapefile, river_name_column, river_name)
        
    except Exception as e:
        print(f"Error: {e}")
    
    for i in range(riverpoints):
        try:
            # Save satellite image
            gsi.save_satellite_image(
                latitude=riverpoints["Latitude"][i],
                longitude=riverpoints["Longitude"][i],
                output_path=f"river_{i}.png",
                zoom_level=21
            )
            print(f"\nSatellite image {i} saved successfully!")
        except Exception as e:
            print(f"Error: {e}")
            
        try:
            #do the river identification
            id.kclustering(f"river_{i}.png")
        except Exception as e: 
            print(f"Error: {e}")
        
        try:
            #do the river identification using contours
            id.contouring(f"river_{i}.png")
        except Exception as e: 
            print(f"Error: {e}")
        
            
    # get_map_image(
    # latitude: float,  # lat of centre 
    # longitude: float,  # long of centre
    # zoom_level: int = 21,  # default to maximum zoom
    # api_key: Optional[str] = None,
    # image_size: Tuple[int, int] = (640, 640)
    # )

# Example usage
shapefile = "c:/Users/Jamie/Documents/GitHub/Back-End/river identification/WatercourseLink.shp"  # File path
river_name_column = "name1"  # Select the column containing the river names
river_name = "Burn of Sulerdale"  # Specific river
main(shapefile, river_name_column, river_name, 5)