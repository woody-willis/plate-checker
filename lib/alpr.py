import requests
import os
from dotenv import load_dotenv

load_dotenv()

def getPlateFromImage(path):
    regions = ['gb']

    with open(path, 'rb') as fp:
        response = requests.post(
            'https://api.platerecognizer.com/v1/plate-reader/',
            data=dict(regions=regions),
            files=dict(upload=fp),
            headers={'Authorization': 'Token ' + os.getenv('ALPRTOKEN')})
        return response