""" Micro-service which holds Pumpkin data """
import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

PUMPKINTYPES =  [
  "JAPANESE",
  "QUEENSLAND",
  "BUTTERNUT"
]

CAPACITY_SERVICE_URL = "http://capacity:5500/"

PUMPKINS = []

@app.route("/pumpkins", methods=['GET', 'POST'])
def pumpkins():
    """pumpkins endpoint for getting and posting Pumpkins to basket"""
    if request.method == 'POST':
        return update_pumpkins()
    else:
        return get_pumpkins()

def get_pumpkins():
    """Return all Pumpkins"""
    return jsonify(PUMPKINS)

def update_pumpkins():
    """Update/Add or Remove Pumpkins in basket"""
    response = 'No valid request', 400
    global PUMPKINS
    pumpkin_type = request.get_json()["type"]
    if validate_pumpkin_type(pumpkin_type):
        if check_sufficient_capacity(pumpkin_type):
            remove_pumpkin = bool(request.get_json()['removePumpkin'])
            if remove_pumpkin:
                PUMPKINS = [i for i in PUMPKINS if i['name'] == request.get_json()["name"]]
                request_object = { 'weight': get_pumpkin_weight(pumpkin_type), 'pumpkinRemoved': True }
                requests.post(CAPACITY_SERVICE_URL + 'capacity', json=request_object)
                response = 'Pumpkin have been removed succesfully', 200
            else:
                PUMPKINS.append(request.get_json())
                request_object = { 'weight': get_pumpkin_weight(pumpkin_type), 'pumpkinRemoved': False }
                requests.post(CAPACITY_SERVICE_URL + 'capacity', json=request_object)
                response = 'Pumpkin have been added succesfully', 200
        else:
            response = 'Not enough capacity available', 400
    return response

def validate_pumpkin_type(pumpkin_type):
    """Validate Pumpkintype before adding to basket"""
    return pumpkin_type in PUMPKINTYPES

def get_pumpkin_weight(pumpkin_type):
    """Get the weight of a given pumpkin"""
    if validate_pumpkin_type(pumpkin_type):
        pumpkin_weight_request = CAPACITY_SERVICE_URL + 'pumpkinweight?type='+ pumpkin_type
        pumpkin_weight = str(requests.get(pumpkin_weight_request).text)
        return pumpkin_weight
    return 'No valid pumpkinType', 400

def check_sufficient_capacity(pumpkin_type):
    """Get the remaining capacity of the basket"""
    available_capacity = str(requests.get(CAPACITY_SERVICE_URL + 'capacity').text)
    pumpkin_weight = get_pumpkin_weight(pumpkin_type)
    return (int(available_capacity) >= int(pumpkin_weight))
