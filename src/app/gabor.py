# reference: https://github.com/diezcami/CS129-18-face-detection/blob/master/gabor.py
import numpy as np
import cv2
import os
import csv

EPS = 0.00000000000000001

def build_filters():
    filters = []
    ksize = 40
    # Eight orientations
    for theta in np.arange(0, 2*np.pi, np.pi/4):
        # 5 wavelengths
        for lamb in np.linspace(0, 2 * np.pi, 5, endpoint=False):
            kern = cv2.getGaborKernel((ksize, ksize), 4.0, theta, lamb, 0.5, 0, ktype=cv2.CV_32F)
            kern /= 1.5*kern.sum()
            filters.append(kern)
    return filters

def process(img, filters):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = cv2.resize(img, (100, 100))

    texture_values = []
    for kern in filters:
        fimg = cv2.filter2D(img, cv2.CV_8UC3, kern)
        texture_value = np.mean(fimg)  # Calculate texture value (mean of all pixels)
        texture_values.append(texture_value)

    return texture_values

def get_image_feature_vector(image, filters):
    response_texture_values = process(image, filters)
    final_texture_value = np.mean(response_texture_values)  # Average texture values from all responses
    return final_texture_value

if __name__ == '__main__':
    #usage for a single image
    image_path = ""
    image = cv2.imread(image_path)
    filters = build_filters()
    feature_vector = get_image_feature_vector(image, filters)