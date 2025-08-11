# California Housing Price Prediction

This project predicts California housing prices using a machine learning model, MLFLOW for selecting best model, serves predictions via a Flask API, and provides Docker support for deployment.

## Table of Contents

- [Requirements](#requirements)
- [ML Model Creation & Best Model Selection](#ml-model-creation)
- [Flask App for Model Serving](#flask-app-for-model-serving)
- [Docker Commands](#docker-commands)

---

## Requirements

Install conda:

```bash
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
```

```bash
bash Miniconda3-latest-Linux-x86_64.sh
```

```bash
conda --version
```

```bash
conda update conda
```

Install dependencies:

```bash
conda env create -f environment.yml
```

---


## ML Model Creation

Train the model using the provided script:

```bash
python main_california_housing.py
```

This will generate a best model into the directory ./models  in the project directory.

---


## Flask App for Model Serving

Start the Flask API to serve predictions:

```bash
python ./api/app.py
```

The API will be available at `http://localhost:5001/predict`. Send a POST request with input data in JSON format.

Example:

```bash
curl -X POST -H "Content-Type: application/json" -d '{"features": [2.5, 37.88, 30.0, 1200.0, 300.0, 500.0, 150.0, 9.0, "BAY AREA"]}' http://127.0.0.1:5001/predict
```

---

## Docker Commands

Build the Docker image:

```bash
sudo docker build -t california-housing-api .
```

Run the container:

```bash
sudo docker run -p 5001:5001 california-housing-api
```

---


## License

MIT License
