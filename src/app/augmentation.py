import imageio
import imgaug as ia
import imgaug.augmenters as iaa
import os
import cv2
import numpy as np

input_dir = r'C:\Users\ASUS\OneDrive\Documents\Facial Images\Nondiabetics'
output_dir = r'C:\Users\ASUS\OneDrive\Documents\Facial Images\Nondiabetic augmented'

# Function to perform augmentation on an image
def augment_image(image):
    # Horizontal flip
    hflip= iaa.Fliplr(p=1.0)
    flipped_image = hflip.augment_image(image)

    # Add Gaussian noise
    noise = iaa.AdditiveGaussianNoise(5,10)
    noisy_image = noise.augment_image(image)

    # Adjust contrast
    contrasted_image = cv2.convertScaleAbs(image, alpha=1.5, beta=0)
    #contrast=iaa.GammaContrast((0.5, 2.0))
    #contrast_sig = iaa.SigmoidContrast(gain=(5, 10), cutoff=(0.4, 0.6))
    #contrast_lin = iaa.LinearContrast((0.6, 0.4))
    #input_contrast = contrast.augment_image(input_img)
    #sigmoid_contrast = contrast_sig.augment_image(input_img)
    #linear_contrast = contrast_lin.augment_image(input_img)

    return flipped_image, noisy_image, contrasted_image

# Iterate through each image in the input directory
for filename in os.listdir(input_dir):
    if filename.endswith('.jpg') or filename.endswith('.png'): 
        # Read the image
        image_path = os.path.join(input_dir, filename)
        image = cv2.imread(image_path)

        # Perform augmentation
        flipped_image, noisy_image, contrasted_image = augment_image(image)

        # Save augmented images to the output directory
        flipped_output_path = os.path.join(output_dir, f'flipped_{filename}')
        noisy_output_path = os.path.join(output_dir, f'noisy_{filename}')
        contrasted_output_path = os.path.join(output_dir, f'contrasted_{filename}')

        cv2.imwrite(flipped_output_path, flipped_image)
        cv2.imwrite(noisy_output_path, noisy_image)
        cv2.imwrite(contrasted_output_path, contrasted_image)

        print(f'Augmented images saved: {flipped_output_path}, {noisy_output_path}, {contrasted_output_path}')

        """
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
            img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
            if img is not None:
                images.append(img)
    return images

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
        feature_vectors.append(gabor_features)
    return np.array(feature_vectors)

# Function to write Gabor features to CSV
def write_gabor_features_to_csv(filename, feature_vectors):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        for idx, features in enumerate(feature_vectors, 1):
            writer.writerow(features)
            # Add an empty row every 4 images
            if idx % 4 == 0:
                writer.writerow([])  

# Directory containing facial images
facial_images_dir = r"C:\Users\ASUS\OneDrive\Documents\Facial Images\blocks_nondiabetic" 

# Load facial images from the directory
facial_images = load_images_from_folder(facial_images_dir)

# Extract Gabor features from facial images with 5 scales and 8 orientations
gabor_features = extract_gabor_features(facial_images, scales=5, orientations=8)

# Write Gabor features to CSV file
output_csv_file = r"C:\Users\ASUS\OneDrive\Documents\Facial Images\featureVectors.csv"
write_gabor_features_to_csv(output_csv_file, gabor_features)

        """