import ee
import datetime
import numpy as np
import matplotlib.pyplot as plt
import cv2
from typing import Tuple, Dict
import urllib.request
from PIL import Image
import io
import sys
import os

# Add the current directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from google_maps_image import get_map_image

def calculate_image_metadata(
    latitude: float,
    longitude: float,
    zoom_level: int,
    image_size: Tuple[int, int]) -> Dict[str, float]:
 
    # Earth's radius in meters
    R_MAJOR = 6378137.0
    R_MINOR = 6356752.3142
    RATIO = R_MINOR / R_MAJOR
    
    # Calculate meters per pixel at the equator
    meters_per_pixel = 156543.03392 * np.cos(np.radians(latitude)) / (2 ** zoom_level)
    
    # Adjust for latitude (pixels get smaller as you move away from equator)
    meters_per_pixel *= np.sqrt(1 - (RATIO * np.sin(np.radians(latitude))) ** 2)
    
    # Calculate total area covered by the image
    width_meters = meters_per_pixel * image_size[0]
    height_meters = meters_per_pixel * image_size[1]
    area_square_meters = width_meters * height_meters
    
    return {
        'meters_per_pixel': meters_per_pixel,
        'width_meters': width_meters,
        'height_meters': height_meters,
        'area_square_meters': area_square_meters
    }

# Initialize the Earth Engine API
ee.Initialize(project='biodevices-without-borders')

def get_sentinel_image( # get the most recent sentinel-2 image
    latitude: float,
    longitude: float,
    zoom_level: int,
    image_size: Tuple[int, int] = (640, 640) ) -> Tuple[np.ndarray, Dict[str, float]]:

    # Define the time range (last 7 days)
    end = ee.Date(datetime.datetime.now())
    start = end.advance(-7, 'day')

    # Create an image collection of Sentinel-2 images for the past week
    s2 = ee.ImageCollection("COPERNICUS/S2_SR") \
        .filterDate(start, end) \
        .filterBounds(ee.Geometry.Point([longitude, latitude])) \
        .sort('system:time_start', False)

    # Get the most recent image
    image = s2.first()

    # Get the image date
    image_date = image.get('system:time_start').getInfo()
    image_date = datetime.datetime.fromtimestamp(image_date/1000).strftime('%Y-%m-%d %H:%M:%S')
    print(f"\nSentinel-2 image acquisition date: {image_date}")

    # Define visualization parameters
    vis_params = {
        'bands': ['B4', 'B3', 'B2'],  # Red, Green, Blue bands for true color
        'min': 2000,    # Adjusted to better capture the dynamic range
        'max': 4500,    # Adjusted to prevent overexposure
        'gamma': 1.1    # Slightly reduced gamma for better mid-tone detail
    }

    # Select bands (B4, B3, B2 for true color)
    image = image.select(['B4', 'B3', 'B2'])

    # Calculate buffer size based on zoom level
    meters_per_pixel = 156543.03392 * np.cos(np.radians(latitude)) / (2 ** zoom_level)
    buffer_meters = meters_per_pixel * max(image_size) / 2  # Half the image size in meters

    # Create a region of interest around the point
    point = ee.Geometry.Point([longitude, latitude])
    roi = point.buffer(buffer_meters)

    # Get the image data as a numpy array
    image_data = image.sampleRectangle(roi)
    image_data = image_data.getInfo()
    
    # Extract band data from properties
    bands = ['B4', 'B3', 'B2']
    image_arrays = []
    for band in bands:
        if band in image_data['properties']:
            band_data = np.array(image_data['properties'][band])
            image_arrays.append(band_data)
        else:
            print(f"Warning: Band {band} not found in image data")
            print("Available properties:", image_data['properties'].keys())
    
    if not image_arrays:
        raise ValueError("No valid band data found in the image")
    
    # Stack bands into RGB image
    image_array = np.stack(image_arrays, axis=-1)
    
    # Print value ranges for debugging
    print("\nValue ranges before normalization:")
    for i, band in enumerate(bands):
        print(f"{band}: min={np.min(image_array[:,:,i]):.1f}, max={np.max(image_array[:,:,i]):.1f}")
    
    # Clip values to valid range and normalize
    image_array = np.clip(image_array, vis_params['min'], vis_params['max'])
    image_array = (image_array - vis_params['min']) / (vis_params['max'] - vis_params['min'])
    
    # Apply gamma correction
    image_array = np.power(image_array, 1/vis_params['gamma'])
    
    # Apply contrast enhancement
    image_array = np.clip(image_array * 1.2, 0, 1)  # Increase contrast by 20%
    
    # Resize to target dimensions
    image_array = cv2.resize(image_array, image_size)
    
    # Calculate metadata
    metadata = calculate_image_metadata(latitude, longitude, zoom_level, image_size)
    
    return image_array, metadata

def save_sentinel_image(
    latitude: float,
    longitude: float,
    zoom_level: int,
    output_path: str,
    image_size: Tuple[int, int] = (640, 640)):
   
    image_data, metadata = get_sentinel_image(
        latitude=latitude,
        longitude=longitude,
        zoom_level=zoom_level,
        image_size=image_size
    )
    
    # Save the image
    plt.imsave(output_path, image_data)
    
    # Print metadata
    print(f"\nImage Metadata:")
    print(f"Meters per pixel: {metadata['meters_per_pixel']:.2f}")
    print(f"Image width: {metadata['width_meters']:.1f} meters")
    print(f"Image height: {metadata['height_meters']:.1f} meters")
    print(f"Total area covered: {metadata['area_square_meters']:.1f} square meters")


# Example 
if __name__ == "__main__":
    # Example coordinates 
    lat, lon = 51.37851635187733, -2.3289445443237153
    
    try:
        # Get  satellite image
        save_sentinel_image(
            latitude=lat,
            longitude=lon,
            zoom_level=15,
            output_path="sentinel2.png",
            image_size=(640, 640)
        )
    except Exception as e:
        print(f"Error: {e}")

        def get_sentinel_image(
            latitude: float,
            longitude: float,
            zoom_level: int,
            image_size: Tuple[int, int] = (640, 640)) -> Tuple[np.ndarray, Dict[str, float]]:

            # Use Google Maps Static API to get the image
            image_url = get_map_image(latitude, longitude, zoom_level, image_size)
            with urllib.request.urlopen(image_url) as url:
                image_data = url.read()

            # Convert image data to numpy array
            image = Image.open(io.BytesIO(image_data))
            image_array = np.array(image)

            # Normalize the image array
            image_array = image_array / 255.0

            # Calculate metadata
            metadata = calculate_image_metadata(latitude, longitude, zoom_level, image_size)

            return image_array, metadata