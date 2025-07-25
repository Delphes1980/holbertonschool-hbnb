// Function that check user authentication
function checkAuthentication() {
    const token = getCookie('token');
    const loginLink = document.getElementById('login-link');
	const loginButton = document.querySelector('.login-button');

    if (!token) {
        if (loginLink) loginLink.style.display = 'block';
		if (loginButton) loginButton.style.display = 'block';
    } else {
        if (loginLink) loginLink.style.display = 'none';
		if (loginButton) loginButton.style.display = 'none';

      // Fetch places data if the user is authenticated
        fetchPlaces(token)
			.then(placesData => {
                allPlaces = placesData;
                addPriceFilter();
				displayAllPlaces(allPlaces);
                placesFilter();
			})
			.catch(error => {
				console.error('Fail during display of places after authentication', error);
				const placeListContainer = document.getElementById('places-list');
				if (placeListContainer) {
					placeListContainer.innerHTML = `<p style="color: red;">Fail during the places loading: ${error.message}</p>`;
				}
			});
		}
	}


// Function that fetch all places from the DB
async function fetchPlaces(token) {
	try {
		const authHeader = new Headers();
		if (token) {
			authHeader.append('Authorization', `Bearer ${token}`);
		}

		const response = await fetch(`${DATA_URL}/places/`, {
			method: 'GET',
			mode: 'cors',
			credentials: 'include', //for cookies & specific headers
			headers: authHeader,
		});

		if (!response.ok) {
			const errorBody = await response.text();
			console.error(`HTTP error during getting the places: ${response.status} ${response.statusText}`, errorBody);
			throw new Error(`Fail during getting the places: ${response.status} ${response.statusText}`);
		}

		const data = await response.json();
		console.log('Getting list of places succeed:', data);
		return data;
	} catch (error) {
		console.error('Error during fetching the places:', error);
		throw error;
	}
}


// Function that create & add a place card
function addPlaceCard(place) {
  const placeToAdd = document.getElementById('places-list');
  if (placeToAdd) {
    const addPlace = document.createElement('div');
    addPlace.classList.add('place-card');
    addPlace.dataset.price = place.price;

    const addContainer = document.createElement('div');
    addContainer.classList.add('place-card-container');

    // const placeImage = document.createElement('img');
    // placeImage.src = place.imageUrl;
    // placeImage.alt = place.name;

    const placeName = document.createElement('h4');
    const boldName = document.createElement('b');
    boldName.textContent = place.name;
    placeName.appendChild(boldName);

    const placePrice = document.createElement('p');
    placePrice.textContent = `Price per night: ${place.price}€`;

    const placeDetailsButton = document.createElement('button');
    placeDetailsButton.classList.add('details-button');
    placeDetailsButton.textContent = 'View Details';
    placeDetailsButton.dataset.placeId = place.id;

    placeDetailsButton.addEventListener('click', () => {
      window.location.href = `place.html?id=${encodeURIComponent(place.id)}`;
    });

    // addContainer.appendChild(placeImage);
    addContainer.appendChild(placeName);
    addContainer.appendChild(placePrice);
    addContainer.appendChild(placeDetailsButton);

    addPlace.appendChild(addContainer);
    placeToAdd.appendChild(addPlace);
    } else {
        console.error('Place not found');
  }
}


// Function to display a list of places
function displayAllPlaces(places) {
  const placeToAdd = document.getElementById('places-list');
  if (!placeToAdd) {
    console.error('ID "places-list" not found in the DOM');
    return;
  }
  placeToAdd.innerHTML = '';

  if (places && Array.isArray(places) && places.length > 0) {
    places.forEach(place => {
      addPlaceCard(place);
    });
    console.log('List of places displayed with success');
  } else {
    console.warn('No places to display, or invalid data');
    placeToAdd.innerHTML = '<p> No available place for the moment</p>';
  }
}


// Function to add a price filter dynamically
function addPriceFilter() {
	const filterToAdd = document.getElementById('price-filter');
    if (!filterToAdd) {
        console.error('The "#price-filter" element was not found in the DOM');
        return;
    }

    filterToAdd.innerHTML = '';

    const addFilter = document.createElement('option');
    addFilter.value = 'all';
    addFilter.textContent = 'All';
    filterToAdd.appendChild(addFilter);

    const minOption = document.createElement('option');
    minOption.value = '10';
    minOption.textContent = '<= 10€';
    filterToAdd.appendChild(minOption);

    const maxPrice = allPlaces.reduce((max, place) => Math.max(max, place.price), 0);
    const step = 50;

    for (let i = step; i <= maxPrice + step; i += step) {
        const option = document.createElement('option');
        option.value = i.toString();
        option.textContent = `<= ${i}€`;
        filterToAdd.appendChild(option);
    }
	}


// Function that applies the price filter on the place card
function placesFilter() {
    const priceFilterElement = document.getElementById('price-filter');
    if (!priceFilterElement) {
        console.error('The "price-filter" Element was not found');
        return;
    }
    const valueSelection = priceFilterElement.value;

    let filteredPlace = [];

    if (valueSelection === 'all') {
        filteredPlace = [...allPlaces];
    } else {
        const maxPriceFilter = parseFloat(valueSelection);
        if (!isNaN(maxPriceFilter)) {
            filteredPlace = allPlaces.filter(place => place.price <= maxPriceFilter);
        } else {
            filteredPlace = [...allPlaces];
        }

        filteredPlace.sort((a,b) => a.price - b.price);

        displayAllPlaces(filteredPlace);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    loginRedirection();
    loginButtonVisibility();
	checkAuthentication();

    const priceFilter = document.getElementById('price-filter');
    if (priceFilter) {
        priceFilter.addEventListener('change', placesFilter);
    } else {
        console.error('DOM element "#price-filter" not found');
    }
});
