import mlflow
import mlflow.sklearn
from mlflow.models.signature import infer_signature
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from src.data_preprocessing import load_and_preprocess_data

def evaluate_regression(y_true, y_pred):
    from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
    mse  = mean_squared_error(y_true, y_pred)
    rmse = np.sqrt(mse)
    mae  = mean_absolute_error(y_true, y_pred)
    r2   = r2_score(y_true, y_pred)
    return {"mse": mse, "rmse": rmse, "mae": mae, "r2": r2}

def train_and_log_models():
    X, y, preprocessor = load_and_preprocess_data('./data/housing.csv')
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    candidates = [
        ("LinearRegression", LinearRegression()),
        ("DecisionTreeRegressor", DecisionTreeRegressor(random_state=42)),
    ]
    best = {"name": None, "metrics": None, "model_uri": None}
    mlflow.set_experiment("regression_model_selection")
    PRIMARY_METRIC = "rmse"

    with mlflow.start_run(run_name="model_comparison_parent") as parent_run:
        for name, model in candidates:
            model_pipeline = Pipeline([
                ('preprocessor', preprocessor),
                ('regressor', model)
            ])
            model_pipeline.fit(X_train, y_train)
            y_pred = model_pipeline.predict(X_test)
            metrics = evaluate_regression(y_test, y_pred)
            signature = infer_signature(X_test, y_pred)
            logged_model = mlflow.sklearn.log_model(
                sk_model=model_pipeline,
                artifact_path=f"{name}_model",
                signature=signature,
                input_example=X_test[:2]
            )
            mlflow.log_metrics(metrics)
            if best["metrics"] is None or metrics[PRIMARY_METRIC] < best["metrics"][PRIMARY_METRIC]:
                best = {"name": name, "metrics": metrics, "model_uri": logged_model.model_uri}
        print(f"Best model: {best['name']} | URI: {best['model_uri']}")
    return best

if __name__ == "__main__":
    train_and_log_models()