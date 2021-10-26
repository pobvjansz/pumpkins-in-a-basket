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

BASKET = []

@app.route("/pumpkins", methods=['GET', 'POST'])
def pumpkins():
    """pumpkins endpoint for getting and posting Pumpkins to basket"""
    if request.method == 'POST':
        response = 'No capacity available', 400
        global BASKET
        if check_sufficient_capacity(request.get_json()['type']):
            remove_pumpkin = bool(request.get_json()['removePumpkin'])
            if remove_pumpkin:
                if len(BASKET) == 0:
                    return response
                for i in range(len(BASKET)):
                    if str(BASKET[i]["name"]) == str(request.get_json()['name']):
                        del BASKET[i]
                        request_object = { 'weight': get_pumpkin_weight(request.get_json()['type']), 'pumpkinRemoved': True }
                        requests.post(CAPACITY_SERVICE_URL + 'capacity', json=request_object)
                        response = 'Pumpkin have been removed succesfully', 200
                    else:
                        response = 'Pumpkin was not in the basket', 400
            else:
                if validate_pumpkin(request.get_json()):
                    pumpkin = {"name": request.get_json()['name'], "type": request.get_json()['type']}
                    BASKET.append(pumpkin)
                    request_object = { 'weight': get_pumpkin_weight(request.get_json()['type']), 'pumpkinRemoved': False }
                    requests.post(CAPACITY_SERVICE_URL + 'capacity', json=request_object)
                    response = 'Pumpkin have been added succesfully', 200
                else:
                    response = 'Unvalid pumpkin to add', 400
        return response
    else:
        return jsonify(BASKET)

def validate_pumpkin(pumpkin):
    """Validate a pumpkin before adding it to the basket"""
    pumpkin_type = str(pumpkin['type'])
    pumpkin_name= str(pumpkin['name'])
    return (validate_pumpkin_name(pumpkin_name) and validate_pumpkin_type(pumpkin_type))

def validate_pumpkin_name(pumpkin_name):
    """Validate a pumpkin's name is unique before adding it to the basket"""
    if not any(pumpkin['name'] == pumpkin_name for pumpkin in BASKET):
        return True
    return False

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
