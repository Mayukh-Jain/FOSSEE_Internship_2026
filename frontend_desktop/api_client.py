import requests
import json

BASE_URL = 'https://jain-mayukh-fossee.hf.space/api'
TOKEN = None

def login(username, password):
    global TOKEN
    response = requests.post(f'{BASE_URL}/token/', data={'username': username, 'password': password})
    if response.status_code == 200:
        TOKEN = response.json()['access']
        return True
    return False

def get_headers():
    if TOKEN:
        return {'Authorization': f'Bearer {TOKEN}'}
    return {}

def get_datasets():
    response = requests.get(f'{BASE_URL}/datasets/', headers=get_headers())
    if response.status_code == 200:
        return response.json()
    return None

def get_dataset_data(dataset_id):
    response = requests.get(f'{BASE_URL}/datasets/data/?id={dataset_id}', headers=get_headers())
    if response.status_code == 200:
        return response.json()
    return None

def upload_dataset(filepath):
    with open(filepath, 'rb') as f:
        files = {'file': f}
        response = requests.post(f'{BASE_URL}/datasets/', files=files, headers=get_headers())
        return response.status_code == 201

def download_report(dataset_id, save_path):
    response = requests.get(f'{BASE_URL}/datasets/generate_report/?id={dataset_id}', headers=get_headers(), stream=True)
    if response.status_code == 200:
        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        return True
    return False
