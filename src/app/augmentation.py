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