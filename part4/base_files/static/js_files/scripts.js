let dialogTag = null;

// Function to redirect the login button to the login page

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

// Function to add a place card

function addPlaceCard(place) {
  const placeToAdd = document.getElementById('places-list');
  if (placeToAdd) {
    const addPlace = document.createElement('div');
    addPlace.classList.add('place-card');

    const addContainer = document.createElement('div');
    addContainer.classList.add('place-card-container');

    const placeImage = document.createElement('img');
    placeImage.src = place.imageUrl;
    placeImage.alt = place.name;

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
      showPlaceDetails(place.id);
    });

    addContainer.appendChild(placeImage);
    addContainer.appendChild(placeName);
    addContainer.appendChild(placePrice);
    addContainer.appendChild(placeDetailsButton);

    addPlace.appendChild(addContainer);
    placeToAdd.appendChild(addPlace);
    } else {
        console.error('Place not found');
  }
}

/* Function to show a card containing al the place details
when clicking on the 'view details' button of the place card*/

function showPlaceDetails(placeId) {
    const modal = document.getElementById('placeDetailsModal');
    // const modalHeaderContent = document.getElementById('modal-header-content');
    const modalBodyContent = document.getElementById('modal-body-content');
    // const modalFooterContent = document.getElementById('modal-footer-content');
    const closeButton = document.querySelector('.close-button');
    const modalPlaceName = document.getElementById('modal-place-name');

    const place = placeData.find(p => p.id === placeId);

    if (!place) {
        console.error('Place not found');
        return;
    }

    modalPlaceName.textContent = place.name;

    modalBodyContent.innerHTML = `
    <p><b>Host:</b> ${place.owner}<p>
    <p><b>Price:</b> ${place.price}€</p>
    <p><b>Description:</b> ${place.description}</p>
    <p><b>Amenities:</b> ${place.amenities}</p>
    `;

    modal.style.display = 'flex';
    document.body.classList.add('modal-open');

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
}

document.addEventListener('DOMContentLoaded', () => {
    // loginRedirection();

    const placeListContainer = document.getElementById('places-list');
    if (placeListContainer) {
      placeData.forEach(place => {
        addPlaceCard(place);
    });
    }

    const detailButtons = document.querySelectorAll('.details-button');
    detailButtons.forEach(button => {
        button.addEventListener('click', (event) => {
            const placeId = parseInt(event.target.dataset.placeId);
            showPlaceDetails(placeId);
        });
});
});
