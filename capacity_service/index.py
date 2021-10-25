"""
Micro-service which displays available capacity """
import sys
from flask import Flask, request
app = Flask(__name__)

pumpkins = [
  { 'name': 'JAPANESE', 'weight': 3 },
  { 'name': 'QUEENSLAND', 'weight': 2 },
  { 'name': 'BUTTERNUT', 'weight': 1}
]

MAXCAPACITY = 11
AVAILABLECAPACITY = MAXCAPACITY

@app.route("/capacity")
def get_capacity():
    """Return the available capacity of the basket"""
    return str(AVAILABLECAPACITY)

@app.route("/capacity", methods=["POST"])
def update_capacity():
    """Update the capacity of the basket"""
    global AVAILABLECAPACITY
    request_json = request.get_json(force=True)
    pumpkin_weight = int(request_json['weight'])
    pumpkin_removed = bool(request_json['pumpkinRemoved'])
    if pumpkin_removed:
        if(AVAILABLECAPACITY + pumpkin_weight) <= MAXCAPACITY:
            AVAILABLECAPACITY = AVAILABLECAPACITY + pumpkin_weight
            return "Capacity updated. New capacity: " + str(AVAILABLECAPACITY), 200
        return "Capacity can't be higher than: " + str(MAXCAPACITY), 400
    else:
        if(AVAILABLECAPACITY - pumpkin_weight) >= 0:
            AVAILABLECAPACITY = AVAILABLECAPACITY - pumpkin_weight
            return "Capacity updated. New capacity: " + str(AVAILABLECAPACITY), 200
        return "Capacity can't be lower than: " + str(MAXCAPACITY), 400

@app.route("/pumpkinweight")
def get_pumpkin_weight():
    pumpkin_type = request.args.get("type")
    pumpkin_weight = next((item for item in pumpkins if item['name'] == pumpkin_type), False)
    return str(pumpkin_weight["weight"])
