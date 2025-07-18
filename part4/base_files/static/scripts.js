let dialogTag = null;

function loginRedirection() {
  const clickLogin = document.querySelector('.login-button')
  if (clickLogin) {
    clickLogin.addEventListener('click', () => {
      window.location.href = "login.html";
      console.log('Redirection to the login page');
    });
} else {
  console.error('Login button not found');
}
}

function addPlaceCard(place) {
  const placeToAdd = document.querySelector('.place-list');
  if (placeToAdd) {
    const addPlace = document.createElement('div');
    addPlace.classList.add('place-card');

    const addContainer = document.createElement('div');
    addContainer.classList.add('place-container');

    const placeName = document.createElement('h4');
    const boldName = document.createElement('b');
    boldName.textContent = place.name;
    placeName.appendChild(boldName);

    const placePrice = document.createElement('p');
    placePrice.textContent = `Price per night: ${place.price}€`;
      
    const placeDetailsButton = document.createElement('button');
    placeDetailsButton.classList.add('details-button');
    placeDetailsButton.textContent = 'View Details';
    placeDetailsButton.addEventListener('click', () => {
      showPlaceDetails(place.id);
    });

    addContainer.appendChild(placeName);
    addContainer.appendChild(placePrice);
    addContainer.appendChild(placeDetailsButton);

    addPlace.appendChild(addContainer);
    placeToAdd.appendChild(addPlace);
    } else {
        console.error('Place not found');
  }
}

function showPlaceDetails(id) {
  if (!dialogTag) {
    dialogTag = document.createElement('dialog');
    dialogTag.id = 'place-details-modal';
    document.body.appendChild(dialogTag);
    console.error('Dialog tag with ID "place-details-modal" was not found in the DOM');
    return;
  }

  const place = placeData.find(p => p.id === id);

  if (!place) {
    console.error('No data found for this place');
    return;
  }

  dialogTag.innerHTML = '';

  const divItem = document.createElement('div');
  divItem.classList.add('modal-container');

  const placeName =document.createElement('h3');
  const boldName = document.createElement('b');
  boldName.textContent = place.name;
  placeName.appendChild(boldName);
  divItem.appendChild(placeName);

  const hostName = document.createElement('p');
  const boldHost = document.createElement('b');
  boldHost.textContent = `Host: ${place.owner}`;
  hostName.appendChild(boldHost);
  divItem.appendChild(hostName);

  const placePrice = document.createElement('p');
  const boldPrice = document.createElement('b');
  boldPrice.textContent = `Price per night: ${place.price}€`;
  placePrice.appendChild(boldPrice);
  divItem.appendChild(placePrice);

  const placeDescription = document.createElement('p');
  const boldDescription = document.createElement('b');
  boldDescription.textContent = `Description: ${place.description}`;
  placeDescription.appendChild(boldDescription);
  divItem.appendChild(placeDescription);

  const placeAmenities = document.createElement('p');
  const boldAmenities = document.createElement('b');
  boldAmenities.textContent = `Amenities: ${place.amenities}`;
  placeAmenities.appendChild(boldAmenities);
  divItem.appendChild(placeAmenities);

  const closeButton = document.createElement('button');
  closeButton.textContent = 'Close';
  closeButton.classList.add('modal-close-button');
  closeButton.addEventListener('click', () => {
    dialogTag.close();
  });

  divItem.appendChild(closeButton);
  dialogTag.appendChild(divItem);

  dialogTag.showModal();
  console.log(`Modal open for the place having this ${id}`);
}





document.addEventListener('DOMContentLoaded', () => {
    loginRedirection();

    const placeList = document.querySelector('.place-list');
      if (placeList) {
        placeList.innerHTML = '';
      }
      placeData.forEach(place => {
        addPlaceCard(place);
      });

    showPlaceDetails(id);
  });
