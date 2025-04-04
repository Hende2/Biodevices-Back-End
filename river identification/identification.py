# Necessary Libraries
import cv2
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

# Approach 1: K-Means Clustering
def kclustering(cv2_image):
    '''Using K-Means Clustering to identify a river in a image read by OpenCV
    Input: cv2_image - Image read by OpenCV
    Output: Visualisation of the original image, the segmented image and the river mask
    Possible adjustments: Number of clusters, gaussian blurring, adjustment to the inital state of the KMeans object
    '''
    # Convert to right formats
    image_rgb = cv2.cvtColor(cv2_image, cv2.COLOR_BGR2RGB) # Ensures data is in the correct format as satellite images are often in BGR.
    # Returns object of dimension (height, width, 3) where 3 represents the RGB values of the pixel.
    pixels = image_rgb.reshape(-1, 3) # Reshapes that matrix to a 2d array of height and width linked to the respective RGB values.

    # Apply K-Means Clustering
    kmeans = KMeans(n_clusters=2, random_state=0)  # Choosing 2 clusters as we just want river and not river.
    kmeans.fit(pixels)
    labels = kmeans.labels_ # Labels are the identification for which cluster each pixel belongs to.
    centroids = kmeans.cluster_centers_ # Centroids are the RGB values of the clusters.
    river_cluster = np.argmin(centroids[:, 0] + centroids[:, 1])  # Choose cluster with lowest (R+G) values

    # Now we reshape the labels to the original image dimensions
    segmented_image = labels.reshape(image_rgb.shape[:2])

    # Visualisation
    highlighted_image = np.zeros_like(image_rgb)
    river_mask = (segmented_image == river_cluster).astype(np.uint8) * 255 # Creates mask for the image where river is white and not river is black.

    plt.figure(figsize=(15, 5)) # Arbitrary figure size chosen, can be adjusted as necessary.
    # Subplot 1: Original Image
    plt.subplot(131)  # Numbers mean (1 row, 3 columns, position 1)
    plt.imshow(image_rgb)
    plt.title('Original Image')
    plt.axis('off')  # Hide axes
    # Subplot 2: K-Means Segmented Image, visualises the result of the clustering
    plt.subplot(132)
    plt.imshow(segmented_image, cmap='gray')  # Display in grayscale as river is white, not river black
    plt.title('Identified River (K-Means)')
    plt.axis('off')
    # Subplot 3: River Mask, Final result of the river identification
    plt.subplot(133)  # (1 row, 3 columns, position 3)
    plt.imshow(river_mask, cmap='gray')  # Binary mask (black & white)
    plt.title('Identified River')
    plt.axis('off')
    plt.show()

# Approach 2: Contours
def contouring(cv2_image):
    '''Using canny edge detection and contours to identify a river in a image read by OpenCV
    Input: cv2_image - Image read by OpenCV
    Output: Visualisation of the original image and the image with river contours
    Adjustments: Canny edge detection thresholds, contour settings (CHAIN_APPROX_SIMPLE)
    '''
    #Convert the image to grayscale
    gray = cv2.cvtColor(cv2_image, cv2.COLOR_BGR2GRAY)
    # Apply GaussianBlur to reduce noise and improve edge detection
    blurred = cv2.GaussianBlur(gray, (5, 5), 0) # Will need to experiment with how large the ksize should be before deciding an approach.
    # The 0 setting means standard deviation automatically calculated by ksize.
    # Apply Canny edge detection
    edges = cv2.Canny(blurred, 50, 150) # Can adjust the lower and upper thresholds during testing.
    # Find contours
    contours, hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # Retrieves only the external contours as we only
    # want the boundary of the river. Simple is just a setting to save memory

    #Draw the contours on the original image to visualize the river
    river_image = cv2_image.copy()
    cv2.drawContours(river_image, contours, -1, (0, 255, 0), 2)  # Green color for the river contour

    # Display the original image and the image with river contours
    plt.subplot(121), plt.imshow(cv2.cvtColor(cv2_image, cv2.COLOR_BGR2RGB)), plt.title('Original Image')
    plt.subplot(122), plt.imshow(cv2.cvtColor(river_image, cv2.COLOR_BGR2RGB)), plt.title('River Contours')
    plt.show()
garbled = cv2.imread(r"/Users/tom/Documents/Biodevices/Repository Git/Biodevices-Back-End/river identification/UoB_sentinel.png")
proper = cv2.imread(r"/Users/tom/Documents/Biodevices/Repository Git/Biodevices-Back-End/river identification/UoB_gmap.png")
test = cv2.imread(r"/Users/tom/Documents/Biodevices/Repository Git/Biodevices-Back-End/river identification/images/google_maps_2.png")
# kclustering(test)
contouring(test)