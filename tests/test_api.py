# test_api_simple.py
from flask import Flask, request, jsonify

# Minimal API definition for testing
app = Flask(__name__)

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    if not data or "features" not in data:
        return jsonify({"error": "Missing 'features'"}), 400

    # Pretend prediction logic
    prediction = 123.45
    return jsonify({"prediction": prediction}), 200

# ------------- Tests -----------------

def test_predict_valid():
    client = app.test_client()
    sample = {
        "features": [-122.23, 37.88, 41.0, 880, 129, 322, 126, 8.3252, "NEAR BAY"],
    }
    response = client.post("/predict", json=sample)
    assert response.status_code == 200
    data = response.get_json()
    assert "prediction" in data
    assert isinstance(data["prediction"], (int, float))

def test_predict_invalid():
    client = app.test_client()
    # Missing the required "features" field
    response = client.post("/predict", json={"foo": "bar"})
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data
