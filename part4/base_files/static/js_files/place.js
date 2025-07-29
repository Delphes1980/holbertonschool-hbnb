// Function that fetch the details of a specific place
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


// Function that generate stars in an already left review
function generateStarsInReviews(rating) {
  let stars = '';
  const maxStars = 5;
  for (let i = 1; i <= maxStars; i++) {
  if (i <= rating) {
    stars += '<i class="bx bxs-star star"></i>';
    } else {
    stars += '<i class="bx bx-star star"></i>';
    }
  }
  return `<div class="review-rating">${stars}</div>`;
}


// Function that create and add a details card for a specific place
function addPlaceDetailsCard(place) {
  const detailsPlace = document.getElementById('place-details');
  if (detailsPlace) {
    detailsPlace.innerHTML = '';

    const detailsPlaceCardContainer = document.createElement('div');
    detailsPlaceCardContainer.classList.add('place-details-card');

    const detailsPlaceCardName = document.createElement('h3');
    detailsPlaceCardName.classList.add('place-title');
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
    placeInfoPrice.innerHTML = `<b>Price:</b> ${place.price}€`;

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
      reviewSection.innerHTML = '<h3>Reviews</h3>';

      if (place.reviews && Array.isArray(place.reviews) && place.reviews.length > 0) {
        place.reviews.forEach(review => {
          const reviewCard = document.createElement('div');
          reviewCard.classList.add('review-card');

          reviewCard.innerHTML = `
          <p class="user-info"><b>${review.user.first_name} ${review.user.last_name}</b></p>
          ${generateStarsInReviews(review.rating)} <p class="review-content">${review.text}</p>`;

          reviewSection.appendChild(reviewCard);
        });

      } else {
        const noReviewMessage = document.createElement('p');
        noReviewMessage.textContent = 'No review for this place yet';
        reviewSection.appendChild(noReviewMessage);
      }
    } else {
      console.error('The element with ID "reviews" was not found');
    }
  } else {
    console.error('Place info not found on place page');
  }
}


document.addEventListener('DOMContentLoaded', async () => {
  loginButtonVisibility();
  loginRedirection();
  userReviewForm();
  ratingSubmit();

  const reviewForm = document.getElementById('review-form');
  if (reviewForm) {
    reviewForm.addEventListener('submit', async (event) => {
      event.preventDefault();

      const placeIdToSubmit = new URLSearchParams(window.location.search).get('id');
      const reviewTextContent = document.getElementById('review-text').value;
      const ratingInput = reviewForm.querySelector('input[name="rating"]');
      const ratingValue = ratingInput ? parseInt(ratingInput.value) : 0;

      const token = getCookie('token');

      if (!token) {
        alert('You must be authenticated');
        return;
      }

      if (!placeIdToSubmit) {
        alert('Place ID is missing for review submission');
        console.error('Submission failed: Place ID is null or empty');
        return;
      }

      if (!reviewTextContent) {
        alert('You must write a review');
        return;
      }

      if (isNaN(ratingValue) || ratingValue < 1 || ratingValue > 5) {
        alert('You must give a valid rating');
        return;
      }

      try {
      await submitReview(token, placeIdToSubmit, reviewTextContent, ratingValue);

        fetchPlaceDetails(placeIdToSubmit)
          .then(updatedPlace => {
            addPlaceDetailsCard(updatedPlace);
            reviewForm.reset();

            const stars = reviewForm.querySelectorAll('.rating .star');
            stars.forEach(s => {
              s.classList.remove('bxs-star', 'active');
              s.classList.add('bx-star');
            });
            if (ratingInput) ratingInput.value ='';
          })

          .catch (error => {
            console.error("Fail during loading places' details", error);
            alert('Review submit but error during loading place details');
          });

      } catch (error) {
        console.error('Error during reiew submission', error);
        alert(`Error submitting review: ${error.message}`);
      }
    });

      const cancelButton = reviewForm.querySelector('.btn-cancel');
      if (cancelButton) {
        cancelButton.addEventListener('click', () => {
          reviewForm.reset();

          const stars = document.querySelectorAll('#review-form .rating .star');
          const currentRatingInput = document.getElementById('rating-input');
          if (currentRatingInput) {
            currentRatingInput.value ='';
            stars.forEach(s => {
              s.classList.remove('bxs-star');
              s.classList.add('bx-star');
              s.classList.remove('active');
            });
          }
        });
      }
    }

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
            console.error("Fail during loading places' details", error);
          });
      } else {
        console.error('No placeId found in URL');
      }
    } else {
      console.error('The element with ID "place-details" was not found');
    }
  });
