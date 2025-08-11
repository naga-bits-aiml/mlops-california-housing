from src.data_download import download_data
from src.data_preprocessing import load_and_preprocess_data
from src.train import train_and_log_models
from src.model_register import register_best_model

import mlflow

import json
import os

def main():
    print("Step 1: Downloading data from Kaggle...")
    download_data()

    print("Step 2: Loading and preprocessing data...")
    X, y, preprocessor = load_and_preprocess_data('./data/housing.csv')

    print("Step 3: Training models and logging to MLflow...")
    best = train_and_log_models()

    print("Step 4: Registering best model in MLflow Model Registry...")
    name, version = register_best_model(best['model_uri'])

    # Save best model info for Flask app
    config = {
        "best_model": name,
        "version": version
    }
    os.makedirs("./models", exist_ok=True)
    with open("./models/models.config", "w") as f:
        json.dump(config, f)
    print("Best model info saved to models.config.")

    # Download best model to models directory
    model_path = mlflow.artifacts.download_artifacts(best['model_uri'], dst_path="./models")
    print(f"Best model downloaded to {model_path}")

    
if __name__ == "__main__":
    main()