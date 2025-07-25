let dialogTag = null;
// const DATA_URL = 'http://localhost:5000/api/v1';

// Function to redirect the login button to the login page

function loginRedirection() {
  const clickLogin = document.querySelector('.login-button');
  if (clickLogin) {
    clickLogin.addEventListener('click', () => {
      window.location.href = "login.html";
      console.log('Redirection to the login page');
    });
} else {
  console.error('Login button not found');
}
}

// Function to add a place card

function addPlaceCard(place) {
  const placeToAdd = document.getElementById('places-list');
  if (placeToAdd) {
    const addPlace = document.createElement('div');
    addPlace.classList.add('place-card');

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

/* Function to show a card containing all the place details
when clicking on the 'view details' button of the place card*/

async function showPlaceDetails(placeId) {
    const modal = document.getElementById('placeDetailsModal');
    const modalBodyContent = document.getElementById('modal-body-content');
    const closeButton = document.querySelector('.close-button');
    const modalPlaceName = document.getElementById('modal-place-name');

    // const place = placeData.find(p => p.id === placeId);

    // if (!place) {
    //     console.error('Place not found');
    //     return;
    // }

    let place;
    try {
      const response = await fetch(`${DATA_URL}/places/${placeId}`, {
        method: 'GET',
        mode: 'cors',
        credentials: 'include'
      });

      if (!response.ok) {
        throw new Error(`HTTP error: ${response.status} during getting details for ID ${placeId}`);
      }
      place = await response.json();
      console.log(`Getting details for ${placeId}`, place);

    } catch (error) {
      console.error(`Loading impossible for the details of ${placeId} for the modal`, error);
      modalPlaceName.textContent = 'Loading error';
      modalBodyContent.innerHTML = `<p styme="color: red">Sorry, Loading details for this place is impossible. (${error.message})</p>`;
      modal.style.display = 'flex';
      document.body.classList.add('modal-open');
      closeButton.onclick = function() {
        modal.style.display = 'none';
        document.body.classList.remove('modal-open');
      };
      return;
    }

    if (place) {
      modalPlaceName.textContent = place.name;

      modalBodyContent.innerHTML = `
        <p><b>Host:</b> ${place.owner}<p>
        <p><b>Price:</b> ${place.price}€</p>
        <p><b>Description:</b> ${place.description || 'No description available'}</p>
        <p><b>Amenities:</b> ${place.amenities && Array.isArray(place.amenities) ? place.amenities.join(', ') : 'Aucune'}</p>
      `;

    closeButton.onclick = function() {
        modal.style.display = 'none';
        document.body.classList.remove('modal-open');
    };

    // window.onclick = function(event) {
    //     if (event.target == modal) {
    //         modal.style.display = 'none';
    //         document.body.classList.remove('modal-open');
    //     }
    // };
    // console.log('Modal opened');
    } else {
      console.error('PLace details not found after API call for modal:', placeId);
      modalPlaceName.textContent = 'Error';
      modalBodyContent.innerHTML = '<p style="color: red;">Sorry, Loading details for this place is impossible.</p>'
      modal.style.display = 'flex';
      document.body.classList.add('modal-open');
      closeButton.onclick = function() {
        modal.style.display = 'none';
        document.body.classList.remove('modal-open');
      };
    }
  }

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

document.addEventListener('DOMContentLoaded', () => {
    loginRedirection();
});
