
import cv2
import numpy as np
from skimage.filters import gabor

# Function to resize image to 100x100 pixels and convert to grayscale
def preprocess_image(image_path):
    image = cv2.imread(image_path)
    resized_image = cv2.resize(image, (100, 100))
    grayscale_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)
    return grayscale_image

def extract_gabor_features(grayscale_image):

    # Define parameters for Gabor filters
    sigmas = [1, 2, 3, 4, 5]
    lambdas = [0, np.pi/4, np.pi/2, 3*np.pi/4, np.pi, 5*np.pi/4, 3*np.pi/2, 7*np.pi/4]
    orientations = [0, 1, 2, 3, 4, 5, 6, 7]  # Corresponding to 0°, 45°, 90°, 135°, 180°, 225°, 270°, 315°

    # Initialize list to store texture values
    texture_values = []

    # Iterate over combinations of parameters
    for sigma in sigmas:
        for theta in orientations:
            # Check if lambda[theta] is zero to avoid division by zero
            if lambdas[theta] != 0:
                # Create Gabor filter
                gabor_kernel = cv2.getGaborKernel((39, 39), sigma, theta*np.pi/8, 1/lambdas[theta], 0.5, 0, ktype=cv2.CV_32F)
                    
                # Convolve image with Gabor filter
                filtered_image = cv2.filter2D(grayscale_image, cv2.CV_64F, gabor_kernel)
                
                # Compute mean of filtered image as texture value
                texture_value = np.mean(filtered_image)
                texture_values.append(texture_value)

    # Calculate the average texture value
    average_texture_value = np.mean(texture_values)
    
    return average_texture_value


"""
# Load a single facial image and preprocess it
facial_image_path = r"path_to_your_image.jpg"
preprocessed_image = preprocess_image(facial_image_path)

# Extract Gabor features from the preprocessed image
gabor_features_single = extract_gabor_features_single(preprocessed_image, scales=5, orientations=8)

# Print the final Gabor feature vector for the image
print("Gabor Features for the Image:")
print(gabor_features_single)
"""