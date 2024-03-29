import cv2
import numpy as np
import os
import csv
from scipy.stats import kurtosis, skew, entropy

def compute_texture_features(img):
    # Compute mean, variance, kurtosis, std, entropy, and skewness
    mean_value = np.mean(img)
    variance_value = np.var(img)
    # Check if variance is non-zero before computing kurtosis and skewness
    if variance_value > 0:
        kurtosis_value = kurtosis(img.flatten())
        skewness_value = skew(img.flatten())
    else:
        # Set kurtosis and skewness to NaN (Not a Number) if variance is zero
        kurtosis_value = np.nan
        skewness_value = np.nan

    std_value = np.std(img)
    entropy_value = entropy(np.histogramdd(img.flatten(), bins=256)[0])
    
    return mean_value, variance_value, kurtosis_value, std_value, entropy_value, skewness_value

def apply_gabor_filter(image, ksize=31, sigma=5, theta=0, lam=10, gamma=0.5):
    # Convert the image to grayscale if it's in color
    if len(image.shape) == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply Gabor filter
    gabor_kernel = cv2.getGaborKernel((ksize, ksize), sigma, theta, lam, gamma, 0, ktype=cv2.CV_32F)
    filtered_image = cv2.filter2D(image, cv2.CV_8UC3, gabor_kernel)

    return filtered_image

# Directory containing images
images_dir = r"C:\Users\ASUS\OneDrive\Documents\Facial Images\blocks_diabetic"

# Output CSV file path
output_csv_file = r"C:\Users\ASUS\OneDrive\Documents\Facial Images\featureVectors.csv"

# List to store texture features for all images
texture_features_list = []

# Loop through each image in the directory
for i, filename in enumerate(os.listdir(images_dir)):
    if filename.endswith(('.jpg', '.png', '.jpeg')):  # Check if the file is an image
        # Load the image
        image_path = os.path.join(images_dir, filename)
        image = cv2.imread(image_path)

        # Apply Gabor filter
        filtered_image = apply_gabor_filter(image)

        # Compute texture features from the filtered image
        mean_val, var_val, kurt_val, std_val, entropy_val, skew_val = compute_texture_features(filtered_image)

        # Append texture features to the list
        texture_features_list.append([filename, mean_val, var_val, kurt_val, std_val, entropy_val, skew_val])

        # Write to CSV file every 4 images
        if (i + 1) % 4 == 0:
            with open(output_csv_file, 'a', newline='') as csv_file:
                writer = csv.writer(csv_file)
                # Write texture features for each image
                writer.writerows(texture_features_list)
            # Clear the list for the next batch of images
            texture_features_list = []

# If there are remaining images in the list, write them to the CSV file
if texture_features_list:
    with open(output_csv_file, 'a', newline='') as csv_file:
        writer = csv.writer(csv_file)
        # Write texture features for remaining images
        writer.writerows(texture_features_list)

print("Texture features saved to:", output_csv_file)