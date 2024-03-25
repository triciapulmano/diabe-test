# reference: https://github.com/diezcami/CS129-18-face-detection/blob/master/gabor.py
import numpy as np
import cv2
import os
import csv

# diabetic data
# POSITIVE_TRAIN_DIR = 'data/train_images/positives'
# non-diabetic data
NEGATIVE_TRAIN_DIR = r'C:\Users\ASUS\OneDrive\Documents\Facial Images\Nondiabetics'

# EPS value for handling division by zero
EPS = 0.00000000000000001

# Load the pre-trained face and eye cascade classifiers
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')


# Function to load images from a folder
def load_images_from_folder(folder):
    images = []
    # Print the filenames before reading images
    print("Filenames in folder:", os.listdir(folder))
    for filename in os.listdir(folder):
        img = cv2.imread(os.path.join(folder, filename))
        if img is not None:
            images.append(img)
    return images

"""
def detect_eyes(gray_face):
    eyes = eye_cascade.detectMultiScale(gray_face, scaleFactor=1.3, minNeighbors=5)
    return eyes


# Function to segment facial blocks based on eye positions
def segment_blocks(image, eyes):
    # Sort eyes by x-coordinate to determine left and right eyes
    eyes = sorted(eyes, key=lambda x: x[0])

    # Print the detected eye positions for debugging
    print("Detected left eye:", eyes[0])
    print("Detected right eye:", eyes[1])

    # Extract eye positions
    left_eye = eyes[0]
    right_eye = eyes[1]

    # Define the regions for different facial blocks
    forehead = image[int(right_eye[1] * 0.6):int(right_eye[1] * 0.8), int(right_eye[0] * 0.8):int(left_eye[0] * 1.2)]
    nose_bridge = image[int(right_eye[1] * 0.4):int(left_eye[1] * 0.6), int(right_eye[0] * 0.8):int(left_eye[0] * 1.2)]
    cheek = image[int(left_eye[1] * 1.1):int(left_eye[1] * 1.5), int(left_eye[0] * 0.6):int(right_eye[0] * 1.4)]
    # Print the dimensions of the extracted blocks
    print("Forehead size:", forehead.shape)
    print("Nose bridge size:", nose_bridge.shape)
    print("Cheek size:", cheek.shape)

    return forehead, nose_bridge, cheek
"""

# Function to resize an image to a specific size
def resize_image(image, size):
    print("Image size before resizing:", image.shape)
    try:
        resized_image = cv2.resize(image, size)
        print("Image size after resizing:", resized_image.shape)
        return resized_image
    except Exception as e:
        print("Error during resizing:", e)
        return None


def build_filters():
    filters = []

    # Size of Gabor kernel
    ksize = 40

    # Eight orientations
    for theta in np.arange(0, 2*np.pi, np.pi/4):
        # 5 wavelengths
        for lamb in np.linspace(0, 2 * np.pi, 5, endpoint=False):
            # Get a filter
            kern = cv2.getGaborKernel((ksize, ksize), 4.0, theta, lamb, 0.5, 0, ktype=cv2.CV_32F)
            kern /= 1.5*kern.sum()
            filters.append(kern)

    return filters


# Function to apply Gabor filtering to an image
def apply_gabor_filter(image, ksize, theta, lamb):
    try:
        kern = cv2.getGaborKernel((ksize, ksize), 4.0, theta, lamb, 0.5, 0, ktype=cv2.CV_32F)
        kern /= 1.5 * kern.sum()
        return cv2.filter2D(image, cv2.CV_8UC3, kern)
    except Exception as e:
        print("Error during filtering:", e)
        return None


# Function to compute local energy of a matrix
def compute_local_energy(matrix):
    local_energy = np.sum(matrix.astype(np.float32) ** 2)
    return EPS if local_energy == 0 else local_energy / 650250000


# Function to compute mean amplitude of a matrix
def compute_mean_amplitude(matrix):
    mean_amp = np.sum(np.abs(matrix.astype(np.float32)))
    return EPS if mean_amp == 0 else mean_amp / 2550000


# Function to compute feature vectors for facial blocks
def compute_feature_vectors(blocks):
    filters = build_filters()  # Build Gabor filters
    print("Filters:", filters)
    feature_vectors = []
    for block in blocks:
        block = resize_image(block, (100, 100))  # Resize block
        responses = [apply_gabor_filter(block, ksize, theta, lamb) for ksize, theta, lamb in filters]  # Apply Gabor filters
        local_energies = [compute_local_energy(response) for response in responses]  # Compute local energies
        mean_amplitudes = [compute_mean_amplitude(response) for response in responses]  # Compute mean amplitudes
        feature_vectors.append(local_energies + mean_amplitudes)  # Combine local energies and mean amplitudes
    return feature_vectors

# Function to create CSV output containing feature vectors
#def create_csv_output(filename, posdir, negdir):


def create_csv_output(filename, negdir):
    #positive_images = load_images_from_folder(posdir)
    try:
        negative_images = load_images_from_folder(negdir)
        with open(filename, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
        """for image in positive_images:
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            eyes = detect_eyes(gray_image)
            blocks = segment_blocks(image, eyes)
            feature_vectors = compute_feature_vectors(blocks)
            writer.writerows(feature_vectors)
            """
        for image in negative_images:
            print("Image size before resizing:", image.shape)
            gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            eyes = detect_eyes(gray_image)
            # Add error handling for too few or too many detected eyes
            if len(eyes) != 2:
                print("Error: Expected to detect 2 eyes, but detected", len(eyes))
                continue
            try:
                blocks = segment_blocks(image, eyes)
                feature_vectors = compute_feature_vectors(blocks)
                writer.writerows(feature_vectors)
            except:
                print("Error: compute feature_vectors")

    except Exception as e:
        print("Error during image processing:", e)

if __name__ == '__main__':
    # create_csv_output("data/train.csv", POSITIVE_TRAIN_DIR, NEGATIVE_TRAIN_DIR)
    create_csv_output(r"C:\Users\ASUS\OneDrive\Documents\Facial Images\featureVectors.csv", NEGATIVE_TRAIN_DIR)