import os
from kaggle.api.kaggle_api_extended import KaggleApi

def download_data():
    os.environ['KAGGLE_CONFIG_DIR'] = os.path.expanduser('~/.kaggle')
    api = KaggleApi()
    api.authenticate()
    api.dataset_download_files('camnugent/california-housing-prices', path='data', unzip=True)

if __name__ == "__main__":
    download_data()