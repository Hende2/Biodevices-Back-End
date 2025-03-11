import requests
import os
from typing import Tuple, Optional, Dict
from config import GOOGLE_MAPS_API_KEY
import cv2
import numpy as np
from datetime import datetime

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

def get_map_image(
    latitude: float,  # lat of centre 
    longitude: float,  # long of centre
    zoom_level: int = 21,  # default to maximum zoom
    api_key: Optional[str] = None,
    image_size: Tuple[int, int] = (640, 640)
) -> Tuple[bytes, Dict[str, float]]:
    """
    Get a Google Maps static image centered on a coordinate with a specified zoom level.
    
    Args:
        latitude (float): Latitude of the center point
        longitude (float): Longitude of the center point
        zoom_level (int): Zoom level (0-21, default 21 for maximum detail)
        api_key (str, optional): Google Maps API key
        image_size (tuple): Size of the output image in pixels (width, height)
    
    Returns:
        tuple: (image_data, metadata)
    """
    # Get API key from config or environment if not provided
    if api_key is None:
        api_key = GOOGLE_MAPS_API_KEY or os.getenv('GOOGLE_MAPS_API_KEY')
        if not api_key:
            raise ValueError("Google Maps API key not provided and not found in config or environment variables")
    
    # Ensure zoom level is within valid range
    zoom_level = max(0, min(21, zoom_level))
    
    # Calculate image metadata
    metadata = calculate_image_metadata(latitude, longitude, zoom_level, image_size)
    
    # Construct the URL for the Static Maps API
    base_url = "https://maps.googleapis.com/maps/api/staticmap"
    
    # Request a taller image to account for the attribution
    request_height = image_size[1] + 40
    
    # Parameters for the API request
    params = {
        'center': f"{latitude},{longitude}",
        'zoom': zoom_level,
        'size': f"{image_size[0]}x{request_height}",
        'maptype': 'satellite',
        'key': api_key,
        'scale': 5  # Request 2x resolution for better quality
    }
    
    # Make the request
    response = requests.get(base_url, params=params)
    response.raise_for_status()  # Raise an exception for bad status codes
    
    # Crop the Google attribution from the bottom and resize to desired dimensions
    return crop_and_resize_image(response.content, image_size), metadata

def crop_and_resize_image(image_data: bytes, target_size: Tuple[int, int]) -> bytes:
    ''' gets rid of the google maps logo/copyright shit at the bottom
    so we can piece the images together '''
    
    # Convert bytes to numpy array
    nparr = np.frombuffer(image_data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    # Crop the bottom 40 pixels (where the attribution is)
    height = img.shape[0]
    cropped_img = img[0:height-40, :]
    
    # Resize to target dimensions
    resized_img = cv2.resize(cropped_img, target_size)
    
    # Convert back to bytes
    _, buffer = cv2.imencode('.png', resized_img)
    return buffer.tobytes()

def save_map_image(
    latitude: float,
    longitude: float,
    output_path: str,
    zoom_level: int = 21,  # default is maximum zoom
    api_key: Optional[str] = None,
    image_size: Tuple[int, int] = (640, 640)):
 
    image_data, metadata = get_map_image(
        latitude=latitude,
        longitude=longitude,
        zoom_level=zoom_level,
        api_key=api_key,
        image_size=image_size
    )
    
    with open(output_path, 'wb') as f:
        f.write(image_data)
    
    # Print metadata
    print(f"\nImage Metadata:")
    print(f"Zoom Level: {zoom_level}")
    print(f"Meters per pixel: {metadata['meters_per_pixel']:.2f}")
    print(f"Image width: {metadata['width_meters']:.1f} meters")
    print(f"Image height: {metadata['height_meters']:.1f} meters")
    print(f"Total area covered: {metadata['area_square_meters']:.1f} square meters")

# Example 
if __name__ == "__main__":
    lat, lon = 51.37851635187733, -2.3289445443237153
    
    try:
        # Save the map image using API key from config
        save_map_image(
            latitude=lat,
            longitude=lon,
            zoom_level=18,  # maximum zoom for highest detail
            output_path="my_house.png"
        )
        print(f"\nMap image saved successfully!")
    except Exception as e:
        print(f"Error: {e}") 