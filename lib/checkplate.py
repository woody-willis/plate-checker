from imgur_python import Imgur
import requests
from requests.structures import CaseInsensitiveDict
from datetime import datetime
from plyer import notification
import json
import os

imgur_client = Imgur({'client_id': os.getenv('IMGURCLIENTID')})

def getDataFromNumberPlate(plate: str):
    plate = plate.upper()
    resp = None
    url = "https://driver-vehicle-licensing.api.gov.uk/vehicle-enquiry/v1/vehicles"
    headers = CaseInsensitiveDict()
    headers["x-api-key"] = "4KJdRlhl5p8NOGFZo4KQ937qaVqN0yNHaiGZSH91"
    headers["Content-Type"] = "application/json"
    data = '{"registrationNumber": "' + plate + '"}'
    req = requests.post(url, headers=headers, data=data)
    resp = json.loads(req.text)
    resp['registrationNumber'] = plate
    if req.status_code == 200:
        resp['status'] = req.status_code
        return resp
    else:
        resp['status'] = req.status_code
        return resp

def verifyNumberPlate(dvlaResp):
    resp = {}
    resp["status"] = []
    resp['registrationNumber'] = dvlaResp['registrationNumber']
    if dvlaResp['status'] == 200:
        if 'taxDueDate' in dvlaResp:
            taxDueDate = datetime.strptime(dvlaResp['taxDueDate'], '%Y-%m-%d')
            today = datetime.now()
            if taxDueDate.date() < today.date():
                resp["status"].append('Tax Overdue')
        if 'motStatus' in dvlaResp:
            motStatus = dvlaResp['motStatus']
            if motStatus == "Not valid":
                resp["status"].append('MOT Invalid')
        if 'motExpiryDate' in dvlaResp:
            motExpiryDate = datetime.strptime(dvlaResp['motExpiryDate'], '%Y-%m-%d')
            today = datetime.now()
            if motExpiryDate.date() < today.date():
                resp["status"].append('MOT Expired')
        return resp
    elif dvlaResp['status'] == 404:
        # Alert! Vehicle not found!
        resp["status"].append("Car Not Found")
        return resp
    else:
        # Something went wrong fetching data
        resp["status"].append("API Error")
        return resp

def notifyComputer(status):
    if status['status'] == []:
        return True

    alertsTriggered = ""

    for i in range(len(status['status'])):
        alertsTriggered = alertsTriggered + status['status'][i] + ', '

    alertsTriggered = alertsTriggered[:-2]

    notification.notify(
            title = "Dodgy car detected!",
            message = "Number Plate: {noplate}\nAlerts Triggered: {alerts}".format(
                        noplate = status['registrationNumber'],
                        alerts = alertsTriggered),  
            app_icon = "Paomedia-Small-N-Flat-Bell.ico",
            timeout = 5
        )