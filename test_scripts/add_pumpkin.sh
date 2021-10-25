#!/bin/bash
NAME="Test Pumpkin"

curl -X POST -H "Content-Type: application/json" -d "{
    \"name\": \"pumpkin_${NAME}\",
    \"type\": \"JAPANESE\",
    \"removePumpkin\": false
}" http://localhost:5000/pumpkins