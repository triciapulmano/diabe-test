import os
import cv2
import numpy as np
import csv
from skimage.filters import gabor

# Function to load facial images from a directory
def load_images_from_folder(folder_path):
    images = []
    for filename in os.listdir(folder_path):
        img_path = os.path.join(folder_path, filename)
        if os.path.isfile(img_path):
            read_img = cv2.imread(img_path)
            resized_image = cv2.resize(read_img, (100, 100))
            img = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)
            if img is not None:
                images.append(img)
    return images

"""
# Function to extract Gabor features from images
def extract_gabor_features(images, scales=5, orientations=8):
    feature_vectors = []
    for img in images:
        gabor_features = []
        for scale in range(scales):
            scale_responses = []
            for orientation in range(orientations):
                gabor_filter_bank = gabor(img, frequency=0.6, theta=(orientation / orientations) * np.pi,
                                          bandwidth=1, sigma_x=1, sigma_y=1, n_stds=3, offset=0)
                gabor_response = np.abs(gabor_filter_bank)
                scale_responses.append(np.mean(gabor_response))
            gabor_features.append(np.mean(scale_responses))
        feature_vectors.append(np.mean(gabor_features))
    return np.array(feature_vectors)
"""
    
# Function to extract Gabor features from an image
def extract_gabor_features(images):
    feature_vectors = []
    for img in images:
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
                    filtered_image = cv2.filter2D(img, cv2.CV_64F, gabor_kernel)
                    
                    # Compute mean of filtered image as texture value
                    texture_value = np.mean(filtered_image)
                    texture_values.append(texture_value)

        # Calculate the average texture value
        average_texture_value = np.mean(texture_values)
        feature_vectors.append(average_texture_value)
    
    return np.array(feature_vectors)


def write_gabor_features_to_csv(filename, feature_vectors):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        for idx in range(0, len(feature_vectors), 4):
            writer.writerow(feature_vectors[idx:idx + 4])

# Directory containing facial images
facial_images_dir = r"C:\Users\ASUS\OneDrive\Documents\Facial Images\blocks_nondiabetic" 

# Load facial images from the directory
facial_images = load_images_from_folder(facial_images_dir)

# Extract Gabor features from facial images with 5 scales and 8 orientations
gabor_features = extract_gabor_features(facial_images)

# Write Gabor features to CSV file
output_csv_file = r"C:\Users\ASUS\OneDrive\Documents\Facial Images\featureVectors.csv"
write_gabor_features_to_csv(output_csv_file, gabor_features)
