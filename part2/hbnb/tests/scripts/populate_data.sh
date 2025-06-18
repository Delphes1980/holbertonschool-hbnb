#!/bin/bash
# Script to create 5 users, 3 places, and 10 amenities via API, using real user IDs

API_URL="http://127.0.0.1:5000/api/v1"
USER_IDS=()

# Create 5 users and store their IDs
for i in {1..5}
do
  RESPONSE=$(curl -s -X POST "$API_URL/users/" \
    -H "Content-Type: application/json" \
    -d "{\"first_name\": \"User\", \"last_name\": \"Test\", \"email\": \"user$i@example.com\"}")
  echo "Response for user $i: $RESPONSE"
  USER_ID=$(echo "$RESPONSE" | grep -o '"id"[ ]*:[ ]*"[^"]*"' | head -1 | cut -d '"' -f4)
  USER_IDS+=("$USER_ID")
  echo "User $i ID: $USER_ID"
  sleep 0.2
done

# Use the first user as owner for all places (or rotate if you want)
OWNER_ID=${USER_IDS[0]}

# List all places
echo "\n Listing all users:"
curl -s "$API_URL/users/" | jq .

echo "Creating places..."
for i in {1..3}
do
  RESPONSE=$(curl -s -X POST "$API_URL/places/" \
    -H "Content-Type: application/json" \
    -d '{"title": "Place'$i'", "description": "A nice place '$i'", "price": 100, "latitude": 10.0, "longitude": 20.0, "owner": "'$OWNER_ID'"}')
  echo "Response for place $i: $RESPONSE"
  PLACE_ID=$(echo "$RESPONSE" | grep -o '"id"[ ]*:[ ]*"[^"]*"' | head -1 | cut -d '"' -f4)
  PLACE_IDS+=("$PLACE_ID")
  echo "Place $i ID: $PLACE_ID"
  sleep 0.2
done

# List all places
echo -e "\nListing all places:"
curl -s "$API_URL/places/" | jq .

# Create 10 amenities
echo "Creating amenities..."
for i in {1..10}
do
  RESPONSE=$(curl -s -X POST "$API_URL/amenities/" \
    -H "Content-Type: application/json" \
    -d '{"name": "Amenity'$i'"}')
  echo "Response for amenity $i: $RESPONSE"
  AMENITY_ID=$(echo "$RESPONSE" | grep -o '"id"[ ]*:[ ]*"[^"]*"' | head -1 | cut -d '"' -f4)
  AMENITY_IDS+=("$AMENITY_ID")
  echo "Amenity $i ID: $AMENITY_ID"
  sleep 0.2
done

# List all amenities
echo -e "\nListing all amenities:"
curl -s "$API_URL/amenities/" | jq .

echo "Done."
