import folium
from folium.plugins import HeatMap  # Import HeatMap from plugins
import numpy as np
import time
import threading
import http.server
import socketserver
import os

class LiveHeatmapServer:
    def __init__(self, map_center=(0, 0), zoom_start=2, update_interval=5, map_file="live_map.html"):
        self.map_center = map_center
        self.zoom_start = zoom_start
        self.update_interval = update_interval
        self.map_file = map_file
        self.running = False
        self.port = 8000

    def generate_random_data(self):
        """
        Simulates data for heatmap.
        Returns a list of tuples [(lat, lon, value), ...].
        """
        return [(np.random.uniform(-90, 90), np.random.uniform(-180, 180), np.random.uniform(1, 100)) for _ in range(100)]

    def update_map(self):
        """
        Updates the heatmap and saves it to an HTML file.
        """
        while self.running:
            try:
                # Generate new data
                data = self.generate_random_data()
                locations = [[lat, lon] for lat, lon, _ in data]
                weights = [value for _, _, value in data]

                # Create a new folium map
                m = folium.Map(location=self.map_center, zoom_start=self.zoom_start)
                HeatMap(locations, radius=15, blur=10, max_zoom=1).add_to(m)

                # Save the updated map
                m.save(self.map_file)
                print("Map updated!")

                # Wait before the next update
                time.sleep(self.update_interval)
            except Exception as e:
                print(f"Error updating map: {e}")

    def start_server(self):
        """
        Starts the local HTTP server to serve the map.
        """
        os.chdir(os.path.dirname(os.path.abspath(self.map_file)))
        handler = http.server.SimpleHTTPRequestHandler
        with socketserver.TCPServer(("", self.port), handler) as httpd:
            print(f"Serving map at http://localhost:{self.port}")
            httpd.serve_forever()

    def start(self):
        """
        Start the heatmap updates and the server.
        """
        self.running = True
        threading.Thread(target=self.update_map, daemon=True).start()
        self.start_server()

    def stop(self):
        """
        Stop the live updates.
        """
        self.running = False


# Run the application
if __name__ == "__main__":
    live_map = LiveHeatmapServer(map_center=(0, 0), zoom_start=2, update_interval=5)
    try:
        live_map.start()
    except KeyboardInterrupt:
        live_map.stop()
        print("Stopped the server.")



#------------------------
#attempt to add 3d aspect
#-------------------------
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
from mpl_toolkits.mplot3d import Axes3D
import threading

