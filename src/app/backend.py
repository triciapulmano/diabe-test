import cv2
from mtcnn import MTCNN
import numpy as np

# Load the MTCNN face detector
detector = MTCNN()

# Load the input image
image = cv2.imread(r"C:\Users\ASUS\OneDrive\Documents\Facial Images\Nondiabetics\20240118_142551 - Ray Angelo Pulmano.jpg")  # Replace "path/to/your/image.jpg" with the actual path to your image

# Convert the image to RGB format (MTCNN requires RGB images)
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Detect faces and facial landmarks using MTCNN
detections = detector.detect_faces(image_rgb)

if detections:
    # Assume only one face is detected for simplicity (you can modify for multiple faces)
    face = detections[0]['box']  # Get bounding box coordinates of the face
    keypoints = detections[0]['keypoints']  # Get facial keypoints

    # Extract forehead (with eyebrows) and nose (with left and right cheek) if the keypoints are available
    if 'left_eyebrow' in keypoints and 'right_eyebrow' in keypoints:
        forehead_x1, forehead_y1 = keypoints['left_eyebrow']
        forehead_x2, forehead_y2 = keypoints['right_eyebrow']
        forehead = image[forehead_y1:forehead_y2, forehead_x1:forehead_x2]
        forehead_resized = cv2.resize(forehead, (72, 24))
        cv2.imshow("Forehead", forehead_resized)
    else:
        print("Left or right eyebrow keypoint not found.")

    if 'nose' in keypoints and 'right_cheek' in keypoints:
        nose_x1, nose_y1 = keypoints['nose']
        nose_x2, nose_y2 = keypoints['right_cheek']
        nose = image[nose_y1:nose_y2, nose_x1:nose_x2]
        nose_resized = cv2.resize(nose, (72, 24))
        cv2.imshow("Nose", nose_resized)
    else:
        print("Nose or right cheek keypoint not found.")

    cv2.waitKey(0)
else:
    print("No face detected in the image.")

# Close all OpenCV windows
cv2.destroyAllWindows()

