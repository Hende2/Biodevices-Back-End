import os
from google_earth_sat import get_sentinel_image, save_sentinel_image
from google_maps_image import get_map_image

def save_satellite_images(latitude, longitude, n, zoom_level:int = 18):
    # saves recent satellite images and the basic google maps one for comparison
    
    # Create images directory if it doesn't exist
    os.makedirs('images', exist_ok=True)
    
    try:
        # Get and save Sentinel-2 image
        print("\nGetting Sentinel-2 image...")
        save_sentinel_image(
            latitude=latitude,
            longitude=longitude,
            zoom_level=zoom_level,
            output_path=f"images/sentinel2_{n}.png",
            image_size=(640, 640)
        )
        
        # Get and save Google Maps image
        print("\nGetting Google Maps image...")
        image_data, metadata = get_map_image(
            latitude=latitude,
            longitude=longitude,
            zoom_level=zoom_level,
            image_size=(640, 640)
        )
        
        # Save Google Maps image
        with open(f"images/google_maps_{n}.png", 'wb') as f:
            f.write(image_data)
        
        print("\nImages saved in the 'images' directory:")
        print(f"- images/sentinel2_{n}.png")
        print(f"- images/google_maps_{n}.png")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # Example coordinates along the avon
    coords= [(51.38304985779056, -2.357886640213137),
             (51.3792112971465, -2.3655278199062546),
             (51.380955908927966, -2.369569326144386),
             (51.38464483112403, -2.3785772869684405),
             (51.381556264974535, -2.3901158740682407),
             (51.3855979360861, -2.4035207801691496),
             (51.37851635187733, -2.3289445443237153)]
    
    try:
        i = 0
        for c in coords:
            save_satellite_images(c[0], c[1], i)
            i += 1
        
    except Exception as e:
        print(f"Error: {e}") 