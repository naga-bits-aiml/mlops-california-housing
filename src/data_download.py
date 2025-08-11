import os
import json
from kaggle.api.kaggle_api_extended import KaggleApi

def ensure_kaggle_credentials():
    kaggle_config_dir = os.environ.get('KAGGLE_CONFIG_DIR', os.path.expanduser('~/.kaggle'))
    kaggle_json_path = os.path.join(kaggle_config_dir, 'kaggle.json')

    # If kaggle.json exists, use it
    if os.path.exists(kaggle_json_path):
        return

    # Otherwise, try to get from environment variables
    username = os.environ.get('KAGGLE_USERNAME')
    key = os.environ.get('KAGGLE_KEY')

    if username and key:
        os.makedirs(kaggle_config_dir, exist_ok=True)
        with open(kaggle_json_path, 'w') as f:
            json.dump({'username': username, 'key': key}, f)
        os.chmod(kaggle_json_path, 0o600)
    else:
        raise RuntimeError("Kaggle credentials not found. Set KAGGLE_USERNAME and KAGGLE_KEY env vars or provide ~/.kaggle/kaggle.json.")

def download_data():
    ensure_kaggle_credentials()
    kaggle_config_dir = os.environ.get('KAGGLE_CONFIG_DIR', os.path.expanduser('~/.kaggle'))
    os.environ['KAGGLE_CONFIG_DIR'] = kaggle_config_dir
    api = KaggleApi()
    api.authenticate()
    api.dataset_download_files('camnugent/california-housing-prices', path='data', unzip=True)

if __name__ == "__main__":
    download_data()