# import the necessary packages
from collections import OrderedDict
import os
import numpy as np
import cv2
import dlib
import imutils

input_dir = r'C:\Users\ASUS\OneDrive\Documents\Facial Images\Nondiabetics'
output_dir = r"C:\Users\ASUS\OneDrive\Documents\Facial Images\blocks_nondiabetic"
os.makedirs(output_dir, exist_ok=True)

facial_features_cordinates = {}

# define a dictionary that maps the indexes of the facial
# landmarks to specific face regions
FACIAL_LANDMARKS_INDEXES = OrderedDict([
    ("Mouth", (48, 68)),
    ("Right_Eyebrow", (17, 22)),
    ("Left_Eyebrow", (22, 27)),
    ("Right_Eye", (36, 42)),
    ("Left_Eye", (42, 48)),
    ("Nose", (27, 35)),
    ("Jaw", (0, 17))
])



def shape_to_numpy_array(shape, dtype="int"):
    # initialize the list of (x, y)-coordinates
    coordinates = np.zeros((68, 2), dtype=dtype)

    # loop over the 68 facial landmarks and convert them
    # to a 2-tuple of (x, y)-coordinates
    for i in range(0, 68):
        coordinates[i] = (shape.part(i).x, shape.part(i).y)

    # return the list of (x, y)-coordinates
    return coordinates

def visualize_facial_landmarks(image, shape, colors=None, alpha=0.75):
    # create two copies of the input image -- one for the
    # overlay and one for the final output image
    overlay = image.copy()
    output = image.copy()

    # if the colors list is None, initialize it with a unique
    # color for each facial landmark region
    if colors is None:
        colors = [(19, 199, 109), (79, 76, 240), (230, 159, 23),
                  (168, 100, 168), (158, 163, 32),
                  (163, 38, 32), (180, 42, 220)]

    # loop over the facial landmark regions individually
    for (i, name) in enumerate(FACIAL_LANDMARKS_INDEXES.keys()):
        # grab the (x, y)-coordinates associated with the
        # face landmark
        (j, k) = FACIAL_LANDMARKS_INDEXES[name]
        pts = shape[j:k]
        facial_features_cordinates[name] = pts

        # check if are supposed to draw the jawline
        if name == "Jaw":
            # since the jawline is a non-enclosed facial region,
            # just draw lines between the (x, y)-coordinates
            for l in range(1, len(pts)):
                ptA = tuple(pts[l - 1])
                ptB = tuple(pts[l])
                cv2.line(overlay, ptA, ptB, colors[i], 2)

        # otherwise, compute the convex hull of the facial
        # landmark coordinates points and display it
        else:
            hull = cv2.convexHull(pts)
            cv2.drawContours(overlay, [hull], -1, colors[i], -1)

    # apply the transparent overlay
    cv2.addWeighted(overlay, alpha, output, 1 - alpha, 0, output)

    # return the output image
    print(facial_features_cordinates)
    return output


# initialize dlib's face detector (HOG-based) and then create the facial landmark predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(r"C:\Users\ASUS\OneDrive\Documents\diabetes app\src\app\shape_predictor_68_face_landmarks (1).dat")

def block_extraction(point, img):
    # nose block center = point[29]
    height = int(point[31][1] - point[28][1])
    width = height

    nose = img[int(point[29][1]-(height/2)):int(point[29][1]+(height/2)), int(point[29][0]-(width/2)):int(point[29][0]+(width/2))]
    cv2.imwrite(os.path.join(output_dir, f"{filename}_nose.jpg"), nose)

    # right cheek
    # point[47] x-coordinate of center 
    r_centery = int(point[46][1]) + int(height / 2)
    r_centerx = int(point[46][0])

    # Calculate the integer values for slicing indices
    r_left = r_centerx - int(width / 2)
    r_right = r_centerx + int(width / 2)
    r_top = r_centery - int(height / 2)
    r_bottom = r_centery + int(height / 2)

    right = img[r_top:r_bottom, r_left:r_right]
    cv2.imwrite(os.path.join(output_dir, f"{filename}_right.jpg"), right)

    # left cheek, point[41] x-coordinate of center
    l_centery = int(point[41][1]) + int(height / 2)
    l_centerx = int(point[41][0])

    # Calculate the integer values for slicing indices
    l_left = l_centerx - int(width / 2)
    l_right = l_centerx + int(width / 2)
    l_top = l_centery - int(height / 2)
    l_bottom = l_centery + int(height / 2)

    left = img[l_top:l_bottom, l_left:l_right]
    cv2.imwrite(os.path.join(output_dir, f"{filename}_left.jpg"), left)

    # forehead
    min_y = min(point[19][1], point[24][1])
    f_centerx = point[29][0]
    f_centery = min_y - int(height / 2)

    # Calculate the integer values for slicing indices
    f_left = f_centerx - int(width / 2)
    f_right = f_centerx + int(width / 2)
    f_top = f_centery - int(height / 2)
    f_bottom = f_centery + int(height / 2)

    forehead = img[f_top:f_bottom, f_left:f_right]
    # Check if forehead is not empty before writing
    if forehead is not None and forehead.size != 0:
        cv2.imwrite(os.path.join(output_dir, f"{filename}_forehead.jpg"), forehead)
    else:
        print("Empty forehead image. Skipping writing.")

# Iterate through all image files in the input directory
for filename in os.listdir(input_dir):
    # Check if the file is an image (you can adjust the extensions as needed)
    if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp')):
        image_path = os.path.join(input_dir, filename)

        # Load the input image, resize it, and convert it to grayscale
        img = cv2.imread(image_path)
        img = imutils.resize(img, width=500)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Detect faces in the grayscale image
        rects = detector(gray, 1)

        # Initialize an empty NumPy array to store the facial landmarks
        point = np.zeros((68, 2), dtype=int)

        # Loop over the face detections
        for (i, rect) in enumerate(rects):
            # Determine the facial landmarks for the face region
            shape = predictor(gray, rect)

            # Loop over the 68 facial landmarks and store each (x, y) coordinate
            for j in range(0, 68):
                x = shape.part(j).x
                y = shape.part(j).y
                point[j] = (x, y)

            # Perform block extraction using the block_extraction function
            block_extraction(point, img)

