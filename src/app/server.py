import os
from flask import Flask, request, jsonify
import numpy as np
import pickle

app = Flask(__name__)

with open(r'src\app\model.pkl', 'rb') as file:
    model = pickle.load(file)

@app.route('/process_features', methods=['POST'])
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

if __name__ == '__main__':
    app.run(debug=True)
