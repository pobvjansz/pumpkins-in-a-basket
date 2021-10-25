"""
Micro-service which holds testpumpkin data """
from flask import Flask, jsonify, request
from flask.wrappers import Response
import sys, requests
app = Flask(__name__)

PUMPKINTYPES =  [
  "JAPANESE",
  "QUEENSLAND",
  "BUTTERNUT"
]

CAPACITY_SERVICE_URL = "http://capacity:5500/"

testPumpkins = []

@app.route("/testpumpkins", methods=['GET', 'POST'])
def testpumpkins():
  if(request.method == 'POST'):
      return update_testpumpkins()
  else:
    return get_testpumpkins()

def get_testpumpkins():
  return jsonify(testPumpkins)

def update_testpumpkins():
  response = 'No valid request', 400
  global testPumpkins
  pumpkinType = request.get_json()["type"]
  if(validatePumpkinType(pumpkinType)):
      if(sufficientCapacity(pumpkinType)):
        removePumpkin = bool(request.get_json()['removePumpkin'])
        if(removePumpkin):
          testPumpkins = [i for i in testPumpkins if (i['name'] == request.get_json()["name"])]
          requestObj = { 'weight': getPumpkinWeight(pumpkinType), 'pumpkinRemoved': True }
          requests.post(CAPACITY_SERVICE_URL + 'capacity', json=requestObj)
          response = 'Testpumpkin have been removed succesfully', 200
        else:
          testPumpkins.append(request.get_json())
          requestObj = { 'weight': getPumpkinWeight(pumpkinType), 'pumpkinRemoved': False }
          requests.post(CAPACITY_SERVICE_URL + 'capacity', json=requestObj)
          response = 'Testpumpkin have been added succesfully', 200
      else :
        response = 'Not enough capacity available', 400
  return response

def validatePumpkinType(pumpkinType):
  return (pumpkinType in PUMPKINTYPES)
  
def getPumpkinWeight(pumpkinType):
  if(validatePumpkinType):
    pumpkinWeightRequest = CAPACITY_SERVICE_URL + 'pumpkinweight?type='+ pumpkinType    
    pumpkinWeight = str(requests.get(pumpkinWeightRequest).text)
    return pumpkinWeight
  else:
    return 'No valid pumpkinType', 400

def sufficientCapacity(pumpkinType):
  availableCapacity = str(requests.get(CAPACITY_SERVICE_URL + 'capacity').text)
  pumpkinWeight = getPumpkinWeight(pumpkinType)
  return (int(availableCapacity) >= int(pumpkinWeight))