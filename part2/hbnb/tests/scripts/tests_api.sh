#!/bin/bash

API_URL="http://127.0.0.1:5000/api/v1"

echo "Create user via API"

RESPONSE1=$(curl -s -X POST "$API_URL/users/" \
    -H "Content-Type: application/json" \
    -d "{\"first_name\": \"John\", \"last_name\": \"Doe\", \"email\": \"john@example.com\"}")
echo "response: $RESPONSE1"
USER_ID1=$(echo "$RESPONSE1" | grep -o '"id"[ ]*:[ ]*"[^\"]*"' | head -1 | cut -d '"' -f4)
echo "User ID: $USER_ID1"

RESPONSE2=$(curl -s -X POST "$API_URL/users/" \
    -H "Content-Type: application/json" \
    -d "{\"first_name\": \"Jane\", \"last_name\": \"Doe\", \"email\": \"jane@example.com\"}")
echo "response: $RESPONSE2"
USER_ID2=$(echo "$RESPONSE2" | grep -o '"id"[ ]*:[ ]*"[^\"]*"' | head -1 | cut -d '"' -f4)
echo "User ID: $USER_ID2"

RESPONSE3=$(curl -s -X POST "$API_URL/users/" \
    -H "Content-Type: application/json" \
    -d "{\"first_name\": \"Alice\", \"last_name\": \"Marc\", \"email\": \"alice@example.com\"}")
echo "response: $RESPONSE3"
USER_ID3=$(echo "$RESPONSE3" | grep -o '"id"[ ]*:[ ]*"[^\"]*"' | head -1 | cut -d '"' -f4)
echo "User ID: $USER_ID3"

RESPONSE4=$(curl -s -X GET "$API_URL/users/" \
    -H "Content-Type: application/json")
echo "response: $RESPONSE4"
USER_ID4=$(echo "$RESPONSE4" | grep -o '"id"[ ]*:[ ]*"[^\"]*"' | head -1 | cut -d '"' -f4)
echo "User ID: $USER_ID4"


