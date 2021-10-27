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
            if validate_pumpkin(request.get_json()):
                add_pumpkin(request.get_json())
                response = jsonify(request.get_json()), 200
            else:
                response = jsonify(request.get_json()), 400
        return response
    else:
        return jsonify(BASKET)

@app.route("/pumpkins/<int:pumpkin_id>", methods=['GET'])
def get_pumpkin(pumpkin_id):
    """Get Specific Pumpkin by ID"""
    pumpkin = [pumpkin for pumpkin in BASKET if pumpkin['id'] == pumpkin_id]
    if len(pumpkin) == 0:
        return 'Not Found', 404
    return jsonify(pumpkin[0])

@app.route("/pumpkins/<int:pumpkin_id>", methods=['DELETE'])
def delete_pumpkin(pumpkin_id):
    """DELETE endpoint that deletes pumpking from a basket"""
    index = get_pumpkin_index_by_id(pumpkin_id)
    if index is False:
        return "Pumpkin not found in basket", 404
    pumpkin = get_pumpkin_in_basket_by_id(pumpkin_id)
    request_object = { 'weight': get_pumpkin_weight(pumpkin["type"]), 'pumpkinRemoved': True }
    requests.post(CAPACITY_SERVICE_URL + 'capacity', json=request_object)
    del BASKET[index]
    return jsonify(request.get_json(), 200)

@app.route("/pumpkins/<int:pumpkin_id>", methods=['PUT'])
def put_pumpkin(pumpkin_id):
    """PUT endpoint for updating the a pumpkin in a basket by id"""
    if len(BASKET) == 0:
        return 'Update of pumpkin failed', 400
    pumpkin = get_pumpkin_in_basket_by_id(pumpkin_id)
    request_object = { 'weight': get_pumpkin_weight(pumpkin['type']), 'pumpkinRemoved': True }
    requests.post(CAPACITY_SERVICE_URL + 'capacity', json=request_object)
    pumpkin['id'] = pumpkin_id
    pumpkin['type'] = request.get_json()['type']
    request_object = { 'weight': get_pumpkin_weight(pumpkin['type']), 'pumpkinRemoved': False }
    requests.post(CAPACITY_SERVICE_URL + 'capacity', json=request_object)
    return jsonify(request.get_json(), 200)

def add_pumpkin(pumpkin):
    """Adds pumpkin to a basket"""
    pumpkin = {"id": pumpkin['id'], "type": pumpkin['type']}
    request_object = { 'weight': get_pumpkin_weight(pumpkin['type']), 'pumpkinRemoved': False }
    requests.post(CAPACITY_SERVICE_URL + 'capacity', json=request_object)
    BASKET.append(pumpkin)
    return 'Pumpkin have been added succesfully', 200

def get_pumpkin_in_basket_by_id(pumpkin_id):
    """Get the a pumpkin in a basket by id"""
    index = get_pumpkin_index_by_id(pumpkin_id)
    if index is False:
        return "Pumpkin not found in basket", 404
    pumpkin = BASKET[index]
    return pumpkin

def update_pumpkin_in_basket_by_id(pumpkin, pumpkin_id):
    """Update the a pumpkin in a basket by id"""
    index = get_pumpkin_index_by_id(pumpkin_id)
    if index is False:
        return "Pumpkin not found in basket", 404
    BASKET[index] = pumpkin
    return "Pumpkin changed", 200

def get_pumpkin_index_by_id(pumpkin_id):
    """Get the index of a pumpkin in the basket"""
    for i in range(len(BASKET)):
        if str(BASKET[i]["id"]) == str(pumpkin_id):
            return i
    return False

def validate_pumpkin(pumpkin):
    """Validate a pumpkin before adding it to the basket"""
    pumpkin_type = str(pumpkin['type'])
    pumpkin_id = str(pumpkin['id'])
    return (validate_pumpkin_id(pumpkin_id) and validate_pumpkin_type(pumpkin_type))

def validate_pumpkin_id(pumpkin_id):
    """Validate a pumpkin's ID is unique before adding it to the basket"""
    if not any(pumpkin['id'] == pumpkin_id for pumpkin in BASKET):
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
