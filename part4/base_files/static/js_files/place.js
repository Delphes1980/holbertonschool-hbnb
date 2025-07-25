// const DATA_URL = 'http://localhost:5000/api/v1';

function getCookie(name) {
	const cookies = document.cookie.split("; ");
	const value = cookies
		.find(c => c.startsWith(name))
		?.split("=")[1]
		if (value === undefined) {
			return null
		}
		return value
	}

// Function to add a place card with details

function addPlaceDetailsCard(place) {
  const detailsPlace = document.getElementById('place-details');
  if (detailsPlace) {
    detailsPlace.innerHTML = '';

    const detailsPlaceCardContainer = document.createElement('div');
    detailsPlaceCardContainer.classList.add('place-details-card');

    const detailsPlaceCardName = document.createElement('h3');
    const boldPlaceCardName = document.createElement('b');
    boldPlaceCardName.textContent = place.title;
    detailsPlaceCardName.appendChild(boldPlaceCardName);

    // const detailsPlaceImageContainer = document.createElement('div');
    // detailsPlaceImageContainer.classList.add('place-image');
    // const detailsPlaceImage = document.createElement('img');
    // detailsPlaceImage.src = place.imageUrl;
    // detailsPlaceImage.alt = place.name;
    // detailsPlaceImageContainer.appendChild(detailsPlaceImage);

    const placeInfoContainer = document.createElement('div');
    placeInfoContainer.classList.add('place-info');

    const placeInfoHost = document.createElement('p');
    placeInfoHost.innerHTML = `<b>Host:</b> ${place.owner.first_name} ${place.owner.last_name}`;

    const placeInfoPrice = document.createElement('p');
    placeInfoPrice.innerHTML = `<b>Price:</b> ${place.price}`;

    const placeInfoDescription = document.createElement('p');
    placeInfoDescription.innerHTML = `<b>Description:</b> ${place.description || 'No description available'}`;

    const placeInfoAmenities = document.createElement('p');
    placeInfoAmenities.innerHTML = `<b>Amenities:</b> ${place.amenities && Array.isArray(place.amenities) ? place.amenities.join(', ') : 'No amenities available'}`;

    placeInfoContainer.appendChild(placeInfoHost);
    placeInfoContainer.appendChild(placeInfoPrice);
    placeInfoContainer.appendChild(placeInfoDescription);
    placeInfoContainer.appendChild(placeInfoAmenities);

    // detailsPlaceCardContainer.appendChild(detailsPlaceImageContainer);
    detailsPlaceCardContainer.appendChild(detailsPlaceCardName);
    detailsPlaceCardContainer.appendChild(placeInfoContainer);

    detailsPlace.appendChild(detailsPlaceCardContainer);

    const reviewSection = document.getElementById('reviews');

    if (reviewSection) {
      reviewSection.innerHTML = '<h3>Reviews</h3><ul id="review-list"></ul>';
      const reviewList = document.getElementById('review-list');

      if (reviewList) {
        if (place.reviews && Array.isArray(place.reviews) && place.reviews.length > 0) {
          place.reviews.forEach(review => {
            const listItem = document.createElement('li');
            listItem.innerHTML = `<b>${review.user.first_name} ${review.user.last_name}</b><br> ${review.text}<br><b>Rating:</b> ${review.rating}/5`;
            reviewList.appendChild(listItem);
          });
        } else {
          reviewList.innerHTML = '<li>No review for the moment</li>';
        }
      } else {
        console.error('The element with ID "review-list" was not found inside the "reviews" section');
      }
    } else {
      console.error('The element with ID "reviews" was not found on the page');
    }
  } else {
  console.error('Place info not found on place page');
    }
}

async function fetchPlaceDetails(placeId) {
  try {
    const token = getCookie('token');
    const headers = { 'Content-Type': 'application/json'};
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }

    const response = await fetch(`${DATA_URL}/places/${placeId}`, {
    method: 'GET',
    mode: 'cors',
    credentials: 'include',
    headers: headers,
  });
    if (!response.ok) {
      const errorBody = await response.json();
      console.error(`HTTP error during getting the details for the place ${placeId}: ${response.status} ${response.statusText}`, errorBody);
      throw new Error(`Fail during details recuperation for the place: ${response.status} ${response.statusText}`);
    }

    const data = await response.json();
    console.log(`Details for the place ${placeId} with success`, data);
    return data;

  } catch (error) {
    console.error(`Fail during details recuperation of the place ${placeId}`, error);
    throw error;
  }
}

document.addEventListener('DOMContentLoaded', () => {
	const detailsPlaceSection = document.getElementById('place-details');
	if (detailsPlaceSection) {
    const urlParams = new URLSearchParams(window.location.search);
    const placeId = urlParams.get('id');

    if (placeId) {
      fetchPlaceDetails(placeId)
        .then(place => {
          addPlaceDetailsCard(place);
        })

        .catch(error => {
          console.error("Fail during loading places\' details", error);
          detailsPlaceSection.innerHTML = '<p style="color: red;">Sorry, impossible to load places\' details</p>';
        });

    } else {
      detailsPlaceSection.innerHTML ='<p>No place specified. Please choose a place</p>';
    }
  } else {
    console.error('The element with ID "place-details" was not found');
  }
});
