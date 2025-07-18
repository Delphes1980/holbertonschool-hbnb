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
      
    const placeDetails = document.createElement('button');
    placeDetails.classList.add('details-button');
    placeDetails.textContent = 'View Details';
    placeDetails.addEventListener('click', () => {
      showPlaceDetails(place.id);
    });

    addContainer.appendChild(placeName);
    addContainer.appendChild(placePrice);
    addContainer.appendChild(placeDetails);

    addPlace.appendChild(addContainer);
    placeToAdd.appendChild(addPlace);
    } else {
        console.error('Place not found');
  }
}






document.addEventListener('DOMContentLoaded', () => {
    loginRedirection();
    addPlaceCard(place);
  });
