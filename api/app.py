import mlflow
import mlflow.sklearn
from flask import Flask, request, jsonify
import numpy as np
import pandas as pd

import os

# Load the entire pipeline from the Model Registry from models folder
model_path = os.getenv("MODEL_PATH", "./models")
model_pipeline = mlflow.sklearn.load_model(model_path)

# Initialize Flask app
app = Flask(__name__)

# Define a route for predictions
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get the input data from the POST request
        data = request.get_json()  # Expecting JSON input with "features" field
        
        # Convert input features to a Pandas DataFrame (needed for preprocessing)
        input_features = pd.DataFrame([data['features']], columns=[
            'longitude', 'latitude', 'housing_median_age', 'total_rooms', 
            'total_bedrooms', 'population', 'households', 'median_income', 'ocean_proximity'
        ])

        # Make the prediction using the loaded pipeline (which includes preprocessing)
        prediction = model_pipeline.predict(input_features)
        
        # Return the prediction as a JSON response
        return jsonify({"prediction": prediction[0]})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Run the Flask app

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001, debug=False, use_reloader=False)
