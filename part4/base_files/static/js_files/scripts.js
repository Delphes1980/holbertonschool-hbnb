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

// Function that display a review form for authenticated user
function userReviewForm() {
    const reviewFormSection = document.getElementById('add-review');
    const token = getCookie('token');

    if (reviewFormSection) {
        if (token) {
            reviewFormSection.style.display = 'flex';
            console.log('Review form displayed for authenticated user');
        } else {
        reviewFormSection.style.display = 'none';
        console.log('Review form hidden for non authenticated user');
        }
    } else {
        console.error('The "add-review" section was not found on the page');
    }
}

// Function that submit rating stars
function ratingSubmit() {
    const allStar = document.querySelectorAll('.rating .star');
    const ratingValue = document.getElementById('rating-input');

    allStar.forEach((item, idx) => {
        item.addEventListener('click', () => {
          let click = 0;

        ratingValue.value = item.dataset.value;
        console.log('Selected rating value: ', ratingValue.value)

        // Reinitialization of all stars
        allStar.forEach(star => {
            star.classList.replace('bxs-star', 'bx-star');
            star.classList.remove('active');
        });

        // For visual effects
        for(let i = 0; i < allStar.length; i++) {
          const starCurrentValue = parseInt(allStar[i].dataset.value);
          const selectedRating = parseInt(ratingValue.value);

            if (starCurrentValue <= selectedRating) {
                allStar[i].classList.replace('bx-star', 'bxs-star');
                allStar[i].classList.add('active');
                allStar[i].style.setProperty('--i', i);

            } else {
                allStar[i].classList.replace('bxs-star', 'bx-star');
                allStar[i].classList.remove('active');
                allStar[i].style.setProperty('--i', click);
                click++;
            }
        }
    });
});
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
