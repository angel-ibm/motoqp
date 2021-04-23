#!/bin/bash

# Make sure that everything is clean
curl -sS -X DELETE "http://localhost:5000/api/init" -H  "accept: */*" 
# Initialize the game
curl -sS -X POST "http://localhost:5000/api/init" -H  "accept: application/json" -d "" | jq .chname

# Retrieve all circuits
curl -sS -X GET "http://localhost:5000/api/circuit" -H  "accept: application/json" | jq .[]
# Get the riders and their bikes
curl -sS -X GET "http://localhost:5000/api/rider" -H  "accept: application/json" | jq .[]
curl -sS -X GET "http://localhost:5000/api/bike" -H  "accept: application/json" | jq .[]

# Begin the game

echo ------ RACE 1  -------
# What can I choose?
choice=$(curl -sS -X GET "http://localhost:5000/api/choice" -H  "accept: application/json")
free_circuit=$(curl -sS -X GET "http://localhost:5000/api/circuit?onlyfree=true" -H  "accept: application/json" | jq .[0].circuit_id)
free_bike=$(curl -sS -X GET "http://localhost:5000/api/bike?onlyfree=true" -H  "accept: application/json" | jq .[0].bike_id)

# Run the 1st race with my choice and tell me the result
curl -sS -X POST "http://localhost:5000/api/choice" -H  "accept: */*" -H  "Content-Type: application/json" \
              -d "{\"bike_id\":$free_bike,\"circuit_id\":$free_circuit,\"race_type\":\"normal\"}"

echo ------ RACE 2  -------
# What can I choose?
curl -sS -X GET "http://localhost:5000/api/choice" -H  "accept: application/json"
free_circuit=$(curl -sS -X GET "http://localhost:5000/api/circuit?onlyfree=true" -H  "accept: application/json" | jq .[0].circuit_id)
free_bike=$(curl -sS -X GET "http://localhost:5000/api/bike?onlyfree=true" -H  "accept: application/json" | jq .[0].bike_id)

# Run the 2nd. race with my choice and tell me the result
curl -sS -X POST "http://localhost:5000/api/choice" -H  "accept: */*" -H  "Content-Type: application/json" \
              -d "{\"bike_id\":$free_bike,\"circuit_id\":$free_circuit,\"race_type\":\"normal\"}"

echo ------ RACE 3  -------
# What can I choose?
curl -sS -X GET "http://localhost:5000/api/choice" -H  "accept: application/json"
free_circuit=$(curl -sS -X GET "http://localhost:5000/api/circuit?onlyfree=true" -H  "accept: application/json" | jq .[0].circuit_id)
free_bike=$(curl -sS -X GET "http://localhost:5000/api/bike?onlyfree=true" -H  "accept: application/json" | jq .[0].bike_id)

# Run the 3rd. race with my choice and tell me the result
curl -sS -X POST "http://localhost:5000/api/choice" -H  "accept: */*" -H  "Content-Type: application/json" \
              -d "{\"bike_id\":$free_bike,\"circuit_id\":$free_circuit,\"race_type\":\"normal\"}"


echo ------ RACE 4  -------
# What can I choose?
curl -sS -X GET "http://localhost:5000/api/choice" -H  "accept: application/json"
free_circuit=$(curl -sS -X GET "http://localhost:5000/api/circuit?onlyfree=true" -H  "accept: application/json" | jq .[0].circuit_id)
free_bike=$(curl -sS -X GET "http://localhost:5000/api/bike?onlyfree=true" -H  "accept: application/json" | jq .[0].bike_id)


# Run the 4th. race with my choice and tell me the result
curl -sS -X POST "http://localhost:5000/api/choice" -H  "accept: */*" -H  "Content-Type: application/json" \
              -d "{\"bike_id\":$free_bike,\"circuit_id\":$free_circuit,\"race_type\":\"normal\"}"


echo ------ RACE 5  -------
# What can I choose?
curl -sS -X GET "http://localhost:5000/api/choice" -H  "accept: application/json"
# Run the 5th. race with my choice and tell me the result
free_circuit=$(curl -sS -X GET "http://localhost:5000/api/circuit?onlyfree=true" -H  "accept: application/json" | jq .[0].circuit_id)
free_bike=$(curl -sS -X GET "http://localhost:5000/api/bike?onlyfree=true" -H  "accept: application/json" | jq .[0].bike_id)


curl -sS -X POST "http://localhost:5000/api/choice" -H  "accept: */*" -H  "Content-Type: application/json" \
              -d "{\"bike_id\":$free_bike,\"circuit_id\":$free_circuit,\"race_type\":\"normal\"}"
