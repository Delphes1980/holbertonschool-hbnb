// Function to add a place card with details

function addPlaceDetailsCard(place) {
  const detailsPlace = document.getElementById('place-details');
  if (detailsPlace) {
    const detailsPlaceCardContainer = document.createElement('div');
    detailsPlaceCardContainer.classList.add('place-details-card');

    const detailsPlaceCardName = document.createElement('h3');
    const boldPlaceCardName = document.createElement('b');
    boldPlaceCardName.textContent = place.name;
    detailsPlaceCardName.appendChild(boldPlaceCardName);

    const detailsPlaceImageContainer = document.createElement('div');
    detailsPlaceImageContainer.classList.add('place-image');
    const detailsPlaceImage = document.createElement('img');
    detailsPlaceImage.src = place.imageUrl;
    detailsPlaceImage.alt = place.name;
    // detailsPlaceImage.style.width = '100%';
    detailsPlaceImageContainer.appendChild(detailsPlaceImage);

    const placeInfoContainer = document.createElement('div');
    placeInfoContainer.classList.add('place-info');

    const placeInfoHost = document.createElement('p');
    placeInfoHost.innerHTML = `<b>Host:</b> ${place.owner}`;

    const placeInfoPrice = document.createElement('p');
    placeInfoPrice.innerHTML = `<b>Price:</b> ${place.price}`;

    const placeInfoDescription = document.createElement('p');
    placeInfoDescription.innerHTML = `<b>Description:</b> ${place.description}`;

    const placeInfoAmenities = document.createElement('p');
    placeInfoAmenities.innerHTML = `<b>Amenities:</b> ${place.amenities}`;

    placeInfoContainer.appendChild(placeInfoHost);
    placeInfoContainer.appendChild(placeInfoPrice);
    placeInfoContainer.appendChild(placeInfoDescription);
    placeInfoContainer.appendChild(placeInfoAmenities);

    detailsPlaceCardContainer.appendChild(detailsPlaceImageContainer);
    detailsPlaceCardContainer.appendChild(placeInfoContainer);

    detailsPlace.appendChild(detailsPlaceCardContainer);
  } else {
    console.error('Place info not found on place page');
  }
}

document.addEventListener('DOMContentLoaded', () => {
	const detailsPlaceSection = document.getElementById('place-details');
	if (detailsPlaceSection) {
		placeData.forEach(place => {
			addPlaceDetailsCard(place);
		});
	}
});
