import mlflow

def register_best_model(model_uri, model_name="housing_prediction_best_model"):
    with mlflow.start_run():
        registered_model = mlflow.register_model(model_uri, model_name)
        print(f"Best model registered: {registered_model.name}, Version: {registered_model.version}")
        result = (registered_model.name, registered_model.version)
    return result

if __name__ == "__main__":
    # You would load the best model URI from a config or output file
    model_uri = "runs:/<run_id>/<artifact_path>"
    name, version = register_best_model(model_uri)
    print(f"Returned: {name}, version {version}")