class Heatmap3D:
    def __init__(self):
        # Initialize a figure for live updates
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.is_running = False

    # def generate_heatmap_3d(self, locations, values, elevations, grid_size=100, colormap='viridis'):
    #     """
    #     Generates and updates the 3D heatmap based on the input locations, values, and elevations. add a way for it to import data in in the future
    #     Parameters:
    #     locations: List of tuples [(lat1, lon1), (lat2, lon2), ...]
    #     values: List of values [val1, val2, ...]
    #     elevations: List of elevations corresponding to each location
    #     grid_size: Resolution of the grid
    #     colormap: Colormap to use for the heatmap
    #     """
    #     if not locations or not values or not elevations or len(locations) != len(values) or len(values) != len(elevations):
    #         raise ValueError("Locations, values, and elevations must be of the same length and not empty.")

    #     # Convert locations and elevations to arrays
    #     locations = np.array(locations)
    #     values = np.array(values)
    #     elevations = np.array(elevations)

    #     # Create a grid for interpolation
    #     lat = locations[:, 0]
    #     lon = locations[:, 1]
    #     grid_lat, grid_lon = np.linspace(lat.min(), lat.max(), grid_size), np.linspace(lon.min(), lon.max(), grid_size)
    #     #grid_lat, grid_lon = np.meshgrid(grid_lat, grid_lon)

    #     # Interpolate data for values and elevations
    #     grid_values = griddata(locations, values, (grid_lat, grid_lon), method='cubic', fill_value=0)
    #     grid_elevations = griddata(locations, elevations, (grid_lat, grid_lon), method='cubic', fill_value=0)

    #     # Update the 3D heatmap
    #     self.ax.clear()
    #     surf = self.ax.plot_surface(
    #         grid_lon, grid_lat, grid_elevations, 
    #         facecolors=plt.cm.get_cmap(colormap)(grid_values / grid_values.max()),
    #         rstride=1, cstride=1, linewidth=0, antialiased=False, alpha=0.8
    #     )
    #     self.fig.colorbar(plt.cm.ScalarMappable(cmap=colormap), ax=self.ax, orientation='vertical', label="Value")
    #     self.ax.set_xlabel("Longitude")
    #     self.ax.set_ylabel("Latitude")
    #     self.ax.set_zlabel("Elevation")
    #     self.ax.set_title("3D Heatmap")
        

    #     plt.draw()
    #     plt.pause(0.1)
    def generate_heatmap_3d(self, locations, values, elevations, grid_size=100, colormap='viridis'):
        """
        Generates and updates the 3D heatmap based on the input locations, values, and elevations.
        """
        if not locations or not values or not elevations or len(locations) != len(values) or len(values) != len(elevations):
            raise ValueError("Locations, values, and elevations must be of the same length and not empty.")
        
            # Convert locations and elevations to arrays
        locations = np.array(locations)
        values = np.array(values)
        elevations = np.array(elevations)
                
        # Create a grid for interpolation
        lat = locations[:, 0]
        lon = locations[:, 1]
        grid_lat = np.linspace(lat.min(), lat.max(), grid_size)
        grid_lon = np.linspace(lon.min(), lon.max(), grid_size)
        grid_lat, grid_lon = np.meshgrid(grid_lat, grid_lon)
        
        # Interpolate data for values and elevations
        grid_values = griddata(locations, values, (grid_lat, grid_lon), method='cubic', fill_value=0)
        grid_elevations = griddata(locations, elevations, (grid_lat, grid_lon), method='cubic', fill_value=0)
        
        # Update the 3D heatmap
        self.ax.clear()
        self.ax.plot_surface(
            grid_lon, grid_lat, grid_elevations,
            facecolors=plt.cm.get_cmap(colormap)(grid_values / (grid_values.max() if grid_values.max() > 0 else 1)),
            rstride=1, cstride=1, linewidth=0, antialiased=False, alpha=0.8
        )
        self.fig.colorbar(plt.cm.ScalarMappable(cmap=colormap), ax=self.ax, orientation='vertical', label="Value")
        self.ax.set_xlabel("Longitude")
        self.ax.set_ylabel("Latitude")
        self.ax.set_zlabel("Elevation")
        self.ax.set_title("3D Heatmap")
            
        plt.draw()
        plt.pause(0.1)


    def live_update(self, location_func, value_func, elevation_func, update_interval=1):
        """
        Continuously updates the 3D heatmap with live data.

        Parameters:
        location_func: Function that returns the latest location data [(lat, lon), ...]
        value_func: Function that returns the latest value data [val1, val2, ...]
        elevation_func: Function that returns the latest elevation data [elev1, elev2, ...]
        update_interval: Time interval between updates in seconds
        """
        def update():
            self.is_running = True
            while self.is_running:
                locations = location_func()
                values = value_func()
                elevations = elevation_func()
                self.generate_heatmap_3d(locations, values, elevations)
                plt.pause(update_interval)

        thread = threading.Thread(target=update, daemon=True)
        thread.start()

    def stop_live_updates(self):
        """Stops the live updates."""
        self.is_running = False


# Example Usage
if __name__ == "__main__":
    import time

    # Simulated data source
    def generate_locations():
        # Simulate a random scatter of points within a geographic boundary
        return [(np.random.uniform(-90, 90), np.random.uniform(-180, 180)) for _ in range(100)]

    def generate_values():
        # Simulate some random values associated with those points
        return [np.random.uniform(0, 100) for _ in range(100)]

    def generate_elevations():
        # Simulate random elevations
        return [np.random.uniform(0, 5000) for _ in range(100)]

    heatmap = Heatmap3D()

    # # Start live updates
    # try:
    #     heatmap.live_update(generate_locations, generate_values, generate_elevations, update_interval=2)
    #     plt.show()
    # except KeyboardInterrupt:
    #     heatmap.stop_live_updates()



#---------------

