#!/bin/bash
# Script to create 5 users (with passwords), 3 places, 10 amenities, and reviews via API.

API_URL="http://127.0.0.1:5000/api/v1"
USER_IDS=()
PLACE_IDS=()

# --- Create 5 users (with password) and store their IDs ---
echo "Creating users..."
for i in $(seq 1 5)
do
  USER_EMAIL="user$i@example.com"
  USER_PASSWORD="password$i" # A simple password for each user
  
  RESPONSE=$(curl -s -X POST "$API_URL/users/" \
    -H "Content-Type: application/json" \
    -d "{\"first_name\": \"User\", \"last_name\": \"Test\", \"email\": \"$USER_EMAIL\", \"password\": \"$USER_PASSWORD\"}")
  
  echo "User $i response: $RESPONSE"
  USER_ID=$(echo "$RESPONSE" | grep -o '"id"[ ]*:[ ]*"[^\"]*"' | head -1 | cut -d '"' -f4)
  
  if [ -n "$USER_ID" ]; then
    USER_IDS+=("$USER_ID")
    echo "User $i ID: $USER_ID, Email: $USER_EMAIL, Password: $USER_PASSWORD"
  else
    echo "Failed to create user $i. Response was: $RESPONSE"
  fi
  sleep 0.2
done

echo "Collected USER_IDS: ${USER_IDS[@]}"

# --- Use the first user as owner for all places (or rotate if you want) ---
OWNER_ID=${USER_IDS[0]}

echo "Creating places..."
for i in $(seq 1 3)
do
  RESPONSE=$(curl -s -X POST "$API_URL/places/" \
    -H "Content-Type: application/json" \
    -d "{\"title\": \"Place$i\", \"description\": \"A nice place $i\", \"price\": 100, \"latitude\": 10.0, \"longitude\": 20.0, \"owner_id\": \"$OWNER_ID\"}")
  echo "Place $i response: $RESPONSE"
  PLACE_ID=$(echo "$RESPONSE" | grep -o '"id"[ ]*:[ ]*"[^\"]*"' | head -1 | cut -d '"' -f4)
  if [ -n "$PLACE_ID" ]; then
    PLACE_IDS+=("$PLACE_ID")
    echo "Place $i ID: $PLACE_ID"
  else
    echo "Failed to create place $i. Response was: $RESPONSE"
  fi
  sleep 0.2
done

echo "Collected PLACE_IDS: ${PLACE_IDS[@]}"

# --- List all places ---
echo "\nListing all places:"
curl -s "$API_URL/places/" | jq .

# --- Create 10 amenities ---
echo "Creating amenities..."
for i in $(seq 1 10)
do
  curl -s -X POST "$API_URL/amenities/" \
    -H "Content-Type: application/json" \
    -d "{\"name\": \"Amenity$i\"}"
  echo
  sleep 0.2
done

# --- Create reviews: each user reviews each place once ---
echo "Creating reviews..."
REVIEW_NUM=1
for USER_ID in "${USER_IDS[@]}"
do
  for PLACE_ID in "${PLACE_IDS[@]}"
  do
    RESPONSE=$(curl -s -X POST "$API_URL/reviews/" \
      -H "Content-Type: application/json" \
      -d "{\"text\": \"Review $REVIEW_NUM by user $(echo $USER_ID | cut -c1-8) for place $(echo $PLACE_ID | cut -c1-8)\", \"rating\": $(( (REVIEW_NUM % 5) + 1 )), \"place_id\": \"$PLACE_ID\", \"user_id\": \"$USER_ID\"}")
    echo "Review $REVIEW_NUM response: $RESPONSE"
    ((REVIEW_NUM++))
    sleep 0.1
  done
done

echo "Done."

echo "\n--- Récapitulatif des utilisateurs créés ---"
for USER_ID in "${USER_IDS[@]}"
do
  echo "User ID: $USER_ID"
done