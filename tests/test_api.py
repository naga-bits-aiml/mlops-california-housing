import importlib
import importlib.util
import os
import sys
import types

import pytest


class DummyModel:
    def predict(self, X):
        return [123.45]


def create_app():
    """Import the Flask app with stubbed dependencies."""
    # Stub mlflow with a sklearn submodule providing load_model
    mlflow_stub = types.ModuleType("mlflow")
    sklearn_stub = types.ModuleType("mlflow.sklearn")
    sklearn_stub.load_model = lambda path: DummyModel()
    mlflow_stub.sklearn = sklearn_stub

    # Stub pandas with minimal DataFrame implementation
    pandas_stub = types.ModuleType("pandas")

    class DummyDataFrame:
        def __init__(self, data, columns):
            self.data = data
            self.columns = columns

    pandas_stub.DataFrame = DummyDataFrame

    # Stub numpy as it's imported but unused
    numpy_stub = types.ModuleType("numpy")

    sys.modules["mlflow"] = mlflow_stub
    sys.modules["mlflow.sklearn"] = sklearn_stub
    sys.modules["pandas"] = pandas_stub
    sys.modules["numpy"] = numpy_stub

    # Load the app module from the api/app.py file
    module_path = os.path.join(os.path.dirname(__file__), "..", "api", "app.py")
    spec = importlib.util.spec_from_file_location("api.app", module_path)
    app_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(app_module)
    return app_module


def test_predict_valid():
    app_module = create_app()
    client = app_module.app.test_client()
    sample = {
        "features": [-122.23, 37.88, 41.0, 880, 129, 322, 126, 8.3252, "NEAR BAY"],
    }
    response = client.post("/predict", json=sample)
    assert response.status_code == 200
    data = response.get_json()
    assert "prediction" in data
    assert isinstance(data["prediction"], (int, float))


def test_predict_invalid():
    app_module = create_app()
    client = app_module.app.test_client()
    # Missing the required "features" field
    response = client.post("/predict", json={"foo": "bar"})
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data
