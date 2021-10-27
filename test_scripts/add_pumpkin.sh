#!/bin/bash
ID=$$

curl -X POST -H "Content-Type: application/json" -d "{
    \"id\": 91390,
    \"type\": \"JAPANESE\",
    \"removePumpkin\": false
}" http://localhost:5000/pumpkins
