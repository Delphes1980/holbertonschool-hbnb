let allPlacesForReviewPage = [];

// Function that submit a review
async function submitReview(token, placeId, reviewText, rating) {
    try {
        const headers = { 'Content-Type': 'application/json'};
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }

        const response = await fetch(`${DATA_URL}/reviews/`, {
            method: 'POST',
            headers: headers,
            credentials: 'include',
            body: JSON.stringify({
                text : reviewText,
                place_id: placeId,
                rating: rating})
        });
        if (response.ok) {
            try {
                console.log('Success for review submission');
                const data = await response.json();
                console.log('Response for review submission: ', data);

                const reviewFormReinitializated = document.getElementById('review-form');
                if (reviewFormReinitializated) {
                    reviewFormReinitializated.reset();
                }

            } catch (jsonError) {
                console.error('Error parsing JSON: ', jsonError);
            }

        } else {
            let errorMessage = 'Review submission failed';
            try {
                const errorData = await response.json();
                if (errorData && errorData.message) {
                    errorMessage += 'Details: ' + errorData.message;
                } else {
                    errorMessage += 'Status: ' + response.statusText;
                }
            } catch (networkError) {
                console.error('Network error during review submission', networkError);
            }
            alert(errorMessage);
        }
    } catch (error) {
        console.error('Unexpected error during review submission', error);
    }
}


// Function that search for a specific place
function searchPlace() {
    const searchInput = document.getElementById('place-search-input');

    if (!searchInput) {
        console.error("Search bar (#place-search-input) was not found");
        return;
    }

    // Get the input value & put it in lowercase
    const searchString = searchInput.value.toLowerCase();

    // Filter the list of all places
    const filteredPlace = allPlacesForReviewPage.filter(place => {
        return (place.title || '').toLowerCase().includes(searchString);
    });

    displayPlacesOnReviewPage(filteredPlace);
};


// Function to create a place card with a 'submit' button
function createPlaceCard(place) {
    const placeCard = document.createElement('div');
    placeCard.classList.add('place-card');

    const addContainer = document.createElement('div');
    addContainer.classList.add('place-card-container');

    const placeName = document.createElement('h4');
    placeName.classList.add('place-title');
    const boldName = document.createElement('b');
    boldName.textContent = place.title;
    placeName.appendChild(boldName);

    const placeDescription = document.createElement('p');
    placeDescription.textContent = place.description || 'No description available';
    placeDescription.classList.add('description');

    const placePrice = document.createElement('p');
    placePrice.classList.add('price');
    placePrice.textContent = `Price: ${place.price}€`;

    const submitButton = document.createElement('button');
    submitButton.classList.add('submit-review-button');
    submitButton.textContent = 'Submit a review';
    submitButton.dataset.placeId = place.id;
    submitButton.dataset.placeTitle = place.title;

    addContainer.appendChild(placeName);
    addContainer.appendChild(placeDescription);
    addContainer.appendChild(placePrice);
    addContainer.appendChild(submitButton);

    placeCard.appendChild(addContainer);

    return placeCard;
}


// Function that displays the places in the main container of the review page
function displayPlacesOnReviewPage(placesToDisplay) {
    const placesListContainer = document.getElementById('places-list-review');
    if (!placesListContainer) {
        console.error("Places container (#places-list-review') was not found");
        return;
    }
    placesListContainer.innerHTML = '';

    if (placesToDisplay.length === 0) {
        placesListContainer.innerHTML = '<p>No places available for the moment</p>';
        return;
    }

    placesToDisplay.forEach(place => {
        const placeCard = createPlaceCard(place);
        placesListContainer.appendChild(placeCard);
    });

    document.querySelectorAll('.submit-review-button').forEach(button => {
        button.addEventListener('click', (event) => {
            const placeId = event.target.dataset.placeId;
            const placeTitle = event.target.dataset.placeTitle;
            reviewButtonClick(placeId, placeTitle);
        });
    });
}

// Function to redirect user if not authenticated
function reviewButtonClick(placeId, placeTitle) {
    const token = getCookie('token');

    // Redirect to the login page if not authenticated
    if (!token) {
        alert('You must be authenticated to submit a review');
        window.location.href = 'login.html';
        return;
    }

    // If authenticated, open the modal
    showPlaceDetails(placeId, placeTitle);
}


async function fetchAndDisplayPlaces() {
    try {
        const token = getCookie('token');
        const headers = new Headers();
        if (token) {
            headers.append('Authorization', `Bearer ${token}`);
        }

        const response = await fetch(`${DATA_URL}/places/`, {
            method: 'GET', 
            mode: 'cors',
            credentials: 'include',
            headers: headers,
        });

        if (!response.ok) {
            throw new Error(`HTTP error during places loading: ${response.status} ${response.statusText}`);
        }
        allPlacesForReviewPage = await response.json();

        // Display all the places
        displayPlacesOnReviewPage(allPlacesForReviewPage);

    } catch (error) {
        console.error('Fail during initial places loading', error);
    }
}


document.addEventListener('DOMContentLoaded', () => {
    loginButtonVisibility();
    loginRedirection();
});