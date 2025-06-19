#!/bin/bash
# Script to create 5 users, 3 places, 10 amenities, and reviews via API, using real user IDs

API_URL="http://127.0.0.1:5000/api/v1"
USER_IDS=()
PLACE_IDS=()

# Create 5 users and store their IDs
echo "Creating users..."
for i in $(seq 1 5)
do
  RESPONSE=$(curl -s -X POST "$API_URL/users/" \
    -H "Content-Type: application/json" \
    -d "{\"first_name\": \"User\", \"last_name\": \"Test\", \"email\": \"user$i@example.com\"}")
  echo "User $i response: $RESPONSE"
  USER_ID=$(echo "$RESPONSE" | grep -o '"id"[ ]*:[ ]*"[^\"]*"' | head -1 | cut -d '"' -f4)
  if [ -n "$USER_ID" ]; then
    USER_IDS+=("$USER_ID")
    echo "User $i ID: $USER_ID"
  else
    echo "Failed to create user $i"
  fi
  sleep 0.2
done

echo "Collected USER_IDS: ${USER_IDS[@]}"

# Use the first user as owner for all places (or rotate if you want)
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
    echo "Failed to create place $i"
  fi
  sleep 0.2
done

echo "Collected PLACE_IDS: ${PLACE_IDS[@]}"

# List all places
echo "\nListing all places:"
curl -s "$API_URL/places/" | jq .

# Create 10 amenities
echo "Creating amenities..."
for i in $(seq 1 10)
do
  curl -s -X POST "$API_URL/amenities/" \
    -H "Content-Type: application/json" \
    -d "{\"name\": \"Amenity$i\"}"
  echo
  sleep 0.2
done

# Create reviews: each user reviews each place once
echo "Creating reviews..."
REVIEW_NUM=1
for USER_ID in "${USER_IDS[@]}"
do
  for PLACE_ID in "${PLACE_IDS[@]}"
  do
    RESPONSE=$(curl -s -X POST "$API_URL/reviews/" \
      -H "Content-Type: application/json" \
      -d "{\"text\": \"Review $REVIEW_NUM by user $USER_ID for place $PLACE_ID\", \"rating\": $(( (REVIEW_NUM % 5) + 1 )), \"place_id\": \"$PLACE_ID\", \"user_id\": \"$USER_ID\"}")
    echo "Review $REVIEW_NUM response: $RESPONSE"
    ((REVIEW_NUM++))
    sleep 0.1
  done
done

echo "Done."


for USER_ID in "${USER_IDS[@]}"
do
  echo "User ID: $USER_ID"
done

