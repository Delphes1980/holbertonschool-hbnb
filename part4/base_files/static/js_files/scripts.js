let dialogTag = null;
let allPlaces = [];
const DATA_URL = 'http://localhost:5000/api/v1';

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


function loginButtonVisibility() {
  const token = getCookie('token');
  const loginLink = document.getElementById('login-link');
	const loginButton = document.querySelector('.login-button');

    if (loginLink) {
        if (!token) {
          loginLink.style.display = 'block';
        } else {
          loginLink.style.display = 'none';
        }
      }
		if (loginButton) {
      if (!token) {
        loginButton.style.display = 'block';
      } else {
        loginButton.style.display = 'none';
      }
    }
    console.log('Login button visibility update');
  }


// Function to get a cookie by its name
function getCookie(name) {
	const cookies = document.cookie.split("; ");
  const foundCookie = cookies.find(c => {
    return c.startsWith(name);
  })

	let value = undefined;
  if (foundCookie) {
    value = foundCookie.split("=")[1];
  }

  if (value === undefined) {
    return null;
  }
  return value;
}


  /* Function to show a card containing all the place details
  when clicking on the 'view details' button of the place card*/

// async function showPlaceDetails(placeId) {
//     const modal = document.getElementById('placeDetailsModal');
//     const modalBodyContent = document.getElementById('modal-body-content');
//     const closeButton = document.querySelector('.close-button');
//     const modalPlaceName = document.getElementById('modal-place-name');

//     let place;
//     try {
//       const response = await fetch(`${DATA_URL}/places/${placeId}`, {
//         method: 'GET',
//         mode: 'cors',
//         credentials: 'include'
//       });

//       if (!response.ok) {
//         throw new Error(`HTTP error: ${response.status} during getting details for ID ${placeId}`);
//       }
//       place = await response.json();
//       console.log(`Getting details for ${placeId}`, place);

//     } catch (error) {
//       console.error(`Loading impossible for the details of ${placeId} for the modal`, error);
//       modalPlaceName.textContent = 'Loading error';
//       modalBodyContent.innerHTML = `<p styme="color: red">Sorry, Loading details for this place is impossible. (${error.message})</p>`;
//       modal.style.display = 'flex';
//       document.body.classList.add('modal-open');
//       closeButton.onclick = function() {
//         modal.style.display = 'none';
//         document.body.classList.remove('modal-open');
//       };
//       return;
//     }

//     if (place) {
//       modalPlaceName.textContent = place.name;

//       modalBodyContent.innerHTML = `
//         <p><b>Host:</b> ${place.owner}<p>
//         <p><b>Price:</b> ${place.price}€</p>
//         <p><b>Description:</b> ${place.description || 'No description available'}</p>
//         <p><b>Amenities:</b> ${place.amenities && Array.isArray(place.amenities) ? place.amenities.join(', ') : 'Aucune'}</p>
//       `;

//     closeButton.onclick = function() {
//         modal.style.display = 'none';
//         document.body.classList.remove('modal-open');
//     };

//     } else {
//       console.error('PLace details not found after API call for modal:', placeId);
//       modalPlaceName.textContent = 'Error';
//       modalBodyContent.innerHTML = '<p style="color: red;">Sorry, Loading details for this place is impossible.</p>'
//       modal.style.display = 'flex';
//       document.body.classList.add('modal-open');
//       closeButton.onclick = function() {
//         modal.style.display = 'none';
//         document.body.classList.remove('modal-open');
//       };
//     }
//   }


// document.addEventListener('DOMContentLoaded', () => {
//     loginRedirection();
// });
