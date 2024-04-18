import os
from flask import Flask, request, jsonify
import numpy as np
import pickle

app = Flask(__name__)
# Get the directory of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Specify the filename you want to open (replace 'filename.txt' with your actual filename)
filename = 'svm_model.pkl'

# Construct the full path to the file
file_path = os.path.join(current_dir, filename)

# Open the file using a with statement
with open(file_path, 'rb') as file:
    # Perform operations with the file
    model = pickle.load(file)

@app.route('/process_features', methods=['GET'])
def process_features():
    # Get the features from the request
    features = request.json['features']

    # Convert features to numpy array
    features_array = np.array(features).reshape(1, -1)

    # Predict using the SVM model
    prediction = model.predict(features_array)

    # Return the prediction
    response = {'prediction': prediction.tolist()}
    return jsonify(response)


@app.route('/hello', methods=['GET'])
def hello():
    return jsonify("Hello World!")

    
if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host='0.0.0.0', port=8080, debug=True)
