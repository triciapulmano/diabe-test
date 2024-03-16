import cv2
import numpy as np
import matplotlib.pyplot as plt

def extract_facial_blocks(image_path, block_size=(100, 100)):
    # Load the image
    image = cv2.imread(image_path)

    # Convert the image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Face detection using Haarcascades (you may need to adjust the path)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(gray_image, scaleFactor=1.3, minNeighbors=5)

    facial_blocks = []

    for (x, y, w, h) in faces:
        # Extract left cheek block
        left_cheek_block = gray_image[y:y + h, x:x + w // 3]
        left_cheek_block = cv2.resize(left_cheek_block, block_size)

        # Extract nose bridge block
        nose_bridge_block = gray_image[y:y + h // 2, x + w // 4:x + 3 * w // 4]
        nose_bridge_block = cv2.resize(nose_bridge_block, block_size)

        # Extract forehead block
        forehead_block = gray_image[y:y + h // 4, x:x + w]
        forehead_block = cv2.resize(forehead_block, block_size)

        facial_blocks.append((left_cheek_block, nose_bridge_block, forehead_block))

    return facial_blocks

def apply_gabor_filter(image):
    # Apply Gabor filter to the image
    kernel = cv2.getGaborKernel((21, 21), 5.0, 1.0, 10.0, 0.5, 0, ktype=cv2.CV_32F)
    gabor_filtered = cv2.filter2D(image, cv2.CV_8UC3, kernel)

    return gabor_filtered

def display_results(facial_blocks):
    for i, (left_cheek_block, nose_bridge_block, forehead_block) in enumerate(facial_blocks):
        # Apply Gabor filter to each facial block
        left_cheek_texture = apply_gabor_filter(left_cheek_block)
        nose_bridge_texture = apply_gabor_filter(nose_bridge_block)
        forehead_texture = apply_gabor_filter(forehead_block)

        # Display original and Gabor-filtered images
        plt.subplot(3, 4, i * 4 + 1), plt.imshow(left_cheek_block, cmap='gray')
        plt.title('Left Cheek Block'), plt.xticks([]), plt.yticks([])

        plt.subplot(3, 4, i * 4 + 2), plt.imshow(left_cheek_texture, cmap='gray')
        plt.title('Left Cheek Texture'), plt.xticks([]), plt.yticks([])

        plt.subplot(3, 4, i * 4 + 3), plt.imshow(nose_bridge_block, cmap='gray')
        plt.title('Nose Bridge Block'), plt.xticks([]), plt.yticks([])

        plt.subplot(3, 4, i * 4 + 4), plt.imshow(nose_bridge_texture, cmap='gray')
        plt.title('Nose Bridge Texture'), plt.xticks([]), plt.yticks([])

        plt.subplot(3, 4, i * 4 + 5), plt.imshow(forehead_block, cmap='gray')
        plt.title('Forehead Block'), plt.xticks([]), plt.yticks([])

        plt.subplot(3, 4, i * 4 + 6), plt.imshow(forehead_texture, cmap='gray')
        plt.title('Forehead Texture'), plt.xticks([]), plt.yticks([])

    plt.show()

if __name__ == '__main__':
    # Specify the path to your image
    image_path = r'C:\Users\ASUS\OneDrive\Documents\_facialsample.png'

    # Extract facial blocks and apply Gabor filter
    facial_blocks = extract_facial_blocks(image_path, block_size=(100, 100))

    # Display the results
    display_results(facial_blocks)
