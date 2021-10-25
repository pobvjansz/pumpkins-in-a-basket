"""
Micro-service which displays available capacity """
from flask import Flask, jsonify, request 
import sys, requests
app = Flask(__name__)

pumpkins = [
  { 'name': 'JAPANESE', 'weight': 3 },
  { 'name': 'QUEENSLAND', 'weight': 2 },
  { 'name': 'BUTTERNUT', 'weight': 1}
]

MAXCAPACITY = 11
capacity = MAXCAPACITY

@app.route("/capacity")
def get_capacity():
  """List the available capacity"""
  # print("GetCapacity", file=sys.stderr)
  return str(capacity)

@app.route("/capacity", methods=["POST"])
def update_capacity():
  """Update the available capacity"""
  global capacity
  request_json = request.get_json(force=True) 
  pumpkinWeight = int(request_json['weight'])
  pumpkinRemoved = bool(request_json['pumpkinRemoved'])
  if((capacity - pumpkinWeight) >= 0):
    if(pumpkinRemoved):
      capacity = capacity - pumpkinWeight
    else:
      if(capacity + pumpkinWeight <= MAXCAPACITY):
        capacity = capacity + pumpkinWeight
      else:
        return "Capacity can't be higher than " + str(MAXCAPACITY), 400
    return "Capacity updated", 200
  else:
    return "Capacity can't be lower than 0", 400

@app.route("/pumpkinweight")
def get_pumpkinweight():
  """Get the weight of a pumpkintype"""
  pumpkinType = request.args.get("type")
  pumpkinWeight = next((item for item in pumpkins if item['name'] == pumpkinType), False)
  return str(pumpkinWeight["weight"])